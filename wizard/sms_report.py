from openerp.osv import osv,fields
from openerp import _
from openerp.report import report_sxw
   
class sms_report(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context=None):
        super(sms_report,self).__init__(cr,uid,name,context=context)
        self.localcontext.update({'time':time})

report_sxw.report_sxw('report.sms.report','sms.log.report','addons/jkp_devotees/wizard/sms_report.rml') 
    

class sms_log_report(osv.osv_memory):
    _name="sms.log.report"
    
    _columns={
              
              'message_ids':fields.many2many('devotees.logs','message_log_rel','message_logs','logs_message','Message List'),
              'from_date':fields.date('From',required=True),
              'to_date':fields.date('To',required=True),
              }
    
    
    
    def get_message_list(self,cr,uid,ids,context=None):
        res={}
        data=self.browse(cr,uid,ids)
        from_date=data[0].from_date
        to_date=data[0].to_date
        msg_obj=self.pool.get('devotees.logs')
        report_ids=msg_obj.search(cr,uid,[('log_date','>=' ,from_date),('log_date','<=' ,to_date)])
        self.write(cr,uid,ids,{'message_ids':[(6,0,report_ids)]})
        report_obj = self.pool.get('ir.actions.report.xml')
        datas = {'ids' : ids}
        rpt_id =  report_obj.search(cr, uid, [('report_name','=','sms.report')])[0]
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
    
   
