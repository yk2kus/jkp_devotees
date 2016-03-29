
from openerp.osv import osv,fields
import base64
import datetime
from openerp.tools import flatten 


class check_duplicates(osv.osv):
    _name="check.duplicates"
    _columns={
              'duplicate_devotee_ids':fields.many2many('jkp.devotees','devotee_duplicate_rel','duplicate_jkp','jkp_duplicate','Possible duplicate devotees',readonly=True),
              }
    def default_get(self, cr, uid, fields, context=None):
        print 
        res={}
        if not context:
            return res
        act_id = context.get('active_ids', [])
        res = super(check_duplicates, self).default_get(cr, uid, fields, context=context)
        if act_id:
            dev_search=self.pool.get('jkp.devotees')
            dev_obj=self.pool.get('jkp.devotees').browse(cr,uid,act_id)[0]
            dup_firstName  = dev_obj.first_name.title()
            dup_fatherName = dev_obj.f_name.title()
            dup_lastName   = dev_obj.last_name.title()
            dup_dob        = dev_obj.dob
            dup_ids1=dev_search.search(cr,uid,[('first_name','=',dup_firstName),('f_name','=',dup_fatherName),('state','=','Draft')])
            dup_ids2=dev_search.search(cr,uid,[('f_name','=',dup_fatherName),('dob','=',dup_dob),('state','=','Draft')])
            dup_ids3=dev_search.search(cr,uid,[('first_name','=',dup_firstName),('dob','=',dup_dob),('state','=','Draft')])
            dup_ids4=dev_search.search(cr,uid,[('last_name','=',dup_lastName),('f_name','=',dup_fatherName),('state','=','Draft')])
            dup_ids=list(set(dup_ids1 + dup_ids2 + dup_ids3 + dup_ids4))
            print dup_ids,act_id,dup_ids1,dup_ids2,dup_ids3,dup_ids4
            if act_id[0] in dup_ids:
                dup_ids.remove(act_id[0])
            res.update({'duplicate_devotee_ids':dup_ids})
            print dup_ids
            return res
        
        
    def match_found(self,cr,uid,ids,context=None):
        
        n=0
        sequence_code = self.pool.get('ir.sequence')
        search_id = sequence_code.search(cr ,uid, [('code','=','jkp.devotees')])
        sequence_prefix =sequence_code.browse(cr, uid, search_id[0]).prefix
        if sequence_prefix:
            n=len(sequence_prefix)
        print "n------------------------------",n
#        next_num =sequence_code.browse(cr, uid, search_id[0]).number_next
        
       
        model_id = self.pool.get('ir.model.data')
        jkp_obj = self.pool.get('jkp.devotees')
        act_id  = context.get('active_ids',[])
        dup_ids = self.browse(cr,uid,ids[0]).duplicate_devotee_ids
        if dup_ids:
            form_sequence = jkp_obj.browse(cr ,uid ,act_id[0]).sequence[n:].lstrip('0')
            code=self.pool.get('ir.sequence').get(cr,uid,'jkp.devotees')[n:].lstrip('0')
            if int(form_sequence)+1 ==int(code):
                print "  EQUAL.........."
                jkp_obj.write(cr,uid,act_id[0],{'state':'Confirmed'})
                sequence_code.write(cr,  uid, search_id,{'number_next':form_sequence})
                unlink_id=jkp_obj.unlink(cr, uid, act_id)
            else:
                print "UN..  EQUAL.........."
                unlink_id=jkp_obj.unlink(cr, uid, act_id)
            
        res = False
        try:
            res = model_id.get_object_reference(cr, uid, 'Devotees', 'action_devotees_form')[1]
        except ValueError:
            res = False
            
            
        return {
                'name':'Devotees',
                'view_type':'form',
                'view_id'  :res,
                'view_mode':'tree,form',
                'res_model':'jkp.devotees',
                'type':'ir.actions.act_window',
                'domain' :[('state','=','Draft'),('dormant','!=',True)],
                'context':{'search_default_state': 'Draft','search_default_dormant':False}
                }
                   