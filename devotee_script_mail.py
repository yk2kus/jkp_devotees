from openerp.osv import osv, fields
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
import re
from openerp import tools
import os
import logging
import time
from openerp import SUPERUSER_ID
from openerp.tools.safe_eval import safe_eval as eval
from openerp import _
import base64, urllib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEBase import MIMEBase
from email import Encoders
_logger = logging.getLogger(__name__)
from datetime import datetime
from openerp.tools import flatten
#import GnuPGInterface

from email.message import Message


class birthday_configuration(osv.osv):
    _name="birthday.configuration"
    _columns={
              'date':fields.datetime('Create Date',readonly=True),
              'user_id':fields.many2one('res.users','User',readonly=True),
              'template_id':fields.many2one('email.template','Template',required=True),
              'server_id':fields.many2one('ir.mail_server','Outgoing Mail Server',required=True),
              }
    _defaults={
               'user_id':lambda obj, cr, uid, cnt: uid,
               'date':lambda *a: time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
               }
    _order='date desc'


class mail_logs(osv.osv):
    _name="mail.logs"
    _columns={
              'date_create':fields.date('Create Date'),
              'date':fields.datetime('Sent Date',readonly=True),
              'subject':fields.char('Subject',size=1000,readonly=True),
              'email_from':fields.char('Email From',readonly=True,required=True),
              'email_to':fields.char('Email To',readonly=True,required=True),
              'template_id':fields.many2one('email.template','Template',readonly=True),
              'mail_body':fields.text('Email Content',size=5000,readonly=True),
              'state':fields.selection([('sent','Sent'),('outgoing','Outgoing'),('failed','Failed'),('cancel','Canceled')],'Status',readonly=True),
              'state2':fields.selection([('Draft','Draft'),('Confirmed','Confirmed')],'Deletion State'),
              'status':fields.selection([('Birthday Email','Birthday Email'),('Email','Email')],'Email Type',readonly=True),
              'log_id':fields.many2one('jkp.devotees',"Devotee's Name",readonly=True),
              'user_id':fields.many2one('res.users','User',readonly=True),
              'server_id':fields.many2one('ir.mail_server','Outgoing Mail Server',required=True),
              'data_ids': fields.many2many('ir.attachment','mail_compose_log_rel','log_id', 'attachment_id', 'Attachments',readonly=True),
              'schedule_date':fields.datetime('Schedule Date'),
              'type':fields.selection([('Scheduled','Scheduled'),('Non','Non Scheduled')],'Type',readonly=True),
              'sign':fields.text('Email Signature'),
              }
    _defaults={
               'user_id':lambda obj, cr, uid, cnt: uid,
               'state2':'Draft',
               'date_create':lambda *a: time.strftime(DEFAULT_SERVER_DATE_FORMAT),
               }
    _order='date desc'
    
    
    def retry_sending(self, cr, uid ,ids ,context=None):
        if not context:
            context={}
        date = datetime.now()
        self.write(cr,uid,ids,{'state':'outgoing','schedule_date':date})
        return True
    
    def cancel_sending(self, cr, uid ,ids ,context=None):
        if not context:
            context={}
        self.write(cr,uid,ids,{'state':'cancel'})
        return True
    
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
    
    
    
class email_template(osv.osv):
    "Templates for sending email"
    _inherit = "email.template"
    _description = 'Email Templates'
    _columns={'model_id': fields.many2one('ir.model', 'Applies to', help="Select the object in which you want to use the template.For devotees type jkp.devotees or select it"),
               'creation_date':fields.datetime('Creation Date',readonly=True),
               'is_signature':fields.boolean('Include Singnature'),
                'email_sign':fields.text('Type Signature Here'),
               }
    _defaults={'creation_date':lambda *a: time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),}
    


