
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2011-2015 OpenERP4you  (http://openerp4you.in). 
#    All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details, but reseller should inform 
#    or take permission from OpenERP4you before resell..
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#    
##############################################################################





from openerp.osv import osv, fields
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare
import time
import re
from datetime import datetime
from openerp import _
from dateutil import parser
import datetime as dtm
from openerp import tools

class jkp_attachments(osv.osv):
    _name="jkp.attachments"
    
    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = obj.attachment
        return result
    
    _columns={'name':fields.char('Attachment Name',size=1000,required=True),
              'attachment':fields.binary('Attachment',required=True),
              'preview_attachment':fields.function(_get_image,type="binary",method=True)
#              # al: We keep shitty field names for backward compatibility with document
#              'attachment_datas': fields.function(_data_get, fnct_inv=_data_set, string='File Content', type="binary", nodrop=True),
              
              }

class res_country_state(osv.osv):
    _name="res.country.state"
    _inherit="res.country.state"
    _columns={
              'code':fields.char('State Code',size=3,invisible=True,required=False),
              }
    _order='name'
    _sql_constraints=[('unique_country_state','unique(country_id,name)',"State name should be unique in a country !"),
                      ]
    
    def default_get(self, cr, uid, fields, context=None):
        res={}
        if not context:
            return res
        con_id=context.get('country_id')
        print id,context
        res.update({'country_id':con_id})
        return res
    
    def create(self,cr,uid,vals,context=None):
        
        for key,values in vals.iteritems():
            
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                vals[key] = vals[key].strip()
                word_list =  vals[key].split(' ')
                name = ''
                for word in word_list:
                    if len(word) > 0:
                        name = name + ' ' + word[0].upper()+word[1:]
                vals[key] = name.strip()
        
        id=super(res_country_state,self).create(cr,uid,vals,context)
        message='Record Updated Successfully'
        return id
    
    def write(self, cr, uid, ids, vals, context=None):
        for key,values in vals.iteritems():
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                
                if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                    vals[key] = vals[key].strip()
                    word_list =  vals[key].split(' ')
                    name = ''
                    for word in word_list:
                        if len(word) > 0:
                            name = name + ' ' + word[0].upper()+word[1:]
                    vals[key] = name.strip()
        res = super(res_country_state, self).write(cr, uid, ids, vals, context)
        return res

class jkp_category(osv.osv):
    _name = 'jkp.category'
    
    def _check_name_unique(self, cr, uid, ids, context=None):
       name = None
       count = 0
       for each in self.browse(cr, uid, ids):
           name = each.name.lower().replace(' ','')
           print ".................name",name
       read_ids = self.read(cr, uid, self.search(cr, uid, []), ['name'])
       for rec in read_ids:
           if name == rec['name'].lower().replace(' ',''):
               count += 1
               if count > 1:
                   return False
       return True
   
    def _check_string(self,cr,uid,ids,context=None):
        for val in self.browse(cr,uid,ids):
            res={}
            str=''
            read_ids = self.read(cr, uid, ids, ['name'])
            for rec in read_ids:
               str=rec['name'] 
               print "------------",str
               if re.match("^-?[a-zA-Z ]+$", str) != None:
                   return True
    
    
    _columns = {
                'name':fields.char('Name',size=64,required=True),
                }
    
    _constraints =  [
       (_check_name_unique, 'name should be unique', ['Category']),
       (_check_string,'name should contain valid characters',['Category']),
   ]
    _order='name'
    
    def create(self,cr,uid,vals,context=None):
        for key,values in vals.iteritems():
            print "vals...................",vals
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                vals[key] = vals[key].strip()
                vals[key] = vals[key].title()
              
        id=super(jkp_category,self).create(cr,uid,vals,context)
        message='Record Updated Successfully'
        return id
    
    def write(self, cr, uid, ids, vals, context=None):
        for key,values in vals.iteritems():
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                
                if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                    vals[key] = vals[key].strip()
                    vals[key] = vals[key].title()
        res = super(jkp_category, self).write(cr, uid, ids, vals, context)
        return res
    

class Country(osv.osv):
    _name = 'res.country'
    _inherit="res.country"
    
    def _check_country_code(self, cr, uid, ids, context=None):
       name = None
       count = 0
       str="^-?[0-9]+$"
       obj=self.browse(cr, uid, ids)[0]
       code=obj.country_code
       if code and re.match(str, code) == None:
            return False
       return True
    
    _columns={'country_code':fields.char('Country Code',size=5),
              'code': fields.char('Country Code', size=2,required=False,invisible=True),
              'address_format': fields.text('Address Format',invisible=True)
              }
    _sql_constraints=[('unique_count_code','unique(country_code)',"Country Code must be unique !"),
                    ]
    _constraints=[ (_check_country_code,"is invalid ",['Country Code']),]
 
class jkp_devotees(osv.osv):
    _name="jkp.devotees"
#    _inherits =  {'res.partner':'partner_id'}
#    _table = 'jkp_devotees'
    
    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res={}
        for val in self.pool.get('jkp.devotees').browse(cr,uid,ids):
            first=val.first_name
            last=val.last_name
            c_name= first + ' ' +last
            res[val.id]=c_name
        return res
    
    
   
    def _check_land_code(self, cr, uid, ids, context=None):
      
       str="^-?[0-9]+$"
       obj=self.browse(cr, uid, ids)[0]
       ph=obj.land_code
       mobile_ctry_code = obj.m1_code
       land_ctry_code= obj.country_id.country_code
       
       if land_ctry_code and ph:
           if int(land_ctry_code)!= int(ph):
               raise osv.except_osv(_('Invalid Number'), _('Landline Country code is not valid'))
              
       
       if ph and re.match(str, ph) == None:
            return False
       return True
   
   
    def _check_land_std(self, cr, uid, ids, context=None):
      
       str="^-?[0-9]+$"
       obj=self.browse(cr, uid, ids)[0]
       ph=obj.land_std
       if ph and re.match(str, ph) == None:
            return False
       return True
   
    def _check_landline(self, cr, uid, ids, context=None):
      
       str="^-?[0-9]+$"
       obj=self.browse(cr, uid, ids)[0]
       ph=obj.landline
       if ph and re.match(str, ph) == None:
            return False
       return True
   
    def _check_mob1Code(self, cr, uid, ids, context=None):
      
       str="^-?[0-9]+$"
       obj=self.browse(cr, uid, ids)[0]
       ph=obj.m1_code
       ctry_code = obj.country_id.country_code
       eme_ctry_code =obj.eme_country_id.country_code
       if ctry_code and ph:
           if int(ctry_code) != int(ph):
               raise osv.except_osv(_('Invalid Number'), _('Mobile Country code is not valid'))
       if ph and re.match(str, ph) == None:
            return False
       return True
   
    def _check_mobile1(self, cr, uid, ids, context=None):
      
       str="^-?[0-9]+$"
       code=''
       obj=self.browse(cr, uid, ids)[0]
       cntry_name = obj.country_id.name
       ph=obj.mobile1
       if obj.m1_code:
           try:
               code=int(obj.m1_code)
           except:
               raise osv.except_osv(_('Invalid Number'), _('Mobile Country code is not valid'))
       if code and code==91 or cntry_name == 'India':
           if ph and len(ph)!= 10:
                   raise osv.except_osv(_('Invalid Mobile Number'), _('Mobile Number must contain 10 digits only'))
       elif code and code!=91:
           if ph and len(ph)> 15:
               raise osv.except_osv(_('Invalid Number'), _('Mobile Number can have maximum  15 digits only.'))
       if ph and re.match(str, ph) == None:
            return False
       return True
   
    
    def _check_mob2Code(self, cr, uid, ids, context=None):
      
       str="^-?[0-9]+$"
       obj=self.browse(cr, uid, ids)[0]
       ph=obj.m2_code
       if ph and re.match(str, ph) == None:
            return False
       return True
   
    def _check_mobile2(self, cr, uid, ids, context=None):
      
       str="^-?[0-9]+$"
       code=''
       obj=self.browse(cr, uid, ids)[0]
       ph=obj.mobile2
       cntry_name = obj.country_id.name
       if obj.m2_code:
           try:
               code=int(obj.m2_code)
           except:
               raise osv.except_osv(_('Invalid Number'), _('Alternate Mobile Country code is not valid'))
       if code and code==91:
           if ph and len(ph)!= 10:
                   raise osv.except_osv(_('Invalid Number'), _('Alternate Mobile Number must contain 10 digits only.'))
       elif code and code!=91:
           if ph and len(ph)> 15:
               raise osv.except_osv(_('Invalid Number'), _('Alternate Mobile Number can have maximum  15 digits only.'))
       if ph and re.match(str, ph) == None:
            return False
       return True
    def _check_eme_landline(self, cr, uid, ids, context=None):
      
       str="^-?[0-9]+$"
       obj=self.browse(cr, uid, ids)[0]
       ph=obj.eme_landline
       if ph and re.match(str, ph) == None:
            return False
       return True
   
    def _check_eme_mobile1(self, cr, uid, ids, context=None):
      
       str="^-?[0-9]+$"
       code=''
       obj=self.browse(cr, uid, ids)[0]
       ph=obj.eme_mobile1
       cntry_name = obj.eme_country_id.name
       ctry_code = obj.eme_country_id.country_code
       print "-----------------------------------",ctry_code ,"======================",obj.eme_m1_code
        
       if ctry_code and obj.eme_m1_code:
           if int(ctry_code)!= int(obj.eme_m1_code):
               raise osv.except_osv(_('Invalid Country Code'), _('Emergency Mobile Country code is not valid'))
       if obj.eme_m1_code:
           try:
               code=int(obj.eme_m1_code)
           except:
               raise osv.except_osv(_('Invalid Number'), _('Emergency Mobile Country code is not valid'))
       if code and code==91 or cntry_name == 'India':
           if ph and len(ph)!= 10:
                   raise osv.except_osv(_('Invalid Number'), _('Emergency Mobile Number must contain 10 digits only.'))
       elif code and code!=91:
           if ph and len(ph)> 15:
               raise osv.except_osv(_('Invalid Number'), _('Emergency Mobile Number can have maximum  15 digits only.'))
       if ph and re.match(str, ph) == None:
            return False
       return True
   
    def _check_eme_mobile2(self, cr, uid, ids, context=None):
      
       str="^-?[0-9]+$"
       code=''
       obj=self.browse(cr, uid, ids)[0]
       ph=obj.eme_mobile2
       cntry_name = obj.eme_country_id.name
       
       if obj.eme_m2_code:
           try:
               code=int(obj.eme_m2_code)
           except:
               raise osv.except_osv(_('Invalid Number'), _('Emergency alternate Mobile Country code is not valid'))
       if code and code==91:
           if ph and len(ph)!= 10:
                   raise osv.except_osv(_('Invalid Number'), _('Emergency Alternate Mobile Number must contain 10 digits only.'))
       elif code and code!=91:
           if ph and len(ph)> 15:
               raise osv.except_osv(_('Invalid Number'), _('Emergency Alternate Mobile Number can have maximum  15 digits only.'))
       if ph and re.match(str, ph) == None:
            return False
       return True
   
    def _check_since(self, cr, uid, ids, context=None):
        obj=self.browse(cr,uid,ids)[0]
        year_obj    =  obj.jkp_year
        if year_obj:        
            since =  year_obj.name
            dob_year =  obj.dob
            date= dtm.datetime.strptime(dob_year, '%Y-%m-%d')
            check_year=date.year
            if int(check_year) > int(since):
                return False
            else:
                return True
        return True
        
        
    def _check_pin_code(self,cr,uid,ids,context=None):
        str="^-?[0-9]+$"
        pin=''
        obj=self.browse(cr,uid,ids)[0]
        pin=obj.pin
        country=obj.country_id.name
        if country:
            if pin and country.lower() == 'india':
                if re.match("^-?[0-9]+$", pin) == None:
                    raise osv.except_osv(_('Invalid PIN'), _('Please enter only numbers in pin code !'))
                if len(pin)!= 6:
                    raise osv.except_osv(_('Invalid PIN'), _('PIN should be 6 digits only.'))
            else:
                return True
        return True
    def _check_emepin_code(self,cr,uid,ids,context=None):
        str="^-?[0-9]+$"
        pin=''
        obj=self.browse(cr,uid,ids)[0]
        pin=obj.eme_pin
        country=obj.eme_country_id.name
        if country:
            if pin  and country.lower()== 'india':
                if re.match("^-?[0-9]+$", pin) == None:
                    raise osv.except_osv(_('Invalid Emergency PIN'), _('Please enter only numbers in emergency pin code !'))
                if len(pin)!= 6:
                    raise osv.except_osv(_('Invalid Emergency PIN'), _('Emergency PIN should be 6 digits only.'))
            else:
                return True
        return True
    
    def _check_landline_number(self, cr, uid, ids, context=None):
      
       
       str="^-?[0-9/ ]+$"
       obj=self.browse(cr, uid, ids)[0]
       ph=obj.landline               
       if ph and re.match(str, ph) == None:
            return False
       return True
   
    def _check_eme_landline_number(self, cr, uid, ids, context=None):
       
       
       str="^-?[0-9/ ]+$"
       obj=self.browse(cr, uid, ids)[0]      
       e_ph=obj.eme_landline
       eme_ph = obj.eme_land_code
       ctry_code =obj.eme_country_id.country_code
       
       if eme_ph and ctry_code:
           if int(eme_ph)!= int(ctry_code):
               raise osv.except_osv(_('Invalid Country Code'), _('Emergency landline country code is not valid !'))
       if e_ph and re.match(str, e_ph) == None:
           return False 
       return True
          
    def _check_number(self, cr, uid, ids, context=None):
       name = None
       count = 0
       str="^-?[0-9]+$"
       obj=self.browse(cr, uid, ids)[0]
       
       m1=obj.mobile1
       m2=obj.mobile2
       
       
       e_m1=obj.eme_mobile1
       e_m2=obj.eme_mobile1    
              
      
       
       if m1 and re.match(str, m1) == None:
           return False
   
       if m2 and re.match(str, m2) == None:
           return False
   
         
       if e_m1 and re.match(str, e_m1) == None:
            return False
   
       if e_m2 and re.match(str, e_m2) == None:
           return False
       
       return True
   
        
    def _check_pan_no(self, cr, uid, ids, context=None):
        str="^-?[a-zA-Z ]+$"
        num="^-?[0-9]+$"
        obj=self.browse(cr, uid, ids)[0]
        pan=obj.pan_no
        if pan:
            if len(pan)!=10:
                raise osv.except_osv(_('Invalid PAN'), _('PAN should be 10 digited  code !'))
            str1 =pan[0:5] + pan[9]
            str2 =pan[5:9]
            if str1 and re.match(str,str1) == None:
                print "strring ...............",str1
                return False
            if pan and re.match(num, str2) == None: 
                print "number ==================", str2   
                return False    
        return True
        
       
        
    def _check_first_name(self, cr, uid, ids, context=None):
        str="^-?[a-zA-Z ]+$"
        obj=self.browse(cr, uid, ids)[0]
        name=obj.first_name    
        if name and re.match(str,name) == None:
            return False    
        return True
    def _check_last_name(self, cr, uid, ids, context=None):
        str="^-?[a-zA-Z ]+$"
        obj=self.browse(cr, uid, ids)[0]
        name=obj.last_name    
        if name and re.match(str,name) == None:
            return False    
        return True
    def _check_father_name(self, cr, uid, ids, context=None):
        str="^-?[a-zA-Z ]+$"
        obj=self.browse(cr, uid, ids)[0]
        name=obj.f_name    
        if name and re.match(str,name) == None:
            return False    
        return True
    
    def _check_dob(self,cr,uid,ids,context=None):
        obj=self.browse(cr, uid, ids)[0]
        date=obj.dob 
        date2=dtm.datetime.strptime('1902-01-01', '%Y-%m-%d')
        date= dtm.datetime.strptime(date, '%Y-%m-%d')
        date1= dtm.datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d')
        print date,date1
        if date > date1:
            return False
        if date < date2:
            raise osv.except_osv(_('Invalid Date'), _('Please enter a valid  Date !'))
        return True
    
            
    def _check_email(self,cr,uid,ids,context=None):
        obj=self.browse(cr, uid, ids)[0]
        mail=obj.email
        print "email..................",mail
        if mail and re.match("^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", mail) == None:
            return False
        else:
            return True
    def _check_email2(self,cr,uid,ids,context=None):
        obj=self.browse(cr, uid, ids)[0]
        mail=obj.email2
       
        if mail and re.match("^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", mail) == None:
            return False
        else:
            return True
        
    def _eme_check_email(self,cr,uid,ids,context=None):
        obj=self.browse(cr, uid, ids)[0]
        mail=obj.eme_email
       
        if mail and re.match("^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", mail) == None:
            return False
        else:
            return True
        
    def _eme_check_email2(self,cr,uid,ids,context=None):
        obj=self.browse(cr, uid, ids)[0]
        mail=obj.eme_email2
       
        if mail and re.match("^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", mail) == None:
            return False
        else:
            return True
        
    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
        return result
        
   
    _columns={
            'pan_no':fields.char('PAN',size=10),
            'reg_no':fields.char('Registration No',size=16),
            'reg_new':fields.integer('Registration No'),
            'dob':fields.date('DoB (dd.mm.yyyy)',required=True),
            'user_id':fields.many2one('res.users','User'),
            'sequence':fields.char('Form No',size=128,readonly=True),
            'today_date':fields.datetime('Creation Date',readonly=True),
            'name': fields.function(_name_get_fnc, type="char", string='Full Name',store=True),
            #'partner_id':fields.many2one('res.partner','Partner'),
            'last_name': fields.char('Last Name', size=64,required=True),
            'first_name': fields.char('First Name', size=64,required=True),
            'f_name':fields.char("Father's Name",size=128,required=True),
            'mother_tongue':fields.many2one('lang.known','Mother Tongue'),
            
            'lang_known':fields.many2many('lang.known','devotee_lang_rel','devotee_lang','lang_devotee','Languages Known'),
            'gender':fields.selection([('Male','Male'),('Female','Female')],'Gender',required=True),
            'profession':fields.many2one('profession.profession','Profession'),
            'prof_detail':fields.char('Work Details',size=264),
            'qualification_ids':fields.many2many('qualification','rel_devotees_qualification','devotees_id','qualification_id','Qualification',store=True),
            'jkp_year':fields.many2one('year.jkp','Associated with JKP Since'),
            'through':fields.selection([('Not Known','Not Known'),('Others','Others'),('Pracharak','Pracharak'),('Satsangee','Satsangee'),('TV Channel','TV Channel'),],'Associated Through'),
            'through_name':fields.char("Provide Details",size=128),
            'tv_name':fields.many2one('tv.tv','TV Channel Name'),
            'devotee_name':fields.many2one('jkp.devotees',"Devotee's Name"),
            'pracharak_name':fields.many2one('jkp.pracharak','Pracharak Name'),
            'devotee_family':fields.one2many('devotee.family','m2o_jkp','Z Family member '), 
            'family_permission':fields.selection([('Fully','Fully'),('Partially','Partially'),('Not At All','Not at all'),('Not Known','Not Known')],'Whether family members approve of your association with JKP (Optional)'),
            'street1': fields.text('Address'),
            'street2': fields.char('Z Street2 ', size=128),
            'pin': fields.char('PIN Code', change_default=True,  size=10),
            'tahsil': fields.many2one('res.tahsil','Tehsil/Taluka'),
            'city_id':fields.many2one('res.city','Place'),
            'dist_id':fields.many2one('res.district','District'),
            'post_id':fields.many2one('post.office','Post Office'),
            'state_id': fields.many2one("res.country.state", 'State', ),
            'country_id': fields.many2one('res.country', 'Country'),
            'email': fields.char('Email', size=240),
            'email2':fields.char('Alternate Email', size=240),
            'land_code':fields.char('Landline No',size=6,help="Landline Code must contain numbers only."),
            'land_std':fields.char('Std Code',size=6,help="STD Code must contain numbers only."),
            'landline': fields.char('Landline No (Search)', size=40,help="Landline number must contain numbers only."),
            'm1_code':fields.char('Mobile No',size=5),
            'mobile1': fields.char('Mobile No(Search)', size=20),
            'm2_code':fields.char('Alternate Mobile No',size=5),
            'mobile2': fields.char('Alternate Mobile No (Search)', size=20),
            'letter':fields.boolean('Letter'),
            'mail':fields.boolean('Email'),
            'sms':fields.boolean('SMS'),
            'contact_via':fields.char('Contact Through',size=128),
            'eme_name':fields.char('Name',size=128),
            'eme_rel':fields.char('Relation',size=64),
            'eme_rel_id':fields.many2one('jkp.relation','Relation Combo'),
            'eme_street1': fields.char('EME Address', size=128),
            'eme_street2': fields.char('Z EME Street2 ', size=128),
            'eme_pin': fields.char('EME PIN Code', change_default=True, size=10),
            'eme_tahsil': fields.many2one('res.tahsil','EME Tehsil/Taluka'),
            'eme_dist_id':fields.many2one('res.district','EME District'),
            'eme_post_id':fields.many2one('post.office','EME Post Office'),
            'eme_state_id': fields.many2one("res.country.state", 'EME State', domain="[('country_id','=',country_id)]"),
            'eme_country_id': fields.many2one('res.country', 'EME Country'),
            'eme_email': fields.char('EME Email', size=240),
            'eme_email2':fields.char('EME Alternate Email', size=240),
            'eme_land_code':fields.char('Landline No',size=6),
            'eme_land_std':fields.char('Eme Std Code',size=6),
            'eme_landline': fields.char('EME Landline No (Search)', size=40),
            'eme_m1_code':fields.char('EME Mobile No',size=5),
            'eme_mobile1': fields.char('EME Mobile No (Search )', size=35),
            'eme_m2_code':fields.char('EME Alternate Mobile No',size=4),
            'eme_mobile2': fields.char('EME Alternate Mobile No (Search EME)', size=34),
            'updated_on':fields.date('Updated On',readonly=True),
            'remark':fields.text('Remark'),
            'state':fields.selection([('Draft','Draft'),('Confirmed','Confirmed')],'Stages',invisible=True),
            'family_name':fields.related('devotee_family','default_name',type="char",relation='devotee.family',string="Family Member"),
            'log_ids':fields.one2many('devotees.logs','log_id','Z Message Log IDS ',),
            'mail_log_ids':fields.one2many('mail.logs','log_id','Z Mail Log IDS ',),
            'jkp_attachment_ids':fields.many2many('jkp.attachments','jkp_attachment_rel','jkp_id','attachment_id','Attachments'),
            'image': fields.binary("Image", help="This field holds the image used as image for the product, limited to 1024x1024px."),
            
            'category_ids':fields.many2many('jkp.category','rel_devotees_category','devotees_id','category_id','Category'),
            
            'marital': fields.selection([('Married', 'Married'),('Unmarried', 'Unmarried'),('Divorced', 'Divorced'),('Widowed', 'Widowed'),('Separated', 'Separated')], 'Marital Status'),
            'accommodation':fields.selection([('Yes','Yes'),('No','No')],'Accommodation Provided'),
            'mangarh':fields.char('Mangarh (Accom)',size=64),
            'vrindavan':fields.char('Vrindavan (Accom)',size=64),
            'barsana':fields.char('Barsana (Accom)',size=64),
            'other':fields.char('Other (Accom)',size=64),
            'dormant':fields.boolean('Mark As Dormant'),
            'notes':fields.text('Notes'),
            }
    
    _defaults={
               'dormant':False,
               'accommodation':'No',
               'today_date':lambda *a: time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
               'user_id':lambda obj, cr, uid, cnt: uid,
               'state':'Draft',
               'm1_code':'91',
               'm2_code':'91',
               'land_code':'91',
               'eme_land_code':'91',
               'eme_m1_code':'91',
               'eme_m2_code':'91',
               'sms':False,
               'mail':False,
               'letter':False,               
               }
    _order='id,name'
    
    _constraints =  [
        (_check_since,"should be greater than DoB",['Associated Since']),
        (_check_pan_no,"is invalid",['PAN']),
        (_check_landline_number, ' must contain only integer values', ['Landline No']),
        (_check_mob1Code, 'must contain only integer values', ['Mobile Country Code ']),
        (_check_mobile1, 'must contain only integer values', ['Mobile  Number ']),
        (_check_mob1Code, 'must contain only integer values', ['Alternate Mobile Country Code ']),
        (_check_mobile2, ' must contain only integer values', ['Alternate Mobile  Number']),
        (_check_land_code, ' must contain only integer values', ['Landline Country Code']),
        (_check_land_std, ' must contain only integer values', ['Landline STD Code']),
        (_check_eme_landline_number, ' must contain only integer values', ['Emergency Landline Number']),
        (_check_eme_mobile1, 'must contain only integer values', ['Emergency Mobile  Number ']),
        (_check_eme_mobile2, ' Number must contain only integer values', ['Emergency Alternate Mobile Number']),
        (_check_first_name, 'must contain only character and spaces', ['First Name ']),
        (_check_last_name, ' must contain only character and spaces', ['Last Name']),
        (_check_father_name, ' must contain only character and spaces', ['Father\'s Name']),
        (_check_dob,"should be smaller than today's date",["Date Of Birth"]),
        (_check_email,"is invalid ",['Email']),
        (_check_email2,"is invalid ",['Alternate Email']),
        (_eme_check_email,"is invalid ",['Emergency Email']),
        (_eme_check_email2,"is invalid ",['Emergency Alternate Email']),
        (_check_pin_code,"is invalid",['PIN code']),
        (_check_emepin_code,"is invalid",['Emergency PIN code']),
        
         ]

     
    _sql_constraints=[('reg_unique','unique(reg_no)',"Registration Numbers should be unique"),
                      ('seq_unique','unique(sequence)',"Serial Numbers should be unique"),
                      
#                      ('unique_name_fname','unique(first_name,f_name,dob)',"First Name and Father's name should be unique !"),
#                      ('unique_dob_fname','unique(f_name,dob)',"Father's name should be unique !"),
                      ]
    
    def restore_devotee(self,cr,uid,ids,context=None):
        self.write(cr,uid,ids,{'state':'Draft'})
        return True
    
    
    def copy(self, cr, uid, id, default=None, context=None):
        print "copy............................................................",default
        if default is None:
            default = {}
        if context is None:
            context = {}
        default = default.copy()
        default['image'] = ''
        
        return super(jkp_devotees, self).copy(cr, uid, id, default, context=context)

    
    def create(self,cr,uid,vals,context=None):
        code=self.pool.get('ir.sequence').get(cr,uid,'jkp.devotees'),
        lang=[]
        for key,values in vals.iteritems():
            if key == 'lang_known':
                continue
            if key == 'qualification_ids':
                continue
            if key == 'category_ids':
                continue
            if key == 'sms':
                continue
            if key == 'letter':
                continue
            if key == 'mail':
                continue
            if key == 'contact_via':
                continue
            if key in ['mother_tongue','profession','country_id','state_id','dist_id','post_id','tahsil','eme_country_id','eme_state_id','eme_dist_id','eme_tahsil',
                       'eme_post_id','pracharak_name','jkp_year','city_id','eme_rel_id']:
                continue
            if key == 'landline':
                if vals['landline']:
                        number = vals['landline'].replace(' ','')
                        number = number.replace('/',' / ')
                        vals.update({'landline':number})
                continue
            
            if key == 'eme_landline':
                if vals['eme_landline']:
                        number = vals['eme_landline'].replace(' ','')
                        number = number.replace('/',' / ')
                        vals.update({'eme_landline':number})
                continue
            
            if key == 'email':
                if vals['email']:
                        mail=vals['email'].lower()
                        vals.update({'email':mail})
                continue
            elif key == 'email2':
                if vals['email2']:
                        mail=vals['email2'].lower()
                        vals.update({'email2':mail})
                continue
            elif key == 'eme_email':
                if vals['eme_email']:
                        mail=vals['eme_email'].lower()
                        vals.update({'eme_email':mail})
                continue
            elif key == 'eme_email2':
                if vals['eme_email2']:
                        mail=vals['eme_email2'].lower()
                        vals.update({'eme_email2':mail})
                continue
            elif key == 'pan_no':
                if vals['pan_no']:
                        pan=vals['pan_no'].upper()
                        vals.update({'pan_no':pan})
                continue
            
            elif key == 'through':
                   if vals['through']=='TV Channel':
                       continue
            elif key == 'image':
                continue
            
            elif key == 'image_medium':
                continue
            word_list=''
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                    vals[key] = vals[key].strip()
                    if key not in ['street1','eme_street1','remark','prof_detail','notes','pin','eme_pin']:
                        
                        word_list =  vals[key].title()
                    if key not in ['remark','notes']:                
                        if word_list:
                            word_list=' '.join(word_list.split())
                        else:
                            word_list=' '.join(vals[key].split())
                    else:
                        word_list = vals[key]
               
            word = re.sub(r"(?P<punct>([,.?!]))\1{1,}", "\g<punct>", word_list)
            print word
            word=word.replace(" .",".")
            word=word.replace(",",", ")
            word=word.replace(" ,",",")  
            word=word.replace(",  ",", ")                  
            vals[key] = word
        vals['sequence']=code[0]
        id=super(jkp_devotees,self).create(cr,uid,vals,context)
        print context
        return id
  
    
    def write(self, cr, uid, ids, vals, context=None):
        lang=[]
        for key,values in vals.iteritems():
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                
                if key == 'landline':
                    if vals['landline']:
                            number = vals['landline'].replace(' ','')
                            number = number.replace('/',' / ')
                            vals.update({'landline':number})
                    continue
            
                if key == 'eme_landline':
                    if vals['eme_landline']:
                            number = vals['eme_landline'].replace(' ','')
                            number = number.replace('/',' / ')
                            vals.update({'eme_landline':number})
                    continue
                
                if key == 'email':
                    if vals['email']:
                        mail=vals['email'].lower()
                        vals.update({'email':mail})
                    continue
                elif key == 'email2':
                    if vals['email2']:
                        mail=vals['email2'].lower()
                        vals.update({'email2':mail})
                    continue
                elif key == 'eme_email':
                    if vals['eme_email']:
                        mail=vals['eme_email'].lower()
                        vals.update({'eme_email':mail})
                    continue
                elif key == 'eme_email2':
                    if vals['eme_email2']:
                        mail=vals['eme_email2'].lower()
                        vals.update({'eme_email2':mail})
                    continue
                elif key == 'pan_no':
                    if vals['pan_no']:
                            pan=vals['pan_no'].upper()
                            vals.update({'pan_no':pan})
            
                    continue
                elif key == 'through':
                   if vals['through']=='TV Channel':
                       continue
                     
                elif key == 'image':
                    continue
                
                elif key == 'image_medium':
                    continue
                word_list=''
                if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                    vals[key] = vals[key].strip()

                    if key not in ['street1','eme_street1','remark','prof_detail','notes','pin','eme_pin']:
                        word_list =  vals[key].title()
                    if key not in ['remark','notes']:                        
                        if word_list:
                            word_list=' '.join(word_list.split())
                        else:
                            print "else....list.....",key,"list.............",word_list
                            word_list=' '.join(vals[key].split())
                            print "word....list.....",key,"list.............",word_list
                    else:
                        word_list=vals[key]
               
                word = re.sub(r"(?P<punct>([,.?!]))\1{1,}", "\g<punct>", word_list)
             
                word=word.replace(" .",".")
                word=word.replace(",",", ")
                word=word.replace(" ,",",") 
                word=word.replace(",  ",", ")
                print "word...................................",word                   
                vals[key] = word
        vals['updated_on']=time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        
        res = super(jkp_devotees, self).write(cr, uid, ids, vals, context)
        return res
        
        
        
    def unlink(self, cr, uid, ids, context=None):
        stat = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for t in stat:
            if t['state'] in ('Draft'):
                self.write(cr,uid,ids,{'state':'Confirmed'})
            elif t['state'] in ('Confirmed'): 
                unlink_ids.append(t['id'])
        osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
        return True   
    
    def onchange_pin(self,cr,uid,ids,country,pin):
        res={}
        if not country:
            return res
        else:
            c_name=self.pool.get('res.country').browse(cr,uid,country).name
            
            if pin and c_name.lower()=='india':
                length=len(pin)
                if length != 6:
                    raise osv.except_osv(_('Invalid PIN'), _('Please enter a valid 6 digits pin code !'))
                if pin and re.match("^-?[0-9]+$", pin) == None:
                    raise osv.except_osv(_('Invalid PIN'), _('Please enter a valid  pin code !'))
        return res
            
    
    def onchange_country(self,cr,uid,ids,country):
        res={}
        if not country:
            return res
        else:
            code=self.pool.get('res.country').browse(cr,uid,country).country_code
            if code:
                res['value']={'land_code':code,'m1_code':code,'m2_code':code,'state_id':'','dist_id':'','tahsil':'','post_id':'','pin':''}
                return res
            else:
                res['value']={'land_code':None,'m1_code':None,'m2_code':None,'state_id':'','dist_id':'','tahsil':'','post_id':'','pin':''}
                return res
    
    def onchange_eme_country(self,cr,uid,ids,country):
        res={}
        if not country:
            return res
        else:
            code=self.pool.get('res.country').browse(cr,uid,country).country_code
            print "Running new code.................."
            if code:
                res['value']={'eme_land_code':code,'eme_m1_code':code,'eme_m2_code':code,'eme_state_id':'','eme_dist_id':'','eme_tahsil':'','eme_post_id':'','eme_pin':''}
                return res
            else:
                res['value']={'eme_land_code':None,'eme_m1_code':None,'eme_m2_code':None,'eme_state_id':'','eme_dist_id':'','eme_tahsil':'','eme_post_id':'','eme_pin':''}
                return res
    def onchange_state(self, cr, uid, ids, state):
        res={}
        if not state:
            return res
        else:
            res['value']={'dist_id':'','tahsil':'','post_id':'','pin':''}
            return res
            
    def onchange_emeState(self, cr, uid, ids,eme_state):
        res={}
        if not eme_state:
            return res
        else:
            res['value']={'eme_dist_id':'','eme_tahsil':'','eme_post_id':'','eme_pin':''}
            return res
    def onchange_dist(self, cr, uid, ids, dist):
        res={}
        if not dist:
            return res
        else:
            res['value']={'tahsil':'','post_id':'','pin':''}
            return res
        
    def onchange_emeDist(self, cr, uid, ids, eme_dist):
        res={}
        if not eme_dist:
            return res
        else:
            res['value']={'eme_tahsil':'','eme_post_id':'','eme_pin':''}
            return res
        
    
    def onchange_dob(self,cr,uid,ids,first,last,father,dob):
        print "==============================================================",dob
        res={}
        dup_ids=[]
        if not dob:
            return res
        warning = {
                    'title': _('Duplicacy Information !'),
                    'message': _('Matching records found please contact administrator !')
                    }
        
        dob=datetime.strptime(dob,'%Y-%m-%d')

        if dob > datetime.today():
            print "date is greater than today's date"
            raise osv.except_osv(_('Invalid Date Of Birth'), _('Please enter a valid Date'))
        
#        except:
        if first and father and dob and last:
            first=first.title()
            father=father.title()
            last=last.title()
            print first,father,last
            dev_search=self.pool.get('jkp.devotees')
            dup_ids1=dev_search.search(cr,uid,[('first_name','=',first),('f_name','=',father),('state','=','Draft')])
            dup_ids2=dev_search.search(cr,uid,[('f_name','=',father),('dob','=',dob),('state','=','Draft')])
            dup_ids3=dev_search.search(cr,uid,[('first_name','=',first),('dob','=',dob),('state','=','Draft')])
            dup_ids4=dev_search.search(cr,uid,[('f_name','=',father),('last_name','=',last),('state','=','Draft')])
            dup_ids=list(set(dup_ids1 + dup_ids2 + dup_ids3 + dup_ids4))
            if ids and ids[0] in dup_ids:
                dup_ids.remove(ids[0])
            print dup_ids
        if dup_ids:
            res={'warning':warning}
        
        return res
    
        
        
    def onchange_pan(self, cr, uid, ids, pan):
        res={}
        str="^-?[a-zA-Z ]+$"
        num="^-?[0-9]+$"
        if pan:
            if len(pan)!=10:
                raise osv.except_osv(_('Invalid PAN'), _('PAN should be 10 digited  code !'))
            str1 =pan[0:5] + pan[9]
            str2 =pan[5:9]
            if str1 and re.match(str,str1) == None:
                raise osv.except_osv(_('Invalid PAN'), _('1-5 and 10th digit must be alphabets'))
            if pan and re.match(num, str2) == None: 
                raise osv.except_osv(_('Invalid PAN'), _('6-9 digits must be integers !'))
            return res
            
    def onchange_string(self, cr, uid, ids, str):
        res={}
        if not str:
            str=''
            return res
        if re.match("^-?[a-zA-Z ]+$", str) != None:
            return res
        else:
            raise osv.except_osv(_('Invalid Characters'), _('Only alphabets and spaces are allowed.'))
        
    def check_string2(self,str):
        res={}
        if not str:
            str=''
            return res
        if re.match("^-?[a-zA-Z ]+$", str) != None:
            return res
        else:
            raise osv.except_osv(_('Invalid Characters'), _('Only alphabets and spaces are allowed.'))
        
    def onchange_values(self, cr, uid, ids, first, last, father, dob):
        res={}
        dup_ids =[]
        if first:
            self.check_string2(first)
        else:
            first=''
        if last:
            self.check_string2(last)
        else:
            last=''
        if father:
            self.check_string2(father)
        else:
            father=''
        warning = {
                    'title': _('Duplicacy Information !'),
                    'message': _('Matching records found please contact administrator !')
                    }
        
        if dob:
            dob=datetime.strptime(dob,'%Y-%m-%d')

        if first and father and dob and last:
            first=first.title()
            father=father.title()
            last=last.title()
            print first,father,last
            dev_search=self.pool.get('jkp.devotees')
            dup_ids1=dev_search.search(cr,uid,[('first_name','=',first),('f_name','=',father),('state','=','Draft')])
            dup_ids2=dev_search.search(cr,uid,[('f_name','=',father),('dob','=',dob),('state','=','Draft')])
            dup_ids3=dev_search.search(cr,uid,[('first_name','=',first),('dob','=',dob),('state','=','Draft')])
            dup_ids4=dev_search.search(cr,uid,[('f_name','=',father),('last_name','=',last),('state','=','Draft')])
            dup_ids=list(set(dup_ids1 + dup_ids2 + dup_ids3 + dup_ids4))
            if ids and ids[0] in dup_ids:
                dup_ids.remove(ids[0])
            print dup_ids
        if dup_ids:
            res={'warning':warning}
        
        return res
    

    
    
    def onchange_integer(self, cr, uid, ids, num):
        res={}
        if not num:
            num=''
            return res
        if re.match("^-?[0-9]+$", num) != None:
            return res
        else:
            raise osv.except_osv(_('Invalid Number'), _('Please enter a valid Number'))
        
    def onchange_landline(self, cr, uid, ids, num):
        res={}
        if not num:
            num=''
            return res
        if re.match("^-?[0-9/ ]+$", num) != None:
            return res
        else:
            raise osv.except_osv(_('Invalid Number'), _('Please enter a valid Number'))
    
    
    
    def onchange_mobile_no(self, cr, uid, ids,code, num):
        res={}
       
        if not num:
            num=''
            return res
        if re.match("^-?[0-9]+$", num) != None:
            if int(code)== 91 :
                if len(num)!= 10:
                    raise osv.except_osv(_('Invalid Number'), _('Please enter a 10 digits number'))
                else:
                    return res
            else:
                return res
        else:
            raise osv.except_osv(_('Invalid Number'), _('Please enter a valid Number'))
    
                    
         
    
    def onchange_email(self, cr, uid, ids, email):
        res={}
        if not email:
            email=''
            return res
        if re.match("^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-z0-9-]+)*(\.[a-zA-Z]{2,4})$", email) != None:
            return res
        else:
            raise osv.except_osv(_('Invalid Email'), _('Please enter a valid email address'))
        
    
    
    
    
    def onchange_post(self,cr,uid,ids,post,context=None):
        res={}
        if not post:
             res['value']={'pin':False}
             return res
        pi=self.pool.get('post.office').browse(cr,uid,post,context=context).code
        res['value']={'pin':pi}
        return res
    def onchange_emepost(self,cr,uid,ids,post,context=None):
        res={}
        if not post:
             res['value']={'eme_pin':False}
             return res
        pi=self.pool.get('post.office').browse(cr,uid,post,context=context).code
        res['value']={'eme_pin':pi}
        return res

class jkp_relation(osv.osv):
    _name="jkp.relation"

    def _check_name_unique(self, cr, uid, ids, context=None):
       name = None
       count = 0
       for each in self.browse(cr, uid, ids):
           name = each.name.lower().replace(' ','')
           print ".................name",name
       read_ids = self.read(cr, uid, self.search(cr, uid, []), ['name'])
       for rec in read_ids:
           if name == rec['name'].lower().replace(' ',''):
               count += 1
               if count > 1:
                   return False
       return True
   
    def _check_string(self,cr,uid,ids,context=None):
        for val in self.browse(cr,uid,ids):
            res={}
            str=''
            read_ids = self.read(cr, uid, ids, ['name'])
            for rec in read_ids:
               str=rec['name'] 
               print "------------",str
               if re.match("^-?[a-zA-Z ]+$", str) != None:
                   return True
    
    _columns={
              'name':fields.char('Name',size=30,required=True),
              }
    _order = 'name'
    
    _constraints =  [
       (_check_name_unique, 'name should be unique', ['Relation']),
       (_check_string,'name should contain valid characters',['Relation']),
   ]
    
    def create(self,cr,uid,vals,context=None):
        for key,values in vals.iteritems():
            print "vals...................",vals
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                vals[key] = vals[key].strip()
                vals[key] = vals[key].title()
              
        id=super(jkp_relation,self).create(cr,uid,vals,context)
        message='Record Updated Successfully'
        return id
    
    def write(self, cr, uid, ids, vals, context=None):
        for key,values in vals.iteritems():
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                
                if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                    vals[key] = vals[key].strip()
                    vals[key] = vals[key].title()
        res = super(jkp_relation, self).write(cr, uid, ids, vals, context)
        return res



    
    
class lang_known(osv.osv):
    _name="lang.known"

    def _check_name_unique(self, cr, uid, ids, context=None):
       name = None
       count = 0
       for each in self.browse(cr, uid, ids):
           name = each.name.lower().replace(' ','')
       read_ids = self.read(cr, uid, self.search(cr, uid, []), ['name'])
       for rec in read_ids:
           if name == rec['name'].lower().replace(' ',''):
               count += 1
               if count > 1:
                   return False
       return True
   
    def _check_string(self,cr,uid,ids,context=None):
        for val in self.browse(cr,uid,ids):
            res={}
            str=''
            read_ids = self.read(cr, uid, ids, ['name'])
            for rec in read_ids:
               str=rec['name'] 
               if re.match("^-?[a-zA-Z ]+$", str) != None:
                   return True
    
    _columns={
              'name':fields.char('Name',size=16,required=True),
              }
    _order = 'name'
    
    _constraints =  [
       (_check_name_unique, 'Language should be unique', ['name']),
       (_check_string,'should contain valid characters',['Language']),
   ]
    
    def create(self,cr,uid,vals,context=None):
        for key,values in vals.iteritems():
            
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                vals[key] = vals[key].strip()
                word_list =  vals[key].split(' ')
                name = ''
                for word in word_list:
                    if len(word) > 0:
                        name = name + ' ' + word[0].upper()+word[1:]
                vals[key] = name.strip()
        id=super(lang_known,self).create(cr,uid,vals,context)
        message='Record Updated Successfully'
        return id
    
    def write(self, cr, uid, ids, vals, context=None):
        for key,values in vals.iteritems():
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                
                if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                    vals[key] = vals[key].strip()
                    word_list =  vals[key].split(' ')
                    name = ''
                    for word in word_list:
                        if len(word) > 0:
                            name = name + ' ' + word[0].upper()+word[1:]
                    vals[key] = name.strip()
        res = super(lang_known, self).write(cr, uid, ids, vals, context)
        return res
    
class profession_profession(osv.osv):
    _name="profession.profession"
    
    def _check_name_unique(self, cr, uid, ids, context=None):
       name = None
       count = 0
       for each in self.browse(cr, uid, ids):
           name = each.name.lower().replace(' ','')
       read_ids = self.read(cr, uid, self.search(cr, uid, []), ['name'])
       for rec in read_ids:
           if name == rec['name'].lower().replace(' ',''):
               count += 1
               if count > 1:
                   return False
       return True
   
    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args=[]
        if not context:
            context={}
        if name:
            # Be sure name_search is symetric to name_get
            name = name + '%'
            
            ids = self.search(cr, uid,  [('name', '=ilike', name + '%')] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
            
        return self.name_get(cr, uid, ids, context)

    def _check_string(self,cr,uid,ids,context=None):
        for val in self.browse(cr,uid,ids):
            res={}
            str=''
            read_ids = self.read(cr, uid, ids, ['name'])
            for rec in read_ids:
               str=rec['name'] 
               print "...........",str
               if re.match("^-?[a-zA-Z ]+$", str) != None:
                   return True
   
    _columns={
              'name':fields.char('Profession',size=60,required=True),
              }
    _order='name'
    
    _constraints =  [
        (_check_name_unique, 'Name should be unique', ['Profession']),
        (_check_string,'should contain valid characters',['Profession']),
   ]
    
    def create(self,cr,uid,vals,context=None):
        
        for key,values in vals.iteritems():
            
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                vals[key] = vals[key].strip()
                word_list =  vals[key].split(' ')
                name = ''
                for word in word_list:
                    if len(word) > 0:
                        name = name + ' ' + word[0].upper()+word[1:]
                vals[key] = name.strip()
        id=super(profession_profession,self).create(cr,uid,vals,context)
        message='Record Updated Successfully'
        return id
    
    def write(self, cr, uid, ids, vals, context=None):
        for key,values in vals.iteritems():
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                
                if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                    vals[key] = vals[key].strip()
                    word_list =  vals[key].split(' ')
                    name = ''
                    for word in word_list:
                        if len(word) > 0:
                            name = name + ' ' + word[0].upper()+word[1:]
                    vals[key] = name.strip()
        res = super(profession_profession, self).write(cr, uid, ids, vals, context)
        return res

class tv_tv(osv.osv):
    _name="tv.tv"
    
    def _check_name_unique(self, cr, uid, ids, context=None):
       name = None
       count = 0
       for each in self.browse(cr, uid, ids):
           name = each.name.lower().replace(' ','')
       read_ids = self.read(cr, uid, self.search(cr, uid, []), ['name'])
       for rec in read_ids:
           if name == rec['name'].lower().replace(' ',''):
               count += 1
               if count > 1:
                   return False
       return True
    
    _columns={
              'name':fields.char('TV Channel Name',size=232,required=True),
              }
    _order='name'
    
    _constraints =  [
       (_check_name_unique, 'Name should be unique', ['name']),
   ]
    
    def create(self,cr,uid,vals,context=None):
        
        for key,values in vals.iteritems():            
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                vals[key] = vals[key].strip()
                word_list =  vals[key].split(' ')
                name = ''
                for word in word_list:
                    if len(word) > 0:
                        name = name + ' ' + word[0].upper()+word[1:]
                vals[key] = name.strip()
        id=super(tv_tv,self).create(cr,uid,vals,context)
        return id
    
    def write(self, cr, uid, ids, vals, context=None):
        for key,values in vals.iteritems():
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                
                if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                    vals[key] = vals[key].strip()
                    word_list =  vals[key].split(' ')
                    name = ''
                    for word in word_list:
                        if len(word) > 0:
                            name = name + ' ' + word[0].upper()+word[1:]
                    vals[key] = name.strip()
        res = super(tv_tv, self).write(cr, uid, ids, vals, context)
        return res
    
    
    
    
class res_district(osv.osv):
    _name="res.district"
    
    def _check_string(self,cr,uid,ids,context=None):
        for val in self.browse(cr,uid,ids):
            res={}
            str=''
            read_ids = self.read(cr, uid, ids, ['name'])
            for rec in read_ids:
               str=rec['name'] 
               print "------------",str
               if re.match("^-?[a-zA-Z ]+$", str) != None:
                   return True
               
               
    def _check_name_unique(self, cr, uid, ids, context=None):
       name = None
       count = 0
       for each in self.browse(cr, uid, ids):
           name = each.name.lower().replace(' ','')
       read_ids = self.read(cr, uid, self.search(cr, uid, []), ['name'])
       for rec in read_ids:
           if name == rec['name'].lower().replace(' ',''):
               count += 1
               if count > 1:
                   return False
       return True
    
    _columns={
              'state_id':fields.many2one('res.country.state','State',required=True,ondelete="cascade"),
              'name':fields.char('District',size=232,required=True),
              }
    _order='name'
    
    _constraints =  [
                     (_check_string, 'name should contain valid characters', ['District']),
#       (_check_name_unique, 'name should be unique', ['District']),
  ]    
    _sql_constraints=[('unique_state_dist','unique(state_id,name)',"District name should be unique in a State !"),
                      ]
    def default_get(self, cr, uid, fields, context=None):
        res={}
        if not context:
            return res
        stat_id=context.get('state_id')
        print stat_id
        res.update({'state_id':stat_id})
        return res
    
    def create(self,cr,uid,vals,context=None):
        for key,values in vals.iteritems():
            
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                vals[key] = vals[key].strip()
                word_list =  vals[key].split(' ')
                name = ''
                for word in word_list:
                    if len(word) > 0:
                        name = name + ' ' + word[0].upper()+word[1:]
                vals[key] = name.strip()
        id=super(res_district,self).create(cr,uid,vals,context)
        return id
    
    def write(self, cr, uid, ids, vals, context=None):
        for key,values in vals.iteritems():
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                
                if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                    vals[key] = vals[key].strip()
                    word_list =  vals[key].split(' ')
                    name = ''
                    for word in word_list:
                        if len(word) > 0:
                            name = name + ' ' + word[0].upper()+word[1:]
                    vals[key] = name.strip()
        res = super(res_district, self).write(cr, uid, ids, vals, context)
        return res
    
    
class res_tahsil(osv.osv):
    _name="res.tahsil"
    
    def _check_name_unique(self, cr, uid, ids, context=None):
       name = None
       count = 0
       for each in self.browse(cr, uid, ids):
           name = each.name.lower().replace(' ','')
       read_ids = self.read(cr, uid, self.search(cr, uid, []), ['name'])
       for rec in read_ids:
           if name == rec['name'].lower().replace(' ',''):
               count += 1
               if count > 1:
                   return False
       return True
   
    def _check_string(self,cr,uid,ids,context=None):
        for val in self.browse(cr,uid,ids):
            res={}
            str=''
            read_ids = self.read(cr, uid, ids, ['name'])
            for rec in read_ids:
               str=rec['name'] 
               print "------------",str
               if re.match("^-?[a-zA-Z ]+$", str) != None:
                   return True

    
    _columns={
              'dist_id':fields.many2one('res.district','District',required=True,ondelete="cascade"),
              'name':fields.char('Tehsil',size=232,required=True),
              }
    _order='name'
    _sql_constraints=[('unique_tahsil_dist','unique(dist_id,name)',"Tahsil name should be unique in a District !"),
                      ]
    
    _constraints =  [
       (_check_string,'name should contain valid characters',['Tehsil']),
   ]    
    
    def default_get(self, cr, uid, fields, context=None):
        res={}
        if not context:
            return res
        distt_id=context.get('dist_id')
        print distt_id
        res.update({'dist_id':distt_id})
        return res
    
    def create(self,cr,uid,vals,context=None):
        for key,values in vals.iteritems():
            
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                vals[key] = vals[key].strip()
                word_list =  vals[key].split(' ')
                name = ''
                for word in word_list:
                    if len(word) > 0:
                        name = name + ' ' + word[0].upper()+word[1:]
                vals[key] = name.strip()
        id=super(res_tahsil,self).create(cr,uid,vals,context)
        return id
    
    def write(self, cr, uid, ids, vals, context=None):
        for key,values in vals.iteritems():
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                
                if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                    vals[key] = vals[key].strip()
                    word_list =  vals[key].split(' ')
                    name = ''
                    for word in word_list:
                        if len(word) > 0:
                            name = name + ' ' + word[0].upper()+word[1:]
                    vals[key] = name.strip()
        res = super(res_tahsil, self).write(cr, uid, ids, vals, context)
        return res
    
class res_city(osv.osv):
    _name="res.city"
    
    def _check_name_unique(self, cr, uid, ids, context=None):
       name = None
       count = 0
       for each in self.browse(cr, uid, ids):
           name = each.name.lower().replace(' ','')
       read_ids = self.read(cr, uid, self.search(cr, uid, []), ['name'])
       for rec in read_ids:
           if name == rec['name'].lower().replace(' ',''):
               count += 1
               if count > 1:
                   return False
       return True
   
   
    def _check_string(self,cr,uid,ids,context=None):
        for val in self.browse(cr,uid,ids):
            res={}
            str=''
            read_ids = self.read(cr, uid, ids, ['name'])
            for rec in read_ids:
               str=rec['name'] 
               print "------------",str
               if re.match("^-?[a-zA-Z ]+$", str) != None:
                   return True
    
    
    _columns={
              
              'name':fields.char('Place',size=232,required=True),
              }
    _order='name'    
    
    _constraints =  [
        (_check_string,'name should contain valid characters',['Place']),
       (_check_name_unique, 'name should be unique', ['Place']),
   ]    
    
     
    def create(self,cr,uid,vals,context=None):
        for key,values in vals.iteritems():
            
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                vals[key] = vals[key].strip()
                word_list =  vals[key].split(' ')
                name = ''
                for word in word_list:
                    if len(word) > 0:
                        name = name + ' ' + word[0].upper()+word[1:]
                vals[key] = name.strip()
        id=super(res_city,self).create(cr,uid,vals,context)
        return id
    
    def write(self, cr, uid, ids, vals, context=None):
        for key,values in vals.iteritems():
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                
                if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                    vals[key] = vals[key].strip()
                    word_list =  vals[key].split(' ')
                    name = ''
                    for word in word_list:
                        if len(word) > 0:
                            name = name + ' ' + word[0].upper()+word[1:]
                    vals[key] = name.strip()
        res = super(res_city, self).write(cr, uid, ids, vals, context)
        return res
    
    
class post_office(osv.osv):
    _name="post.office"
    
    def _check_string(self,cr,uid,ids,context=None):
        for val in self.browse(cr,uid,ids):
            res={}
            str=''
            read_ids = self.read(cr, uid, ids, ['name'])
            for rec in read_ids:
               str=rec['name'] 
               print "------------",str
               if re.match("^-?[a-zA-Z0-9-. ]+$", str) != None:
                   return True
               
    _columns={
              'name':fields.char('Post Office',size=64,required=True),
#              'code':fields.integer('PIN Code',required=True),
              'code':fields.char('PIN Code',size=10),
              'distt_id':fields.many2one('res.district','District',required=True,ondelete="cascade")
              }
    _order = 'name'
    
    _constraints=[
           (_check_string,'name should contain valid characters',['Post Office']),
   ]
    _sql_constraints=[('unique_postOffice_dist','unique(distt_id,name)',"Post office name should be unique in a district !"),
                      ]
#    _sql_constraints=[('unique_pin_number','unique (code)','Post Office must have uniqe PIN Code !.'),
#                      ]

    def default_get(self, cr, uid, fields, context=None):
        res={}
        if not context:
            return res
        distt_id=context.get('distt_id')
        print distt_id
        res.update({'distt_id':distt_id})
        return res

    def create(self,cr,uid,vals,context=None):
       
        for key,values in vals.iteritems():
            
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                vals[key] = vals[key].strip()
                word_list =  vals[key].split(' ')
                name = ''
                for word in word_list:
                    if len(word) > 0:
                        name = name + ' ' + word[0].upper()+word[1:]
                vals[key] = name.strip()
       
        id=super(post_office,self).create(cr,uid,vals,context)
        return id
    
    def write(self, cr, uid, ids, vals, context=None):
        for key,values in vals.iteritems():
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                
                if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                    vals[key] = vals[key].strip()
                    word_list =  vals[key].split(' ')
                    name = ''
                    for word in word_list:
                        if len(word) > 0:
                            name = name + ' ' + word[0].upper()+word[1:]
                    vals[key] = name.strip()
        res = super(post_office, self).write(cr, uid, ids, vals, context)
        return res

    
class year_jkp(osv.osv):
    _name="year.jkp"
    
    def _check_year(self, cr, uid, ids, context=None):
       str="^-?[0-9]+$"
       obj=self.browse(cr, uid, ids)[0]
       year=obj.name
       print year,len(year)
       if re.match(str, year) != None:      
           if len(year)!=4:
               return False
               if ph and re.match(str, year) != None:
                    return False
           return True
       else:
            raise osv.except_osv(_('Invalid Number'), _('Please enter a valid Number'))
    _columns={
              'name':fields.char('Year New',size=4,required=True),}
    _sql_constraints=[('unique_jkp_year','unique(name)',"Year should be unique  !"),
                      ]
    _constraints =  [
           (_check_year,'Please enter year in four digits and numbers only.',['Invalid Year']),
   ]
    
class devotee_family(osv.osv):
    _name="devotee.family"
    
    def _check_name(self, cr, uid, ids, context=None):
        str="^-?[a-zA-Z ]+$"
        obj=self.browse(cr, uid, ids)[0]
        name=obj.default_name    
        if name and re.match(str,name) == None:
            return False    
        return True
    
    def _check_rel(self, cr, uid, ids, context=None):
        str="^-?[a-zA-Z ]+$"
        obj=self.browse(cr, uid, ids)[0]
        name=obj.relation    
        if name and re.match(str,name) == None:
            return False    
        return True
    
    def _check_age(self, cr, uid, ids, context=None):
        str="^-?[0-9]+$"
        obj=self.browse(cr, uid, ids)[0]
        name=obj.age2   
        if int(name)<0 or int(name)>200:
            return False 
        if name and re.match(str,name) == None:
            return False    
        return True
    

    def _calc_age(self, cr, uid, ids, prop, unknow_none, context=None):
        res={}
        for val in self.browse(cr,uid,ids):
            today=val.today_date
            age =int(val.age2)
            dt = parser.parse(today)
            diff= datetime.today().year - dt.year
            print "====age=====",age,"==diff=====",diff
            if age==0:
                total_age=0
            else:
                total_age=diff+age
            
            res[val.id]=total_age        
        return res
    
    
    
    _columns={'today_date':fields.date('Today Date'),
              'devotee_name':fields.many2one('jkp.devotees','Name',ondelete="cascade"),
              'default_name':fields.char('Name',size=264,required=True),
              'age2':fields.char('Age',size=3),
              'relation':fields.char('Relation',size=32),
              'family_relation':fields.many2one('jkp.relation','Relation'),
              'dev_profession':fields.many2one('profession.profession','Profession'),
              'm2o_jkp':fields.many2one('jkp.devotees','Devotee',ondelete="cascade"),
              'actual_age':fields.function(_calc_age,type="char", string='Today Age',),
              }
    _defaults={'today_date':lambda *a: time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),}
    _constraints =  [
                     
       (_check_name, 'must contain valid characters', ['Name']),
       (_check_rel, ' must contain valid characters', ['Relation']),
       (_check_age, ' must contain valid Value', ['Age']),
   ]

       
    
    def onchange_age(self, cr, uid, ids, age):
        res={}
        if not age:
            return res
        if re.match("^-?[0-9]+$", age) != None:
            return res
        else:
            raise osv.except_osv(_('Invalid Age'), _('Please enter integers only'))

    def onchange_name(self, cr, uid, ids, str):
        res={}
        if not str:
            str=''
            return res
        if re.match("^-?[a-zA-Z ]+$", str) != None:
            return res
        else:
            raise osv.except_osv(_('Invalid Name'), _('Please enter  valid characters in Name'))
    
    def onchange_rel(self, cr, uid, ids, str):
        print "GOT CALLED REL-----------------------------==============="
        res={}
        if not str:
            str=''
            return res
        if re.match("^-?[a-zA-Z ]+$", str) != None:
            return res
        else:
            raise osv.except_osv(_('Invalid Relation'), _('Please enter  valid characters in Relation'))
    

    def onchange_devotee(self,cr,uid,ids,devotee):
        res={}
        FMT="%Y-%m-%d"
        rel=''
        now_age=0
        if not devotee:
            return res
        part=self.pool.get('jkp.devotees').browse(cr,uid,devotee)
        dob=part.dob
        if dob:
            print "dob",dob
            dob= datetime.strptime(dob, '%Y-%m-%d')
            date = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
            tdelta =  date - dob
            now_age=tdelta.days/365
        name=part.name    
        prof=part.profession.id
        res['value']={'age':now_age,'default_name':name,'dev_profession':prof}
        return res
    
    
    def create(self,cr,uid,vals,context=None):
       
        for key,values in vals.iteritems():
            
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                vals[key] = vals[key].strip()
                word_list =  vals[key].split(' ')
                name = ''
                for word in word_list:
                    if len(word) > 0:
                        name = name + ' ' + word[0].upper()+word[1:].lower()
                vals[key] = name.strip()
       
        id=super(devotee_family,self).create(cr,uid,vals,context)
        return id
    
    def write(self, cr, uid, ids, vals, context=None):
        for key,values in vals.iteritems():
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                
                if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                    vals[key] = vals[key].strip()
                    word_list =  vals[key].split(' ')
                    name = ''
                    for word in word_list:
                        if len(word) > 0:
                            name = name + ' ' + word[0].upper()+word[1:].lower()
                    vals[key] = name.strip()
        res = super(devotee_family, self).write(cr, uid, ids, vals, context)
        return res
    
class qualification(osv.osv):
    _name="qualification"
    
    def _check_name_unique(self, cr, uid, ids, context=None):
       name = None
       count = 0
       for each in self.browse(cr, uid, ids):
           name = each.name.lower().replace(' ','')
       read_ids = self.read(cr, uid, self.search(cr, uid, []), ['name'])
       for rec in read_ids:
           if name == rec['name'].lower().replace(' ',''):
               count += 1
               if count > 1:
                   return False
       return True
    
    
    _columns={'name':fields.char('Name',size=64,required=True)}
    _sql_constraints=[('unique_quali_name','unique(name)',"Qulification name should be unique !"),
                      ]
    _order='name'
   
#    _constraints =  [
#       (_check_name_unique, 'name should be unique', ['Qualification']),
#   ]
    
    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args=[]
        if not context:
            context={}
        if name:
            # Be sure name_search is symetric to name_get
            name = name + '%'
            print "name for search is .............",name
            ids = self.search(cr, uid,  [('name', '=ilike', name + '%')] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
            
        return self.name_get(cr, uid, ids, context)
    



class jkp_pracharak(osv.osv):
    _name="jkp.pracharak"
    
    def _check_string(self,cr,uid,ids,context=None):
        for val in self.browse(cr,uid,ids):
            res={}
            str=''
            read_ids = self.read(cr, uid, ids, ['name'])
            for rec in read_ids:
               str=rec['name'] 
               print "------------",str
               if re.match("^-?[a-zA-Z ]+$", str) != None:
                   return True
    
    _columns={'name':fields.char('Name',size=168,required=True)}
    
    _constraints =  [
        (_check_string,'name should contain valid characters',['Pracharak']),]

    _sql_constraints=[('unique_jkp_pracharak','unique(name)',"Pracharak name should be unique  !"),]
    _order='name'
    
    def create(self,cr,uid,vals,context=None):
        for key,values in vals.iteritems():
            
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                vals[key] = vals[key].strip()
                word_list =  vals[key].split(' ')
                name = ''
                for word in word_list:
                    if len(word) > 0:
                        name = name + ' ' + word[0].upper()+word[1:]
                vals[key] = name.strip()
        id=super(jkp_pracharak,self).create(cr,uid,vals,context)
        return id
    
    def write(self, cr, uid, ids, vals, context=None):
        for key,values in vals.iteritems():
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                
                if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                    vals[key] = vals[key].strip()
                    word_list =  vals[key].split(' ')
                    name = ''
                    for word in word_list:
                        if len(word) > 0:
                            name = name + ' ' + word[0].upper()+word[1:]
                    vals[key] = name.strip()
        res = super(jkp_pracharak, self).write(cr, uid, ids, vals, context)
        return res
    
    
class event_registration(osv.osv):
    _name="event.registration"
    
    def _check_name_unique(self, cr, uid, ids, context=None):
       name = None
       count = 0
       for each in self.browse(cr, uid, ids):
           name = each.name.lower().replace(' ','')
       read_ids = self.read(cr, uid, self.search(cr, uid, []), ['name'])
       for rec in read_ids:
           if name == rec['name'].lower().replace(' ',''):
               count += 1
               if count > 1:
                   return False
       return True
   
   
    def _check_string(self,cr,uid,ids,context=None):
        for val in self.browse(cr,uid,ids):
            res={}
            str=''
            read_ids = self.read(cr, uid, ids, ['name'])
            for rec in read_ids:
               str=rec['name'] 
               print "------------",str
               if re.match("^-?[a-zA-Z ]+$", str) != None:
                   return True
    _columns={
              'name':fields.char('Name',size=255,required=True)
              }
    
    _sql_constraints=[('unique_event_registration','unique(name)',"Event name should be unique  !"),]
    _constraints =  [
        (_check_string,'name should contain valid characters',['Event']),
       (_check_name_unique, 'name should be unique', ['Event']),
   ]    
    _order='name'
    
    def create(self,cr,uid,vals,context=None):
        for key,values in vals.iteritems():
            print "vals...................",vals
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                vals[key] = vals[key].strip()
                vals[key] = vals[key].title()
              
        id=super(event_registration,self).create(cr,uid,vals,context)
        message='Record Updated Successfully'
        return id
    
    def write(self, cr, uid, ids, vals, context=None):
        for key,values in vals.iteritems():
            if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                
                if vals[key] and isinstance(vals[key], basestring) and len(vals[key]) > 0:
                    vals[key] = vals[key].strip()
                    vals[key] = vals[key].title()
        res = super(event_registration, self).write(cr, uid, ids, vals, context)
        return res
    
class registration_card(osv.osv):
    _name = 'registration.card'
    
    _columns = {
                'name':fields.char('Registration Card No.',size=64,readonly=True),
                'event_id':fields.many2one('event.registration','Event',required=True),
                'registration_date':fields.date('Registration Date',readonly=True),
                'devotees_id':fields.many2one('jkp.devotees',"Devotee's Name",required=True),
                'devotees_reg_no':fields.char("Devotee's Reg No.",size=64),
                'devotees_place':fields.text('Place'),
                'valid_date':fields.date('Valid Until',required=True),
                }
    
    _defaults={
               'registration_date':lambda *a: time.strftime(DEFAULT_SERVER_DATE_FORMAT),
               }
    
    def create(self,cr,uid,vals,context=None):
        code=self.pool.get('ir.sequence').get(cr,uid,'registration.card'),
        vals['name']=code[0]
        id=super(registration_card,self).create(cr,uid,vals,context)
        return id
    
    def onchange_devotees(self, cr, uid, ids, devotees, context=None):
        res = {}
        if not devotees:
            res['value'] = {'devotees_reg_no':'','devotees_place':''}
        devotees = self.pool.get('jkp.devotees').browse(cr, uid, devotees)
        print "devotees ..............",devotees,"place...........",devotees.street1
        res['value'] = {'devotees_reg_no':devotees.reg_no,'devotees_place':devotees.street1}
        return res
            
            
            
            
            
            
        
        

    
