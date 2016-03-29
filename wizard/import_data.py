# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv,fields
import base64
import openerplib
import xlrd
import datetime
from openerp.tools import flatten 



class import_data(osv.osv_memory):
    _name="import.data"
    _columns={'file':fields.binary('Upload File'),
              'file_format':fields.text("File's Format",readonly=True),
              'help':fields.char('Note',readonly=True),
              }
    _defaults={'file_format':''' Reg No, First Name, Last Name, Father's Name, Date of Birth, Gender,Profession, Qualification, Mother Tongue,
                 Work Details, Languages Known, Permanent Address, Country,State, Distt, Tehsil,Post Office, Pin,Landline Country Code,
                 STD Code, Landline No, Mob Country Code, Mob No, Alt Mob Country Code, Alt Mob No, Email, Alt Email, EME Name, Relation,
                 EME Add,EME Country,EME State,EME Distt,EME Tehsil,EME Post Office,EME Pin, EME Landline Country Code,EME STD Code,EME Landline No,EME Mob Country Code,
                 EME Mob No,EME Alt Mob Country Code,EME Alt Mob No,EME Email, Associated Since, Associated Through, Specify Name,
                 Correspondence Mode, Family Approval, Remarks, Category,Accommodation Provided('Yes','No'),Mangarh,Barsana,Vrindavan,Other,Marital Status,Place,PAN,''',
                 'help':' '}
    
    def file_upload(self,cr,uid,ids,context=None):
        res={}
        incmp=[]
        file=self.browse(cr,uid,ids)[0].file
        string=base64.decodestring(file)
        fp=open("/tmp/jkp.xls",'wb')

        fp.write(string)
        fp.close()
      
        
        regs_no= 0
        first_name = 1
        last_name = 2
        f_name = 3
        dob = 4
        gender = 5
        profession=6
        qualification_ids=7
        mother_tongue=8
        work_detail=9
        lang_known=10
        street1=11
        country=12
        state=13
        district=14
        tahsil=15
        post_office=16
        pin=17
        land_code=18
        land_std=19
        landline=20
        mobile1_code=21
        mobile1=22
        mobile2_code=23
        mobile2=24
        email=25
        email2=26
        eme_name=27
        eme_rel=28
        eme_street1=29
        eme_country=30
        eme_state=31
        eme_district=32
        eme_tahsil=33
        eme_post_office=34
        eme_pin=35
        eme_land_code=36
        eme_land_std=37
        eme_landline=38
        eme_mobile1_code=39
        eme_mobile1=40
        eme_mobile2_code=41
        eme_mobile2=42
        eme_email=43        
        jkp_year=44
        asso_through=45
        spacify_name=46
        contact_mode=47
        permission=48
        rmrk=49
        categories=50
        accommodation=51
        acc_mangarh=52
        acc_barsana=53
        acc_vrindavan=54
        acc_other=55
        marital_status=56
        place = 57
        pan = 58
        
        
        db_name =cr.dbname
        user_id =self.pool.get('res.users').search(cr,uid, [('login','=','admin')])[0]
        pwd     =self.pool.get('res.users').browse(cr ,uid, user_id).password
          
        conn=openerplib.get_connection(hostname='localhost', database=db_name, login='admin', password=pwd)
        
        jkp_model=conn.get_model("jkp.devotees")
        prof_model=conn.get_model("profession.profession")
        quali_model=conn.get_model("qualification")
        lang_model=conn.get_model("lang.known")
        count_model=conn.get_model("res.country")
        stat_model=conn.get_model("res.country.state")
        distc_model=conn.get_model("res.district")
        tahsil_model=conn.get_model("res.tahsil")
        post_model= conn.get_model("post.office")
        year_model=conn.get_model('year.jkp')
        family_model=conn.get_model('devotee.family')
        pchrk_model=conn.get_model('jkp.pracharak')
        categ_model=conn.get_model('jkp.category')
        place_obj  =conn.get_model('res.city')
        relation_obj= conn.get_model('jkp.relation')
        
        
        try:
            revert_prof=[]
            book=xlrd.open_workbook("/tmp/jkp.xls")
            sh=book.sheet_by_index(0)
            for row in range (1,sh.nrows):
                try:
                    rowValues = sh.row_values(row)
                    serial = rowValues[dob]                    
                    seconds = (serial - 25569) * 86400.0
                    dt=datetime.datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d')                   
                    
                    #Place             
                    place_ids=[] 
                    try:                        
                        place_ids=place_obj.search([ ('name','=',rowValues[place].title() ) ])
                        if rowValues[place] and not place_ids:
                            place_id=place_obj.create({'name':rowValues[place] })   
                            place_ids=[place_id]
                    except:
                        pass
                    
                    #PROFESSION
                    prof_ids=[]
                    try:
                        prof_ids=prof_model.search([('name','=',rowValues[profession].title() )])
                        if rowValues[profession] and not prof_ids:
                            prof_id=prof_model.create({'name':rowValues[profession]})
                            prof_ids=[prof_id]
                    except:
                        pass
                                
                    
                    #QUALIFICATION   
            
                    quali_ids=[]
                    if rowValues[qualification_ids]:
                        qualifications= rowValues[qualification_ids].split(',')
                        lan=[]
                        for val in qualifications:
                            val=val.strip()
                            lan_id1=[]
                            lan_id2=[]
                            try:
                                lan_id1=quali_model.search([('name','=',val )])
                                if len(lan_id1)>0:
                                    lan.append(lan_id1)
                                if not lan_id1:
                                    lan_id2=quali_model.create({'name':val})
                                    lan.append(lan_id2)
                                quali_ids=flatten(lan) 
                            except:
                                pass
                    
                    
                    #MOTHER TONGUE            
                    lang_ids=[] 
                    try:
                        lang_ids=lang_model.search([ ('name','=',rowValues[mother_tongue].title() ) ])
                        if rowValues[mother_tongue] and not lang_ids:
                            lang_id=lang_model.create({'name':rowValues[mother_tongue] })   
                            lang_ids=[lang_id]
                    except:
                        pass
                    
                    #COUNTRY USING SQL QUERY =========
                    count_ids=[]
                    try:
                        if rowValues[country]:
                            cr.execute(" select id from res_country where LOWER(name)='"+rowValues[country].lower()+"'")
                            count_ids=cr.fetchone()                             
                    except:
                        pass
                             
                    
                    #STATE
                    state_ids=[]
                    try:
                        state_ids=stat_model.search([ ('name','=',rowValues[state].title() )])
                        if rowValues[state] and not state_ids:
                            state_id=stat_model.create({ 'name':rowValues[state],'country_id':count_ids[0] })
                            state_ids=[state_id]
                    except:
                        pass
                    
                    #DISTRICT
                    distc_ids=[]
                    try:
                        distc_ids=distc_model.search([ ('name','=',rowValues[district].title() )])
                        if rowValues[district] and not distc_ids:
                            distc_id=distc_model.create({ 'name':rowValues[district],'state_id':state_ids[0] })
                            print "...............district",distc_id
                            distc_ids=[distc_id]
                    except:
                        pass    
                    #TAHSIL
                    
                    tahsil_ids=[]
                    try:
                        tahsil_ids=tahsil_model.search([ ('name','=',rowValues[tahsil].title() )])
                        if rowValues[tahsil] and not tahsil_ids:
                            tahsil_id=tahsil_model.create({ 'name':rowValues[tahsil],'dist_id':distc_ids[0] })
                            tahsil_ids=[tahsil_id]
                    except:
                        pass
                    #POST OFFICE
                    pin1=str(rowValues[pin]).split('.')[0]
                    post_ids=[]
                    try:
                        post_ids=post_model.search([ ('name','=',rowValues[post_office].title() ),('distt_id','=',distc_ids[0])])
                        if rowValues[post_office] and not post_ids:
                            post_id=post_model.create({ 'name':rowValues[post_office],'code':pin1,'distt_id':distc_ids[0] })
                            post_ids=[post_id]
                    except:
                        pass
                    regs=str(rowValues[regs_no]).split('.')[0]
                    code=str(rowValues[land_code]).split('.')[0]
                    std=str(rowValues[land_std]).split('.')[0]
                    landline_no=str(rowValues[landline]).split('.')[0]
                    mob1_code=str(rowValues[mobile1_code]).split('.')[0]
                    mobile1_no=str(rowValues[mobile1]).split('.')[0]
                    mobile2_no=str(rowValues[mobile2]).split('.')[0]
                    mob2_code=str(rowValues[mobile2_code]).split('.')[0]
                    
                    
                    # Address Format
                    add1=''
                    if rowValues[street1]:
                        add1=rowValues[street1]                     
                    
                    
                   
                    #EMERGENCY COUNTRY USING SQL QUERY =========
                    eme_count_ids=[]
                    try:    
                        if rowValues[eme_country]:
                            cr.execute(" select id from res_country where LOWER(name)='"+rowValues[eme_country].lower()+"'")
                            eme_count_ids=cr.fetchone() or []
                            eme_count_ids and eme_count_ids[0]
                    except:
                        pass 
                        
                    #EMERGENCY STATE
                    eme_state_ids=[]
                    try:
                        eme_state_ids=stat_model.search([ ('name','=',rowValues[eme_state].title() )])
                        if rowValues[eme_state] and not eme_state_ids:
                            eme_state_id=stat_model.create({ 'name':rowValues[eme_state],'country_id':eme_count_ids and eme_count_ids[0] })
                            eme_state_ids=[eme_state_id]
                    except:
                        pass 
                    
                    #EMERGENCY DISTRICT
                    eme_distc_ids=[]
                    try:
                        eme_distc_ids=distc_model.search([ ('name','=',rowValues[eme_district].title() )])
                        if rowValues[eme_district] and not eme_distc_ids:
                            eme_distc_id=distc_model.create({ 'name':rowValues[eme_district],'state_id':eme_state_ids and eme_state_ids[0] })
                            eme_distc_ids=[eme_distc_id]
                    except:
                        pass
                        
                    #EMERGENCY TAHSIL
                    eme_tahsil_ids=[]
                    try:
                        eme_tahsil_ids=tahsil_model.search([ ('name','=',rowValues[eme_tahsil].title() )])
                        if rowValues[eme_tahsil] and not eme_tahsil_ids:
                            eme_tahsil_id=tahsil_model.create({ 'name':rowValues[eme_tahsil],'dist_id':eme_distc_ids and eme_distc_ids[0] })
                            eme_tahsil_ids=[eme_tahsil_id]
                    except:
                        pass
                    
                    #EMERGENCY POST OFFICE
                    eme_pin1=str(rowValues[eme_pin]).split('.')[0]
                    eme_post_ids=[]
                    try:
                        
                        eme_post_ids=post_model.search([ ('name','=',rowValues[eme_post_office].title() ),('distt_id','=',eme_distc_ids[0])])
                        if rowValues[eme_post_office] and not eme_post_ids:
                            eme_post_id=post_model.create({ 'name':rowValues[eme_post_office],'code':eme_pin1,'distt_id':eme_distc_ids[0] })
                            eme_post_ids=[eme_post_id]
                       
                    except:
                        pass
                    try:
                        devotee_pan=''
                        if len(str(rowValues[pan]).split('.')[0])==10:
                            devotee_pan =str(rowValues[pan]).split('.')[0]                            
                    except:
                        pass
                    eme_code=str(rowValues[eme_land_code]).split('.')[0]
                    eme_std=str(rowValues[eme_land_std]).split('.')[0]
                    eme_landline_no=str(rowValues[eme_landline]).split('.')[0]
                    eme_mob1_code=str(rowValues[eme_mobile1_code]).split('.')[0]
                    eme_mobile1_no=str(rowValues[eme_mobile1]).split('.')[0]
                    eme_mobile2_no=str(rowValues[eme_mobile2]).split('.')[0]
                    eme_mob2_code=str(rowValues[eme_mobile2_code]).split('.')[0]
                    
                    
                    eme_add1=''
                    try:
                        if rowValues[eme_street1]:
                            eme_add1=rowValues[eme_street1]
                           
                        
                    except:
                        pass
                    
                    #JKP YEAR
                    year=str(rowValues[jkp_year]).split('.')[0]
                    print "year is ...................",rowValues[jkp_year],year
                    try:
                        jkp_year_ids=year_model.search([('name','=',year)])
                        print "year found..........*******************",jkp_year_ids
                    except:
                        pass
                    
                    #EME Relation
                    relation_ids=[]
                    try:
                        relation_ids=relation_obj.search([('name','=',rowValues[eme_rel].title())])
                        if rowValues[eme_rel] and not relation_ids:
                            relation_id = relation_obj.create({'name':rowValues[eme_rel]})
                            relation_ids = relation_id                        
                    except:
                        pass
                    
                    
                    #Language Known
                    list1=[]
                    if rowValues[lang_known]:
                        langs= rowValues[lang_known].split(',')
                        lan=[]
                        for val in langs:
                            print "language is ..:",val
                            m=val.split(' ')
                            val=m[-1]
                            lan_id1=[]
                            lan_id2=[]
                            lan_id1=lang_model.search([('name','=',val.title() )])
            
                            print "lan id ......",lan_id1
                            if len(lan_id1)>0:
                                lan.append(lan_id1)
                            if not lan_id1:
                                lan_id2=lang_model.create({'name':val})
                                lan.append(lan_id2)
                            list1=flatten(lan) 
                 
                    # Associate with pracharak  
                    asso_name=rowValues[spacify_name]         
                    pracharak_ids=[]
                    if rowValues[asso_through]=='Pracharak':
                        asso_name=''
                        try:                            
                            pracharak_ids=pchrk_model.search([ ('name','=',rowValues[spacify_name].title() )])                           
                            if rowValues[asso_through] and not pracharak_ids:
                                pracharak_id=pchrk_model.create({ 'name':rowValues[spacify_name] })
                                pracharak_ids=[pracharak_id]
                               
                        except:
                            pass
                    # Associate with Other options  
                    elif rowValues[asso_through] in ['Others','Satsangee','TV Channel']:
                        asso_name = rowValues[spacify_name]
                    # Preferred way of contact    
                    mode = rowValues[contact_mode]
                    mode_list = mode.split(',')
                    jkp_sms    = False
                    jkp_letter = False
                    jkp_mail   = False
                    for val in mode_list:
                        if val.lower().strip() == 'sms':
                            jkp_sms = True
                        if val.lower().strip() == 'email':
                            jkp_mail = True
                        if val.lower().strip() == 'letter':
                            jkp_letter = True
                            
                    # Updated on            
