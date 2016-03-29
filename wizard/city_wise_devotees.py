from openerp.osv import osv,fields
from openerp import _
from openerp.report import report_sxw
from datetime import datetime
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class citywise_devotees(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context=None):
        super(citywise_devotees,self).__init__(cr,uid,name,context=context)
        self.localcontext.update({'time':time,
                                  'get_data':self.get_data,
                                  'get_time':self.get_time,
                                  })
    def get_time(self):
        str_time = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        return str_time 
        
    def get_data(self,city_id,start,end):
        db = self.pool.db
        cr = db.cursor()
        
        if len(start)==10 and len(end)==10:
            start=datetime.strptime(start,'%Y-%m-%d')
            end=datetime.strptime(end,'%Y-%m-%d')
            
            cr.execute("select dev.name,city.name,dev.mobile1 from jkp_devotees as dev left join res_city as city on (dev.city_id=city.id) where dev.city_id='"+str(city_id)+"' and dev.today_date >='"+str(start)+"' and dev.today_date <= '"+str(end)+"' order by dev.name")
            data=cr.fetchall()
        else:
            cr.execute("select dev.name,city.name,dev.mobile1 from jkp_devotees as dev left join res_city as city on (dev.city_id=city.id) where dev.city_id='"+str(city_id)+"' order by dev.name")
            data=cr.fetchall()
        
        return data
        
report_sxw.report_sxw('report.citywise.devotees','city.wise.report','addons/jkp_devotees/wizard/citywise_devotees.rml',parser=citywise_devotees,header="external")

class city_wise_report(osv.osv_memory):
    _name="city.wise.report"
    
    _columns={
              'all_data':fields.boolean('All Devotees'),
              'from_date':fields.date('From (Creation Date)'),
              'to_date':fields.date('To (Creation Date)'),              
              'city_name':fields.many2one('res.city','Place Name',required=True),
              'devotee_details':fields.many2many('jkp.devotees','city_devotees_rel','devotee_city','city_devotee','Devotees List'),
              }
    _defaults={'all_data':True}
    
    
    def get_devotee_list(self,cr,uid,ids,context=None):
        res={}
        report_ids=[]
        data=self.browse(cr,uid,ids)
        from_date=data[0].from_date
        to_date=data[0].to_date
        name=data[0].city_name.name
        devotee_obj=self.pool.get('jkp.devotees')
        if from_date and to_date:
            report_ids=devotee_obj.search(cr,uid,[('today_date','>=' ,from_date),('today_date','<=' ,to_date),('dist_id','=',name)])
        else:
            report_ids=devotee_obj.search(cr,uid,[('dist_id','=',name)])
       
        self.write(cr,uid,ids,{'devotee_details':[(6,0,report_ids)]})
        report_obj = self.pool.get('ir.actions.report.xml')
        datas = {'ids' : ids}
        rpt_id =  report_obj.search(cr, uid, [('report_name','=','citywise.devotees')])[0]
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
    
   
