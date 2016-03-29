from openerp.osv import osv,fields
from datetime import datetime
class message_logs_delete(osv.osv):
    _name="message.logs.delete"
    _columns={
              'selected':fields.boolean('Selected'),
              'all':fields.boolean('All'),
              'from_date':fields.date('From Date'),
              'till_date':fields.date('Till Date'),
              }
    
    def message_delete(self, cr, uid, ids, context=None):
        res={}
        search_ids= []
        mail_obj = self.pool.get('devotees.logs')
        current_object = self.browse(cr, uid, ids)[0]
        start = current_object.from_date
        end   = current_object.till_date
        if current_object.selected:
            search_ids=context.get('active_ids',[])
            
        if current_object.all:
            search_ids= mail_obj.search(cr,uid,[('state2','=','Draft')])
            
        if start and end:
            search_ids = mail_obj.search(cr,uid,[('date_create','>=' ,start),('date_create','<=' ,end),('state2','=','Draft')])
        print "...................................",search_ids    
        if search_ids:
            mail_obj.unlink(cr, uid, search_ids)
        return True
    
    def message_cancel(self, cr, uid, ids, context=None):
        res={}
        search_ids = []
        mail_obj = self.pool.get('devotees.logs')
        current_object = self.browse(cr, uid, ids)[0]
        start = current_object.from_date
        end   = current_object.till_date
        if current_object.selected:
            search_ids=context.get('active_ids',[])
            
        if current_object.all:
            search_ids= mail_obj.search(cr,uid,[('state2','=','Draft')])
            
        if start and end:
            search_ids = mail_obj.search(cr,uid,[('date_create','>=' ,start),('date_create','<=' ,end),('state2','=','Draft')])

        if search_ids:
            for val in search_ids:
                if mail_obj.browse(cr,uid,val).state == 'Outgoing':
                    mail_obj.write(cr,uid,val,{'state':'Cancel'})
        return True
    
    def message_retry(self, cr, uid, ids, context=None):
        res={}
        search_ids = []
        date = datetime.now()
        mail_obj = self.pool.get('devotees.logs')
        current_object = self.browse(cr, uid, ids)[0]
        start = current_object.from_date
        end   = current_object.till_date
        if current_object.selected:
            search_ids=context.get('active_ids',[])
            
        if current_object.all:
            search_ids= mail_obj.search(cr,uid,[('state2','=','Draft')])
            
        if start and end:
            search_ids = mail_obj.search(cr,uid,[('date_create','>=' ,start),('date_create','<=' ,end),('state2','=','Draft')])

        if search_ids:
            for val in search_ids:
                if mail_obj.browse(cr,uid,val).state == 'Failed' or mail_obj.browse(cr,uid,val).state == 'Cancel' :
                    mail_obj.write(cr,uid,val,{'state':'Outgoing','schedule_date':date})
        return True
    
    
    
    
class mail_logs_delete(osv.osv):
    _name="mail.logs.delete"
    _columns={
              'selected':fields.boolean('Selected'),
              'all':fields.boolean('All'),
              'from_date':fields.date('From Date'),
              'till_date':fields.date('Till Date'),
              }
    
    def message_delete(self, cr, uid, ids, context=None):
        res={}
        search_ids= []
        mail_obj = self.pool.get('mail.logs')
        current_object = self.browse(cr, uid, ids)[0]
        start = current_object.from_date
        end   = current_object.till_date
        if current_object.selected:
            search_ids=context.get('active_ids',[])
            
        if current_object.all:
            search_ids= mail_obj.search(cr,uid,[('state2','=','Draft')])
            
        if start and end:
            search_ids = mail_obj.search(cr,uid,[('date_create','>=' ,start),('date_create','<=' ,end),('state2','=','Draft')])

        if search_ids:
            mail_obj.unlink(cr, uid, search_ids)
        return True
    
    def message_cancel(self, cr, uid, ids, context=None):
        res={}
        search_ids = []
        mail_obj = self.pool.get('mail.logs')
        current_object = self.browse(cr, uid, ids)[0]
        start = current_object.from_date
        end   = current_object.till_date
        if current_object.selected:
            search_ids=context.get('active_ids',[])
            
        if current_object.all:
            search_ids= mail_obj.search(cr,uid,[('state2','=','Draft')])
            
        if start and end:
            search_ids = mail_obj.search(cr,uid,[('date_create','>=' ,start),('date_create','<=' ,end),('state2','=','Draft')])

        if search_ids:
            for val in search_ids:
                if mail_obj.browse(cr,uid,val).state == 'outgoing':
                    mail_obj.write(cr,uid,val,{'state':'cancel'})
        return True
    
    def message_retry(self, cr, uid, ids, context=None):
        res={}
        search_ids = []
        date = datetime.now()
        mail_obj = self.pool.get('mail.logs')
        current_object = self.browse(cr, uid, ids)[0]
        start = current_object.from_date
        end   = current_object.till_date
        if current_object.selected:
            search_ids=context.get('active_ids',[])
            
        if current_object.all:
            search_ids= mail_obj.search(cr,uid,[('state2','=','Draft')])
            
        if start and end:
            search_ids = mail_obj.search(cr,uid,[('date_create','>=' ,start),('date_create','<=' ,end),('state2','=','Draft')])

        if search_ids:
            for val in search_ids:
                if mail_obj.browse(cr,uid,val).state == 'failed' or mail_obj.browse(cr,uid,val).state == 'cancel' :
                    mail_obj.write(cr,uid,val,{'state':'outgoing','schedule_date':date})
        return True
    
    
    