class mail_compose_message(osv.TransientModel):

    _inherit = 'mail.compose.message'
    
    
    def default_get(self, cr, uid, fields, context=None):
        """ Handle composition mode. Some details about context keys:
            - comment: default mode, model and ID of a record the user comments
                - default_model or active_model
                - default_res_id or active_id
            - reply: active_id of a message the user replies to
                - default_parent_id or message_id or active_id: ID of the
                    mail.message we reply to
                - message.res_model or default_model
                - message.res_id or default_res_id
            - mass_mail: model and IDs of records the user mass-mails
                - active_ids: record IDs
                - default_model or active_model
        """
        if context is None:
            context = {}
        result = super(mail_compose_message, self).default_get(cr, uid, fields, context=context)
        
        # get some important values from context
        composition_mode = context.get('default_composition_mode', context.get('mail.compose.message.mode'))
        model = context.get('default_model', context.get('active_model'))
        res_id = context.get('default_res_id', context.get('active_id'))
        message_id = context.get('default_parent_id', context.get('message_id', context.get('active_id')))
        active_ids = context.get('active_ids')
        
        # get default values according to the composition mode
        
        if composition_mode == 'reply':
            vals = self.get_message_data(cr, uid, message_id, context=context)
        elif composition_mode == 'comment' and model and res_id:
            vals = self.get_record_data(cr, uid, model, res_id, context=context)
        elif composition_mode == 'mass_mail' and model and active_ids:
            vals = {'model': model, 'res_id': res_id}
        else:
            vals = {'model': model, 'res_id': res_id}
        if composition_mode:
            vals['composition_mode'] = composition_mode
        
        if active_ids:
#            vals['devotees_ids'] = [devotees.id for devotees in self.pool.get(str(model)).browse(cr, uid, self.pool.get(str(model)).search(cr, uid, [])) if devotees.email]
            vals['devotees_ids'] = [devotees.id for devotees in self.pool.get(str(model)).browse(cr, uid, active_ids) if devotees.email]
        print "vals.................",vals
