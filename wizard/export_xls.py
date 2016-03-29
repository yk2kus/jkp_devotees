from openerp.osv import osv,fields
import StringIO
import base64
import csv

class export_data(osv.TransientModel):
    _name="export.data"
    _columns={'name':fields.char('Name'),
             'filename':fields.char('File Name',size=250,readonly=True),
             'export_data':fields.binary('File',readonly=True),
             }
    _defaults={'name':'Export Data'}
    
    
    def get_data(self,cr,uid,ids,context=None):
        res={}
        headings=['Serial No','Registration No','First Name','Last Name','Fathers Name','DoB','Gender','Marital Status','Profession ','Qualification','Mother Tongue ','Profession Detail','Address','Country','State','District','Tehsil',
                  'Post Office','PIN','Landline Code','Landline STD','Land Number','Mob1 Code','Mobile 1','Mob2 Code','Mobile 2 ','Email','Email 2','EME Contact Name','EME Relation','EME Address','EME Country','EME State','EME District',
                  'EME Tehsil','EME Post Office','EME PIN','EME Landline Code','EME Land STD','EME Landline No','EME Mobile1 Code','EME Mobile1 No','EME Mobile2 Code','EME Mobile2 No','EME Email','EME Email2','Associated Since','Associated Through',
                  'Prachark','Family Apporoval','Remarks','Accomodation Provided','Accom Mangarh','Accom Barsana','Accom Vrindavan','Accom Other']
        
        cr.execute("select ROW_NUMBER() OVER(ORDER BY 1),reg_no,first_name,last_name,f_name,dob,gender,marital,prof.name as Profession,quali.name as Qualification,lang.name as Mother_tongue,dev.prof_detail,dev.street1 as Address,coun.name as country,state.name as state,distt.name as district,tah.name as tahsil,po.name as post_office,dev.pin,dev.land_code,dev.land_std,dev.landline,dev.m1_code,dev.mobile1,dev.m2_code,dev.mobile2,dev.email,dev.email2,dev.eme_name,dev.eme_rel,concat(dev.eme_street1,dev.eme_street2) as eme_address,eme_coun.name as eme_country,eme_state.name as eme_state,eme_distt as eme_distt,eme_tah.name as eme_tahsil,eme_po.name as eme_post_office,dev.eme_pin,dev.eme_land_code,dev.eme_land_std,dev.eme_landline,dev.eme_m1_code,dev.eme_mobile1,dev.eme_m2_code,dev.eme_mobile2,dev.eme_email,dev.eme_email2,year.name as Associated_Since,through,pracharak.name as Pracharak_Name,family_permission,remark as Remark,accommodation,mangarh as Mangarh,barsana as Barsana,vrindavan as Vrindavan,other as Other from jkp_devotees as dev left join profession_profession as prof on (dev.profession=prof.id) left join qualification as quali on (dev.qualification=quali.id) left join lang_known as lang on (dev.mother_tongue=lang.id) left join res_country as coun on(dev.country_id=coun.id) left join res_country_state as state on(dev.state_id=state.id) left join res_district as distt on (dev.dist_id=distt.id)left join res_tahsil as tah on (dev.tahsil=tah.id) left join post_office as po on(dev.post_id=po.id) left join res_country  as eme_coun on(dev.eme_country_id=eme_coun.id) left join res_country_State as eme_state on(dev.eme_state_id=eme_state.id) left join res_district as eme_distt on (dev.eme_dist_id=eme_distt.id) left join res_tahsil as eme_tah on(dev.eme_tahsil=eme_tah.id) left join post_office as eme_po on(dev.eme_post_id=eme_po.id) left join year_jkp as year on(dev.jkp_year=year.id)  left join jkp_pracharak as pracharak on(dev.pracharak_name=pracharak.id) order by first_name")
        fp = StringIO.StringIO()
        writer = csv.writer(fp)
        data_list=cr.fetchall()
        writer.writerow(headings)   
                   
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
        self.write(cr, uid, ids, {'export_data':out, 'filename':'jkp_devotees.xls'}, context=context)
        return True
    