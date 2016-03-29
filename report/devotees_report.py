
import time

from openerp.report import report_sxw

class devotees_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(devotees_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_langs':self.get_langs,
            'get_qualification':self.get_qualification,
            'get_correspondence_info':self.get_correspondence_info,
            })
        
    def get_langs(self,lang_ids):
        lang=''
        for i in lang_ids:
            lang=lang+i.name+', '
        if lang[-2:]==', ':
            lang=lang[0:-2]
        return lang
    
    def get_qualification(self,quali_ids):
        qualification=''
        for i in quali_ids:
            qualification=qualification+i.name+', '
        if qualification[-2:] == ', ':
            qualification = qualification[0:-2]
                
        return qualification
    def get_correspondence_info(self,letter,msg,email):
         
        preferrence=''
        if letter== True:
            preferrence = 'Letter'
        if msg == True:
            if preferrence:
                preferrence = preferrence + ', '+ 'SMS'
            else:
                preferrence = 'SMS'
        if email == True:
            if preferrence:
                preferrence = preferrence + ', '+ 'Email'
            else:
                preferrence = 'Email'
        return preferrence
            
    
report_sxw.report_sxw('report.devotees.report', 'jkp.devotees', 'addons/jkp_devotees/report/jkp_report.rml', parser=devotees_report, header=False)