#        for field in vals:
#            if field in fields:
#                result[field] = vals[field]
                
        return result

    _columns = {'selected':fields.boolean('Selected Devotees'),
                'all':fields.boolean('All Devotees'),
                'category':fields.boolean('Category wise'),
                'schedule_mail':fields.boolean('Schedule Email'),
                'schedule_date':fields.datetime('Schedule Date'),
                'category_ids':fields.many2many('jkp.category','mail_categ_rel','categ_id','mail_id','Categories'),
                'mail_server_id':fields.many2one('ir.mail_server','From',required=True),
                'devotees_ids': fields.many2many('jkp.devotees', 'mail_compose_message_jkp_devotees_rel',
                                                'wizard_id', 'devotees_id', 'Additional contacts'),
                'additional_contacts':fields.text('Additional contacts'),
                
                
                }
    _defaults={
               'schedule_date':lambda *a: time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),}
    
    def onchange_selection(self,cr, uid, selected,all,category,context=None):
        res={}
        if selected:
            res['value']={'all':False,'category':False}
        elif all:
            res['value']={'selected':False,'category':False}
        elif category:
            res['value']={'selected':False,'all':False}
        return res
    
    def mail_birthday_queue(self, cr, uid, ids=False, context=None):
        birthday_obj = self.pool.get('birthday.configuration')
        config_ids = birthday_obj.search(cr, uid, [])
        month = datetime.now().month
        day = datetime.now().day
        dtm= datetime.now()
        mail_list = []
        if len(str(month)) == 1:
            month = '0'+str(month)
        if len(str(day)) == 1:
            day = '0'+str(day)
        if config_ids:
            config_data = birthday_obj.browse(cr, uid, config_ids[-1])
            if config_data:
                sender = config_data.server_id.smtp_user  
                server_id = config_data.server_id
                queue_obj =self.pool.get('mail.logs')
                    
                cr.execute("select distinct email from jkp_devotees where to_char(dob,'MM') = '"+str(month)+"' \
                and to_char(dob,'DD') = '"+str(day)+"'")
                temp = cr.fetchall()
                for val1 in temp:
                    if len(val1) > 0 and val1[0] != None:
                        mail_list.append(val1[0])
                for val in mail_list:
                    vals = {
                            'user_id':uid,
                            'date':dtm,
                            'subject':config_data.template_id.subject,
                            'email_from':config_data.server_id.smtp_user  ,
                            'email_to':val,
                            'mail_body':config_data.template_id.body_html,
                            'server_id':config_data.server_id.id,
                            'state':'outgoing',
                            'status':'Birthday Email',
                            'schedule_date':dtm,
                            'data_ids':[(6,0,[att.id for att in config_data.template_id.attachment_ids])],
                            }
                    queue_obj.create(cr, uid, vals)
        
        return True
    
    def mail_queue(self, cr, uid, ids, context=None):
   
        mail = self.browse(cr, uid, ids[0])
        template_obj = self.pool.get('email.template')
        dev_obj = self.pool.get('jkp.devotees')
        sender = mail.mail_server_id.smtp_user  
        if mail.schedule_mail:
            mail_type='Scheduled'
        else:
            mail_type='Non'
        
        sch_date = mail.schedule_date
        subject = mail.subject
        mail_body = mail.body or '\n'
        signature=''
        if mail.template_id and template_obj.browse(cr, uid,mail.template_id).email_sign:
            signature= template_obj.browse(cr, uid,mail.template_id).email_sign
            
    
        if not sch_date:
            sch_date = datetime.now()
        server_id = mail.mail_server_id.id
        queue_obj =self.pool.get('mail.logs')
        devotee_ids = []
        mail_list = []
        category_ids = []
        dtm = datetime.now()
        if context:
            devotee_ids = context.get('active_ids',[])
        print "devotee ids.........................",devotee_ids
        if mail.all:
            devotee_ids.append(dev_obj.search(cr, uid, [('dormant','=',False),('email','!=',False)]))
        if mail.category_ids:
            for categ in mail.category_ids:
                category_ids.append(categ.id)
            devotee_ids.append(dev_obj.search(cr, uid, [('dormant','=',False),('category_ids','in',category_ids),('email','!=',False)]))
        
        devotee_ids = list(set(flatten(devotee_ids)))
        if len(devotee_ids) == 1:
            devotee_ids.append(devotee_ids[0])
        send_to_ids = tuple(devotee_ids)
        
        if mail.additional_contacts:
            mail_list=mail.additional_contacts.split(',')
        print  "send to ids....................",send_to_ids
        if send_to_ids:
            cr.execute("select distinct email from jkp_devotees where email is not null and id in "+str(send_to_ids))
            temp = cr.fetchall()
            for val1 in temp:
                mail_list.append(val1[0])
        mail_list = list(set(flatten(mail_list)))
        
        for val in mail_list:
            receiver=val
            devotee_id=''
            if val:
                searchMail_ids = dev_obj.search(cr, uid, [('email','=',val),('state','=','Draft')])
                if searchMail_ids:
                    devotee_id=searchMail_ids[0]
                dtm= datetime.now()
            
                
                vals = {
                        'log_id':devotee_id,
                        'user_id':uid,
                        'date':dtm,
                        'subject':subject or 'No Subject',
                        'email_from':sender,
                        'email_to':receiver,
                        'mail_body':mail_body,
                        'server_id':server_id,
                        'state':'outgoing',
                        'status':'Email',
                        'schedule_date':sch_date,
                        'data_ids':[(6,0,[att.id for att in mail.attachment_ids])],
                        'type':mail_type,
                        'sign':signature,
                        }
                queue_obj.create(cr, uid, vals)
    
        return True
    
    def send_script_mail(self, cr, uid, ids=False, context=None ):
        
        date=datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
        date1=datetime.strftime(datetime.now(),'%Y-%m-%d 00:00:00')
        log_obj =  self.pool.get('mail.logs')
        old_mail_ids = log_obj.search(cr,uid,[('state','=','outgoing'),('schedule_date','<',date1)])
        if old_mail_ids:
            log_obj.write(cr, uid, old_mail_ids, {'state':'failed'})
        mail_ids = log_obj.search(cr,uid,[('state','=','outgoing'),('schedule_date','<=',date),('schedule_date','>=',date1)])
     
        for each in log_obj.browse(cr, uid, mail_ids):
            user = each.server_id.smtp_user
            password = each.server_id.smtp_pass
            attachments = []
            for attach in each.data_ids: 
                attachments.append((attach.datas_fname or attach.name, base64.b64decode(attach.datas), attach.inline, attach.cid))
            strTo = each.email_to
            
            msgRoot = MIMEMultipart('related')
            msgRoot['Subject'] = each.subject
            msgRoot['From'] = user
            msgRoot['To'] = strTo
            msgRoot.preamble = 'This is a multi-part message in MIME format.'
            # Encapsulate the plain and HTML versions of the message body in an
            # 'alternative' part, so message agents can decide which they want to display.
            msgAlternative = MIMEMultipart('alternative')
            msgRoot.attach(msgAlternative)
            
            if not each.mail_body:
                each.mail_body=''   
                    
            if each.sign:
               signature= '-- \n'+ '\n' + each.sign
            else:
                signature=''
                
            SRC=''      
            SRC3=''          
            if attachments:
               
                for (fname, fcontent, inline, cid) in attachments:
                    if  inline:
                        cid = fname.replace(" ", "_").lower()   
                        SRC =  SRC + '<br><img src="cid:%s" ><br>' % cid                          
            SRC3= each.mail_body + SRC + signature
            print "SRC.................................",SRC3
            msgText = MIMEText(SRC3,'html')
            msgAlternative.attach(msgText)
            
            
            if attachments:                
                SRC=''
                for (fname, fcontent, inline, cid) in attachments:
                    print "fname....***,",fname,"inline....***,",inline
                    if  inline:
                        print "under if condition ........................",fname
                                                
                        cid = fname.replace(" ", "_").lower()                        
                        SRC = '<br><img src="cid:%s"><br>' % cid
                        msgText = MIMEText(SRC, 'html')
                        print "SRC.........",SRC
                       
                        msgImage = MIMEImage(fcontent)
                        
                        msgImage.add_header('Content-ID', '<%s>' % cid)
                        msgImage.add_header('Content-Disposition' , 'inline' , filename=fname)
                        msgRoot.attach(msgImage)
                        
    
                    else:
                        print "under else condition ........................ when no inline",fname
                        filename_rfc2047 = fname
                        part = MIMEBase('application', "octet-stream")
                        part.set_param('name', filename_rfc2047)    
                        part.add_header('Content-Disposition', 'attachment', filename=filename_rfc2047)                        
                        part.set_payload(fcontent)                       
                        Encoders.encode_base64(part)    
                        msgRoot.attach(part)
           
            try:
                print "message text............",msgText
                import smtplib
                smtp = smtplib.SMTP()
                smtp.connect('smtp.gmail.com',587)
                smtp.ehlo()
                smtp.starttls()
                smtp.login(user,password)
                smtp.sendmail(user, strTo, msgRoot.as_string())
                smtp.quit()
                log_obj.write(cr,uid,[each.id],{'state':'sent'})
                print "#####################    EMAIL SENT SUCCESSFULLY    #################"
            except:
                pass
            
        return True
    
  
class ir_mail_server(osv.osv):
    """Represents an SMTP server, able to send outgoing emails, with SSL and TLS capabilities."""
    _inherit = "ir.mail_server"
    _columns ={
               'user_ids':fields.many2many('res.users','ir_server_users_rel','user_id','server_id','Users')
               }  
 
class ir_attachment(osv.osv):    
    _inherit = 'ir.attachment'
       
       
    def onchange_datas_fname(self, cr, uid, ids, datas_fname):
        vals = {}
        print "running on change..............................",
        if not datas_fname:

            return vals
        print "datas fname...................",datas_fname
        vals['cid'] = '''<img src="cid:%s">''' %(datas_fname.replace(" ", "_").lower())
        vals['name']=datas_fname
        return {'value': vals,}
    
    
class change_mail_state(osv.osv_memory):
    _name="change.mail.state"
    
    def set_to_outgoing(self, cr, uid, ids, context=None):
        res={}
        act_ids = context.get('active_ids',[])
        logs_obj=self.pool.get('mail.logs')
        for act in act_ids:
            logs_obj.write(cr, uid, act, {'status':'outgoing'})
        print "-----------------",act_ids
        return res
        
        
    
    
    
    
    