#                    update= rowValues[update_date]
                    
                    # accommodation
                    accom = rowValues[accommodation].title()
                    
                    # Categories
                    categ1=[]
                    if rowValues[categories]:
                        categs = rowValues[categories].split(',')
                        cat=[]
                        for val in categs:
                            cat1 = []
                            cat2 = []
                            cat_id1 = categ_model.search([('name','=',val.title().strip() )])
                            print "val...............................",val
                            if len(cat_id1)>0:
                                cat.append(cat_id1)
                            if not cat_id1:
                                cat_id2=categ_model.create({'name':val})
                                cat.append(cat_id2)
                        categ1=flatten(cat) 
                        
                    #Language Known
                   
                    if rowValues[lang_known]:
                        langs= rowValues[lang_known].split(',')
                        lan=[]
                        for val in langs:
                            
                            lan_id1=[]
                            lan_id2=[]
                            lan_id1=lang_model.search([('name','=',val.title().strip() )])
            
                            print "lan id ......",lan_id1
                            if len(lan_id1)>0:
                                lan.append(lan_id1)
                            if not lan_id1:
                                lan_id2=lang_model.create({'name':val})
                                lan.append(lan_id2)
                        list1=flatten(lan) 
                        
                     
                    print "PAN===============",pan
                    print "place ...............",place_ids 
                                
                    devotee={
                             'reg_no':regs,
                             'first_name':rowValues[first_name],
                             'last_name':rowValues[last_name],
                             'f_name':rowValues[f_name],
                             'dob':dt,
                             'gender':rowValues[gender],
                             'profession':prof_ids and prof_ids[0] ,
                             'qualification_ids':[(6,0,quali_ids)],
                             'mother_tongue':lang_ids and lang_ids[0],
                             'prof_detail':rowValues[work_detail],
                             'street1':add1,
                             
                             'country_id':count_ids and count_ids[0] or False,
                             'state_id':state_ids and state_ids[0] or False,
                             'dist_id':distc_ids and distc_ids[0] or False,
                             'tahsil':tahsil_ids and tahsil_ids[0] or False,
                             'post_id':post_ids and post_ids[0],
                             'pin':pin1,
                             'land_code':code,
                             'land_std':std,
                             'landline':landline_no,
                             'm1_code':mob1_code,
                             'mobile1':mobile1_no or False,
                             'm2_code':mob2_code,
                             'mobile2':mobile2_no,
                             'email':rowValues[email],
                             'email2':rowValues[email2],
                             'eme_name':rowValues[eme_name],
                             'eme_rel':rowValues[eme_rel],
                             'eme_street1':eme_add1,
                             'eme_country_id':eme_count_ids and eme_count_ids[0] or False,
                             'eme_state_id':eme_state_ids and eme_state_ids[0] or False,
                             'eme_dist_id':eme_distc_ids and eme_distc_ids[0] or False,
                             'eme_tahsil':eme_tahsil_ids and eme_tahsil_ids[0] or False,
                             'eme_post_id':eme_post_ids and eme_post_ids[0] or False, 
                             'eme_pin':eme_pin1,
                             'eme_land_code':eme_code,
                             'eme_land_std':eme_std,
                             'eme_landline':eme_landline_no,
                             'eme_m1_code':eme_mob1_code,
                             'eme_mobile1':eme_mobile1_no or False,
                             'eme_m2_code':eme_mob2_code,
                             'eme_mobile2':eme_mobile2_no,
                             'eme_email':rowValues[eme_email],                             
                             'jkp_year':jkp_year_ids and jkp_year_ids[0] or False,
                             'through':rowValues[asso_through],
                             'through_name':asso_name,
                             'pracharak_name':pracharak_ids and pracharak_ids[0],
                             'contact_via':rowValues[contact_mode],
                             'letter':jkp_letter,
                             'sms':jkp_sms,
                             'mail':jkp_mail,
                             'lang_known':[(6,0,list1)],
                             'family_permission':rowValues[permission],
                             'remark':rowValues[rmrk],
                             'category_ids':[(6,0,categ1)],
                             'accommodation':accom,
                             'mangarh':rowValues[acc_mangarh],
                             'vrindavan':rowValues[acc_vrindavan],
                             'barsana':rowValues[acc_barsana],
                             'other':rowValues[acc_other],
                             'marital':rowValues[marital_status].title(),
                             'city_id':place_ids and place_ids[0],
                             'pan_no':devotee_pan,
                             'eme_rel_id':relation_ids and relation_ids[0],
                             }
                    devotee_id = jkp_model.create(devotee)
                    print "created devotee is ..:",devotee
                    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%.un_uploaded devotees ",incmp
                
                except Exception,e:
                    print "&&&&&&&&&&&&&&&&================$$$$$$$$$$$$$$4", e.args
                    incmp.append(row+1)
                    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%.un_uploaded devotees ",incmp
                    pass
        except:
            raise osv.except_osv(('Unsupported File'),('Please upload (.xls) file or Microsoft Excel 2003 '))
     
        return res