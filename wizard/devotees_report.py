from openerp.osv import osv,fields
from openerp import _
from openerp.report import report_sxw
from datetime import datetime
import time
import StringIO
import base64
import csv
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
   
class devotees_report2(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context=None):
        super(devotees_report2,self).__init__(cr,uid,name,context=context)
        self.localcontext.update({'time':time,
                                  'get_data':self.get_data,
                                  'get_time':self.get_time,})
    
    def get_time(self):
        str_time = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        return str_time 
    
    def get_data(self,start,end):
        if len(start)==10 and len(end)==10:
            start=datetime.strptime(start,'%Y-%m-%d')
            end=datetime.strptime(end,'%Y-%m-%d')
            
            self.cr.execute("select dev.name,dev.mobile1 from jkp_devotees as dev where dev.today_date >='"+str(start)+"' and dev.today_date <='"+str(end)+"' order by dev.name;")
            data=self.cr.fetchall()
        else:
            self.cr.execute("select dev.name,dev.mobile1 from jkp_devotees as dev order by dev.name")
            data=self.cr.fetchall()
       
        return data

report_sxw.report_sxw('report.devotees.report2','devotees.report.list','addons/jkp_devotees/wizard/devotees_report2.rml',parser=devotees_report2,header=False) 


class devotees_report2_head(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context=None):
        super(devotees_report2_head,self).__init__(cr,uid,name,context=context)
        self.localcontext.update({'time':time,
                                  'get_data':self.get_data,
                                  'get_time':self.get_time,})
    
    def get_time(self):
        str_time = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        return str_time 
    
    def get_data(self,start,end):
        if len(start)==10 and len(end)==10:
            start=datetime.strptime(start,'%Y-%m-%d')
            end=datetime.strptime(end,'%Y-%m-%d')
            
            self.cr.execute("select dev.name,dev.mobile1 from jkp_devotees as dev where dev.today_date >='"+str(start)+"' and dev.today_date <='"+str(end)+"' order by dev.name;")
            data=self.cr.fetchall()
        else:
            self.cr.execute("select dev.name,dev.mobile1 from jkp_devotees as dev order by dev.name")
            data=self.cr.fetchall()
       
        return data

report_sxw.report_sxw('report.devotees.report2.head','devotees.report.list','addons/jkp_devotees/wizard/devotees_report2_head.rml',parser=devotees_report2_head,header=False) 


class devotees_report3(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context=None):
        super(devotees_report3,self).__init__(cr,uid,name,context=context)
        self.localcontext.update({'time':time,
                                  'get_data':self.get_data,
                                  'get_time':self.get_time,})
    
    def get_time(self):
        str_time = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        return str_time 
    
    def get_data(self,start,end):
        
        if len(start)==10 and len(end)==10:
            start=datetime.strptime(start,'%Y-%m-%d')
            end=datetime.strptime(end,'%Y-%m-%d')
            
            self.cr.execute("select dev.name,city.name,dev.mobile1 from jkp_devotees as dev left join res_city as city on (dev.city_id=city.id) where dev.today_date >='"+str(start)+"' and dev.today_date <= '"+str(end)+"' order by dev.name")
            data=self.cr.fetchall()
        else:
            self.cr.execute("select dev.name,city.name,dev.mobile1 from jkp_devotees as dev left join res_city as city on (dev.city_id=city.id) order by dev.name")
            data=self.cr.fetchall()
        return data

report_sxw.report_sxw('report.devotees.report3','devotees.report.list','addons/jkp_devotees/wizard/devotees_report3.rml',parser=devotees_report3,header=False) 


class devotees_report3_head(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context=None):
        super(devotees_report3_head,self).__init__(cr,uid,name,context=context)
        self.localcontext.update({'time':time,
                                  'get_data':self.get_data,
                                  'get_time':self.get_time,})
    
    def get_time(self):
        str_time = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        return str_time 
    
    def get_data(self,start,end):
        
        if len(start)==10 and len(end)==10:
            start=datetime.strptime(start,'%Y-%m-%d')
            end=datetime.strptime(end,'%Y-%m-%d')
            
            self.cr.execute("select dev.name,city.name,dev.mobile1 from jkp_devotees as dev left join res_city as city on (dev.city_id=city.id) where dev.today_date >='"+str(start)+"' and dev.today_date <= '"+str(end)+"' order by dev.name")
            data=self.cr.fetchall()
        else:
            self.cr.execute("select dev.name,city.name,dev.mobile1 from jkp_devotees as dev left join res_city as city on (dev.city_id=city.id) order by dev.name")
            data=self.cr.fetchall()
        return data

report_sxw.report_sxw('report.devotees.report3.head','devotees.report.list','addons/jkp_devotees/wizard/devotees_report3_head.rml',parser=devotees_report3,header=False) 
        

