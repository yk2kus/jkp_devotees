import sys
import csv
import openerplib
import logging
import datetime
import string


def run(filename=None, host='localhost', db=None, login=None, passw=None):
    global line
    if filename:
        try: 
            data=csv.reader(open(filename), delimiter=',', quotechar='"')
        except IOError:
            print "No such file exists :%s",filename
    else:
        return False
    
    name = 0
    
    conn=openerplib.get_connection(hostname=host, database=db, login=login, password=passw)
    import ast
                                    
    prchrk_model=conn.get_model("jkp.pracharak")
    
    for row in data:
        pracharak_ids=[]
        try:
             pracharak_ids = prchrk_model.search([('name','=',row[name])])
             if not pracharak_ids:
                 pracharak_id=prchrk_model.create({'name':row[name]})
                 pracharak_ids=[pracharak_id]
        except:
            pass
        
        temp={'name':pracharak_ids[0]}
        


if __name__=='__main__':
    import argparse
    import os
    import shutil
    import time
 
    parser=argparse.ArgumentParser(prog='csv_import')
    parser.add_argument('--file')
    parser.add_argument('--hostname')
    parser.add_argument('--database')
    parser.add_argument('--login')
    parser.add_argument('--password')
    
    args=vars(parser.parse_args(sys.argv[1:]))
    try:
        res=run(filename=args['file'], host=args['hostname'], db=args['database'], login=args['login'], passw=args['password'])
    except:
        print "Error occur during import"   
        sys.exit()     
    
    if res:
        sys.stdout.flush()
        print "Completed!"
    
    else:
        print "Script_name --help"
        