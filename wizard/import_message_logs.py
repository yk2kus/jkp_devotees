from openerp.osv import osv,fields
import csv
import base64
from datetime import datetime

class import_message_logs(osv.osv_memory):
    _name="import.message.logs"
    
    _columns={'filename':fields.binary('File', required=True),
              'help':fields.char('Note',readonly=True),
              }
    _defaults={'help':'Delivery report file should only be in CSV(.csv) format.'}
    
    def get_logs(self, cr, uid, ids, context=None):
        res={}
        dev_obj=self.pool.get('jkp.devotees')
        log_obj=self.pool.get('devotees.logs')
        file=self.browse(cr,uid,ids[0]).filename
        date=datetime.now()
        string=base64.decodestring(file)
        try:
            fp=open("/tmp/logs.csv",'w')
        except:
            print "Wait please"
        fp.write(string)
        fp.close()
        data=csv.reader(open("/tmp/logs.csv","rb"))
        print data
        try:
            for row in data:
                if len(row[2])==12:
                    num = row[2]
                    num = num[2:12]
                    print "num............................................",row[2],num
                    search_ids=dev_obj.search(cr,uid,[('mobile1','=',num)] )
                    if search_ids:
                        for val in search_ids:
                            try:
                                log_obj.create(cr,uid,{'log_date':row[3],'mobile_no':num,'status':row[4],'log_id':val,'content':row[0],'creation_date':date})
                            except:
                                pass
                else:
                    num = row[2]                    
                    print "num............................................",num
                    search_ids=dev_obj.search(cr,uid,[('mobile1','=',num)] )
                    if search_ids:
                        for val in search_ids:
                            try:
                                log_obj.create(cr,uid,{'log_date':row[3],'mobile_no':num,'status':row[4],'log_id':val,'content':row[0],'creation_date':date})
                            except:
                                print "============= EXCEPTION ==================="
                                pass
        except:
            raise osv.except_osv(('Unsupported File'),('Please import file in .csv format '))
                
                
        return res