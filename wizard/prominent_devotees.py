from openerp.osv import osv,fields
from openerp import _
from openerp.report import report_sxw
from datetime import datetime
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class prominent_devotees(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context=None):
        super(prominent_devotees,self).__init__(cr,uid,name,context=context)
        self.localcontext.update({'time':time,
                                  'get_data':self.get_data,
                                  'get_time':self.get_time,
                                  })
    def get_time(self):
        str_time = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        return str_time 
    
    def get_data(self,start,end):
        
        print start,end,len(start),len(end)
        if len(start)==10 and len(end)==10:
            start=datetime.strptime(start,'%Y-%m-%d')
            end=datetime.strptime(end,'%Y-%m-%d')
            self.cr.execute("select dev.name,city.name,dev.mobile1 from jkp_devotees as dev left join res_city as city on  \
             (dev.city_id=city.id) where dev.today_date >='"+str(start)+"' and dev.today_date <= '"+str(end)+"'\
              and dev.id in (select devotees_id from rel_devotees_category where category_id in (select id from jkp_category where name = 'Prominent') ) order by city.name,dev.name ")
            data=self.cr.fetchall()
        else:
            self.cr.execute("select dev.name,city.name,dev.mobile1 from jkp_devotees as dev left join \
            res_city as city on (dev.city_id=city.id) where  dev.id \
            in (select devotees_id from rel_devotees_category where category_id in \
            (select id from jkp_category where name = 'Prominent') ) order by city.name,dev.name ")
            data=self.cr.fetchall()
        print "data...............",data
        return data

report_sxw.report_sxw('report.prominent.devotees','prominent.wise.report','addons/jkp_devotees/wiazard/prominent_devotees.rml',parser=prominent_devotees) 
    

class prominent_wise_report(osv.osv_memory):
    _name="prominent.wise.report"
    
    _columns={'all_devotees':fields.boolean('All Devotees'),
              'devotee_details':fields.many2many('jkp.devotees','prominent_devotees_rel','devotee_prominent','prominent_devotee','Devotees List'),
              'from_date':fields.date('From (Creation Date)',),
              'to_date':fields.date('To (Creation Date)',),
              }
    _defaults={'all_devotees':True}
    
    
    
    def get_devotee_list(self,cr,uid,ids,context=None):
        res={}
        report_ids=[]
        data=self.browse(cr,uid,ids)
        from_date=data[0].from_date
        to_date=data[0].to_date
        print from_date
        print to_date
        devotee_obj=self.pool.get('jkp.devotees')
        categ_id =self.pool.get('jkp.category').search(cr,uid,( [('name','=','Prominent')]  ))
        print "category ids ids......................",categ_id
        
        if to_date and from_date:
            report_ids=devotee_obj.search(cr,uid,[('today_date','>=' ,from_date),('today_date','<=' ,to_date),('category_ids','in',categ_id)])
        else:
            report_ids=devotee_obj.search(cr,uid,[('category_ids','in',categ_id)])
        print "report Ids are ",report_ids
        self.write(cr,uid,ids,{'devotee_details':[(6,0,report_ids)]})
        report_obj = self.pool.get('ir.actions.report.xml')
        datas = {'ids' : ids}
        rpt_id =  report_obj.search(cr, uid, [('report_name','=','prominent.devotees')])[0]
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
    
   