class devotees_report_list(osv.osv_memory):
    _name="devotees.report.list"
    
    _columns={'all_devotees':fields.boolean('All Devotees'),
              'name_place':fields.boolean('Name and Contact No '),
              'name_place_no':fields.boolean('Name, Place and Contact No'),
              'devotee_details':fields.many2many('jkp.devotees','dev_dev_rel','dev_prominent','prominent_dev','Devotees List'),
              'from_date':fields.date('From (Creation Date)',),
              'to_date':fields.date('To (Creation Date)',),
              'header':fields.boolean('Print Header'),
              }
    _defaults={'all_devotees':True,
               'name_place':True}
    
    def onchange_field1(self, cr,uid,ids,name_place, ):
        print name_place
        res={}
        if name_place==True:
            res['value']={'name_place_no':False}
            
        else:
            res['value']={'name_place_no':True}
        return res
    
    def onchange_field2(self, cr,uid,ids,name_place_no, ):
        
        res={}
        if name_place_no==True:
            res['value']={'name_place':False}
            
        else:
            res['value']={'name_place':True}
        return res
    
    def get_devotee_list(self,cr,uid,ids,context=None):
        res={}
        report_id=[]
        data=self.browse(cr,uid,ids)
        from_date=data[0].from_date
        to_date=data[0].to_date
        field1=data[0].name_place
        field2=data[0].name_place_no
        head  = data[0].header
        print from_date
        print to_date
        devotee_obj=self.pool.get('jkp.devotees')
#        if to_date and from_date:
#            report_ids=devotee_obj.search(cr,uid,[('today_date','>=' ,from_date),('today_date','<=' ,to_date),('categ6','=',True)])
#        else:
#            report_ids=devotee_obj.search(cr,uid,[])
#
#        self.write(cr,uid,ids,{'devotee_details':[(6,0,report_ids)]})
        report_obj = self.pool.get('ir.actions.report.xml')
        datas = {'ids' : ids}
        if field1==True and head == False:
            print "name place.........................."
            rpt_id =  report_obj.search(cr, uid, [('report_name','=','devotees.report2')])[0]
            print rpt_id
            
        if field1==True and head == True:
            print "name place..........................head"
            rpt_id =  report_obj.search(cr, uid, [('report_name','=','devotees.report2.head')])[0]
            print rpt_id
            
        if field2==True and head == False:
            print "name place..........................contact no...."
            rpt_id =  report_obj.search(cr, uid, [('report_name','=','devotees.report3')])[0]
            print rpt_id
            
        if field2==True and head == True:
            print "name place..........................contact no. HEAD..."
            rpt_id =  report_obj.search(cr, uid, [('report_name','=','devotees.report3.head')])[0]
            print rpt_id
            
        if not rpt_id:
            raise osv.except_osv(_('Invalid action !'), _('Report for this name does not exists.'))
        rpt_type = report_obj.read(cr, uid, rpt_id, ['report_name'])
        return {
                
           'type' : 'ir.actions.report.xml',
           'report_name':str(rpt_type['report_name']),
           'datas' : datas,
           'nodestroy':True,
        }
        return True
    
   
from openerp.osv import osv,fields
import StringIO
import base64
import csv

class export_devotees(osv.osv):
    _name="export.devotees"
    _columns={
             'name':fields.char('File Name',size=250,readonly=True),
             'export_data':fields.binary('File',readonly=True),
             'from_date':fields.date('From (Creation Date)',),
             'to_date':fields.date('To (Creation Date)',),
             'all_devotees':fields.boolean('All Devotees'),
              'name_place':fields.boolean('Name and Contact No '),
              'name_place_no':fields.boolean('Name,Place and Contact No'),
             }
    _defaults={
               'all_devotees':True,
               'name_place_no':True,
               'name':'Devotees.xls',
               }
    
    
    def get_data(self,cr,uid,ids,context=None):
        res={}
        headings1=['Name','Place','Contact No']
        headings2=['Name','Place','Contact No']
        fp = StringIO.StringIO()
        writer = csv.writer(fp)
        writer.writerow(headings1)
        export_object=self.browse(cr, uid, ids)[0]
        start =export_object.from_date
        end   =export_object.to_date
        case_one = export_object.name_place_no
        case_two = export_object.name_place
        print case_one,case_two,"4343"
        if case_one:
            if start and end:
                cr.execute("select dev.name,city.name,dev.mobile1 from jkp_devotees as dev left join res_city as city on (dev.city_id=city.id) where dev.today_date >='"+str(start)+"' and dev.today_date <= '"+str(end)+"' order by dev.name limit 100")
                data=cr.fetchall()
            else:
                cr.execute("select dev.name,dev.mobile1 from jkp_devotees as dev order by dev.name limit 100")
                data=cr.fetchall()
        if case_two:
            if start and end:
                cr.execute("select dev.name,dev.mobile1 from jkp_devotees as dev where dev.today_date >='"+str(start)+"' and dev.today_date <='"+str(end)+"' order by dev.name  limit 100;")
                data=cr.fetchall()
            else:
                cr.execute("select dev.name,dev.mobile1 from jkp_devotees as dev order by dev.name limit 100")
                data=cr.fetchall()        
        fp = StringIO.StringIO()
        writer = csv.writer(fp)
        data_list=data
                   
        for data in data_list:
            row = []
            for d in data:
                if isinstance(d, basestring):
                    d = d.replace('\n',' ').replace('\t',' ')
                    try:
                        d = d.encode('utf-8')
                    except:
                        pass
                if d is False: d = None
                row.append(d)
    
            writer.writerow(row)
        fp.seek(0)
        data = fp.read()
        fp.close()
        out=base64.encodestring(data)
        self.write(cr, uid, ids, {'export_data':out, 'name':'Devotees.xls'}, context=context)
        return True
    
