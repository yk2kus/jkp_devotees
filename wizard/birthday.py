from openerp.osv import osv,fields
import time
import datetime

class jkp_birthday(osv.TransientModel):
    _name = 'jkp.birthday'
    
    days = [
            ('01','01'),
            ('02','02'),
            ('03','03'),
            ('04','04'),
            ('05','05'),
            ('06','06'),
            ('07','07'),
            ('08','08'),
            ('09','09'),
            ('10','10'),
            ('11','11'),
            ('12','12'),
            ('13','13'),
            ('14','14'),
            ('15','15'),
            ('16','16'),
            ('17','17'),
            ('18','18'),
            ('19','19'),
            ('20','20'),
            ('21','21'),
            ('22','22'),
            ('23','23'),
            ('24','24'),
            ('25','25'),
            ('26','26'),
            ('27','27'),
            ('28','28'),
            ('29','29'),
            ('30','30'),
            ('31','31'),
            ]
    
    _columns = {
                'month':fields.selection([('01','January'),('02','February'),('03','March'),('04','April'),('05','May'),('06','June'),('07','July'),
                ('08','August'),('09','September'),('10','October'),('11','November'),('12','December'),],'Month (Birthday)',required=True),
                'day':fields.selection(days,'Day (Birthday)'),
                'devotees_ids':fields.many2many('jkp.devotees','rel_devotees_birthday','devotees_id','birthday','Devotees',readonly=True),
                'name':fields.char('Name'),
                }

    _defaults ={
                'name':'Birthday',
                } 
    
    
    def get_birthday(self, cr, uid, ids, context=None):
        data = self.browse(cr, uid, ids)[0]
        month = data.month
        day = data.day
        dev_ids = []
        if day and month:
            cr.execute("select id,name,email from jkp_devotees where to_char(dob,'MM') = '"+str(month)+"' \
            and to_char(dob,'DD') = '"+str(day)+"'")
        if not day:
            cr.execute("select id,name,email from jkp_devotees where to_char(dob,'MM') = '"+str(month)+"'")
        temp = cr.fetchall()
        
        for rec in temp:
            if len(rec)>0 and rec[0] != None:
                dev_ids.append(rec[0])
                
        self.write(cr, uid, ids, {'devotees_ids':[(6,0,dev_ids)]})
        return True
        
        
        