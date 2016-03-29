from openerp.osv import osv,fields
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
import urllib
import urllib2
import time
from datetime import datetime,timedelta

class message_server(osv.osv):
    _name="message.server"
    _columns={
              'name':fields.char('Server Name',required=True),
              'user_name':fields.char('User Name',required=True),
              'password':fields.char('Password',required=True),
              }


class message_template(osv.osv):
    _name="message.template"
    _columns={'date':fields.datetime('Creation Date',readonly=True),
              'name':fields.char('Template Name',required=True),
              'template_content':fields.char('Template Content',size=3000,required=True),
                            }
    _defaults={'date':lambda *a: time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),}
    
    
    
class devotees_logs(osv.osv):
    _name="devotees.logs"
    
    _columns={'date_create':fields.date('Create Date'),
              'user_id':fields.many2one('res.users','User',readonly=True),
              'creation_date':fields.datetime('Log Updated On',readonly=True),
              'log_date':fields.datetime('Sent Date',readonly=True),
              'mobile_no':fields.char('Mobile No',size=20,readonly=True),
              'type':fields.selection([('Scheduled','Scheduled'),('Non','Non Scheduled')],'Type',readonly=True),
              'state':fields.selection([('Outgoing','Outgoing'),('Sent','Sent'),('Failed','Failed'),('Cancel','Cancel')],'Server Status',readonly=True),
              'state2':fields.selection([('Draft','Draft'),('Confirmed','Confirmed')],'State2'),
              'status':fields.char('SMS Country Status',size=100,readonly=True,),
              'log_id':fields.many2one('jkp.devotees',"Devotee's Name",ondelete="cascade",readonly=True,),
              'content':fields.text('Content',readonly=True),
              'schedule_date':fields.datetime('Scheduled Date'),
              'server_id':fields.many2one('message.server','Outgoing Message Server'),
              } 
    _defaults={
               'user_id':lambda obj, cr, uid, cnt: uid,
               'type':'Non',
               'state2':'Draft',
               'date_create':lambda *a: time.strftime(DEFAULT_SERVER_DATE_FORMAT),
               }
    _order='log_date desc'
    
   
    def unlink(self, cr, uid, ids, context=None):
        stat = self.read(cr, uid, ids, ['state2'], context=context)
        unlink_ids = []
        for t in stat:
            if t['state2'] in ('Draft'):
                self.write(cr,uid,ids,{'state2':'Confirmed'})
            elif t['state2'] in ('Confirmed'): 
                unlink_ids.append(t['id'])
        osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
        return True   
    
    def _fetch_sms(self,cr,uid,ids=False,context=None):
        print "SMS Scheduler is running......................................"
        log_obj=self.pool.get('devotees.logs')
        date=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
        date1=datetime.strftime(datetime.now(),'%Y-%m-%d 00:00:00')
        old_sms_ids = log_obj.search(cr,uid,[('state','=','outgoing'),('schedule_date','<',date1)])
        if old_sms_ids:
            print "old sms ids...........",old_sms_ids
            log_obj.write(cr, uid, old_sms_ids, {'state':'Failed'})
        sms_ids = log_obj.search(cr,uid,[('state','=','Outgoing'),('schedule_date','<=',date),('schedule_date','>=',date1)])
        
        for each in log_obj.browse(cr, uid, sms_ids):
            print "mobile number....",each.mobile_no
            print each.server_id.user_name
            print each.server_id.password
            print "-----------------------------------"
            values = { 
                            "User" : each.server_id.user_name,
                            "passwd" : each.server_id.password,
                            "mobilenumber" :each.mobile_no,
                            "message" : each.content,
                            "sid" : "JKPISC",
                            "mtype" : "N",
                            "DR" : "Y",
                            }  
            date = datetime.now()
            url = 'http://smscountry.com/SMSCwebservice_Bulk.aspx'
            postdata = urllib.urlencode(values)
            req = urllib2.Request(url, postdata)
    
            try:
                response = urllib2.urlopen(req)
                response_url = response.geturl()
                if response_url==url:
                    print 'SMS sent!'
                    log_obj.write(cr,uid,each.id,{'state':'Sent'})
            except urllib2.URLError, e:
                print 'Send failed!'
                log_obj.write(cr,uid,each.id,{'state':'Outgoing'})
            
            
    
    

class send_sms(osv.osv_memory):
    _name="send.sms"
    
    _columns={'to_all':fields.boolean('All Devotees'),
              'to_selected':fields.boolean('Selected Devotees'),
              'to_category':fields.boolean('Categorywise Devotees'),
              'msg_category_ids':fields.many2many('jkp.category','msg_catgeg_rel','categ_id','message_id','Categories'),
              'mobile_no':fields.text('Mobile No',help="Additional mobile numbers should be separated by commas.You do not need to type mobile numbers of selected devotees.Message will be send to them automatically."),
              'sms_text':fields.text('SMS',required=True),
              'message_template':fields.many2one('message.template','Message Template'),
              'schedule_date':fields.datetime('Scheduled Date'),
              'schedule_sms':fields.boolean('Schecule SMS'),
              'server_id':fields.many2one('message.server','Outgoing Message Sever',required=True)
              }
    
    _defaults={'schedule_date':lambda *a: time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),}
    
    
    def onchange_template(self, cr, uid, ids, template_id, context=None):
        print "templaate id is ............",template_id,
        res={}
        if not template_id:
            return res
        else:
            messgae = self.pool.get('message.template').browse(cr,uid,template_id).template_content
            res['value']={'sms_text':messgae}
        return res
    
