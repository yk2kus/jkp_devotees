from openerp.osv import osv, fields
from datetime import datetime

class jkp_events(osv.osv):
    
    def create(self,cr,uid,vals,context=None):
        user_obj = self.pool.get('res.users')
       
        if 'public' in vals:
            if vals['public']:
                vals['user_ids'] = [(6,0,[u for u in user_obj.search(cr, uid, [('active','=',True)])])]
            else:
                vals['user_ids'] = [(6,0,[uid])]
        id=super(jkp_events,self).create(cr,uid,vals,context)
        return id
    
    def write(self, cr, uid, ids, vals, context=None):
        user_obj = self.pool.get('res.users')
        if 'public' in vals:
            if vals['public']:
                vals['user_ids'] = [(6,0,[u for u in user_obj.search(cr, uid, [('active','=',True)])])]
            else:
                vals['user_ids'] = [(6,0,[uid])]
        res = super(jkp_events, self).write(cr, uid, ids, vals, context)
        return res
    
    _name="jkp.events"
    
    def _check_start_date(self, cr, uid, ids,context=None):
        obj=self.browse(cr, uid, ids)[0]
        today = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        start = datetime.strptime(obj.from_date, '%Y-%m-%d %H:%M:%S')
       
        if start < today:
            return False
        else:
            return True
        
    def _check_end_date(self, cr, uid, ids,context=None):
        obj=self.browse(cr, uid, ids)[0]
        
        start = datetime.strptime(obj.from_date, '%Y-%m-%d %H:%M:%S')
        end   = datetime.strptime(obj.to_date, '%Y-%m-%d %H:%M:%S')
        
        if end < start:
            return False
        else:
            return True
        
        
    _columns={'name':fields.char('JKPFestivals Name',required=True),
              'from_date':fields.datetime('From Date',required=True),
              'to_date':fields.datetime('Till Date',required=True),
              'user_ids':fields.many2many('res.users','rel_user_event','user_id','event_id','User',invisible=True),
              'user_id':fields.many2one('res.users','User',invisible=True),
              'public':fields.boolean('Public'),
              }
    _defaults={
               'public':False,    
               'user_id':lambda obj, cr, uid, cnt: uid,           
               }
    _constraints =  [
        (_check_start_date,"can not be smaller than today's date",['From date']),
        (_check_end_date,"can not be smaller than from date",['Till date'])
        ]