#    def default_get(self,cr,uid,fields,context=None):
#        res={}
#        if not context:
#            return res
#        act_id = context.get('active_ids', [])
#        res = super(send_sms, self).default_get(cr, uid, fields, context=context)
#        if act_id:
#            number_list=[]
#            for val in act_id:
#                number=self.pool.get('jkp.devotees').browse(cr,uid,val).mobile1
#                if number:
#                    number_list.append(number)
#            unique_list=list(set(number_list))
#            print "unique list",unique_list
#            if unique_list:
#                num=''
#                for val in unique_list:
#                    num=','+num
#                    num=val+num
#                    
#            print num
#            res.update({'mobile_no':num})
#            
#        return res
        
    def sms_log_create(self,cr,uid,ids,context=None):
        "################# LOG CREATE ##################"
        devotee_ids = []
        final_list  = []
        additional_number_list = []
        log_obj     = self.pool.get('devotees.logs')
        categ_obj   = self.pool.get('jkp.category')
        devotee_obj = self.pool.get('jkp.devotees')
        
        sms_obj = self.browse(cr,uid,ids[0])
        act_id = context.get('active_ids', [ ])
        schedule_time  = sms_obj.schedule_date
        message        = sms_obj.sms_text
        server         =sms_obj.server_id.id
        print "server id .........................",server
        if_scheduled  = sms_obj.schedule_sms
        if if_scheduled:
            type1='Scheduled'
        else:
            type1='Non'

        additional_number = sms_obj.mobile_no
        if additional_number:
            additional_number_list = additional_number.split(',')
      
        if sms_obj.to_all:
            devotee_ids = devotee_obj.search(cr, uid, [])
       
        if sms_obj.to_selected:
            for val in act_id:
                devotee_ids.append(val)
         
        if sms_obj.to_category:
            for categ in sms_obj.msg_category_ids:
                devCateg_ids = devotee_obj.search(cr, uid, [('category_ids','=',categ.id)])
                for category in devCateg_ids:
                    devotee_ids.append(category)
        
        number_list = list(set(devotee_ids))
        for val in number_list:
            num = devotee_obj.browse(cr,uid,val).mobile1
            if num:
                final_list.append(num)
                
        for val1 in additional_number_list:
            print "ADditional number for looop.............",val1
            if val1:
                "Additional numbers ...................",val1
                final_list.append(val1)
        print "============= FInal number list is going to be unique...."
        final_numbers = list(set(final_list))
        
        for number in final_numbers:
            valsc=''
            try:
                valsc = devotee_obj.search(cr, uid, [('mobile1','=',number)])[0]
            except:
                pass
            date = datetime.now()
            if valsc:
                log_obj.create(cr,uid,{'state':'Outgoing','user_id':uid,'log_id':valsc,'type':'Message','log_date':date,'content':message,'mobile_no':number,'schedule_date':schedule_time,'type':type1,'server_id':server})
            else:
                log_obj.create(cr,uid,{'state':'Outgoing','user_id':uid,'type':'Message','log_date':date,'content':message,'mobile_no':number,'schedule_date':schedule_time,'type':type1,'server_id':server})
        return True
        
            
    
#    def sms_send(self,cr,uid,ids,context=None):
#        #!/usr/bin/python
#        log_obj=self.pool.get('devotees.logs')
#        act_id = context.get('active_ids', [])
#        message=self.browse(cr,uid,ids[0]).sms_text
#        number_list=self.browse(cr,uid,ids[0]).mobile_no
#        unique=set([]) 
#        if number_list:
#            values = { 
#                            "User" : "JKPISC",
#                            "passwd" : "chandra",
#                            "mobilenumber" :number_list,
#                            "message" : message,
#                            "sid" : "JKPISC",
#                            "mtype" : "N",
#                            "DR" : "Y",
#                            }
#            date = datetime.now()
#            url = 'http://smscountry.com/SMSCwebservice_Bulk.aspx'
#            postdata = urllib.urlencode(values)
#            req = urllib2.Request(url, postdata)
#    
#            try:
#                response = urllib2.urlopen(req)
#                response_url = response.geturl()
#                if response_url==url:
#                    print 'SMS sent!'
#            except urllib2.URLError, e:
#                print 'Send failed!'
#        print "---------------------------------------"
#        for val in act_id:
#                number=self.pool.get('jkp.devotees').browse(cr,uid,val).mobile1
#                if number:
#                    
#                    if number not in unique:
#                        unique.add(number)
#                        print ".................not in unique"
#                        values = { 
#                                "User" : "JKPISC",
#                                "passwd" : "chandra",
#                                "mobilenumber" :number,
#                                "message" : message,
#                                "sid" : "JKPISC",
#                                "mtype" : "N",
#                                "DR" : "Y",
#                                }
#                        date = datetime.now()
#                        url = 'http://smscountry.com/SMSCwebservice_Bulk.aspx'
#                        postdata = urllib.urlencode(values)
#                        req = urllib2.Request(url, postdata)
#                
#                        try:
#                            response = urllib2.urlopen(req)
#                            response_url = response.geturl()
#                            if response_url==url:
#                                print 'SMS sent!'
#                                log_obj.create(cr,uid,{'user_id':uid,'log_id':val,'type':'Message','status':'Sent','log_date':date,'content':message,'mobile_no':number})
#                        except urllib2.URLError, e:
#                            print 'Send failed!'
#                            log_obj.create(cr,uid,{'user_id':uid,'log_id':val,'type':'Message','status':'Failed','log_date':date,'content':message,'mobile_no':number})
#                            print e.reason
#        return True
#    


