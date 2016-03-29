#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import openerplib
import logging
import datetime
import string




logger=logging.getLogger('JKP import')
logger.setLevel(logging.DEBUG)

#SET THE LOG FORMATTER
formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#SET THE FILEHANDLER FOR THE LOG
fh=logging.FileHandler('Error.log')
fh.setLevel(logging.ERROR)
fh.setFormatter(formatter)

#SET THE CONSOLE HANDLER
ch=logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

#ADD THE HANDLERS TO THE LOGGER
logger.addHandler(fh)
logger.addHandler(ch)

def run(filename=None, host='localhost', db=None, login=None, passw=None):
    global line
    if filename:
        try: 
            data=csv.reader(open(filename), delimiter=',', quotechar='"')
        except IOError:
            print "No such file exists :%s",filename
    else:
        return False
    
    
    
    reg = 0
    f_name = 1
    l_name = 2
    gen = 3
    prof = 4
    rel = 5
    old=6
    
    conn=openerplib.get_connection(hostname=host, database=db, login=login, password=passw)
    import ast
    
    
    dev_model=conn.get_model("jkp.devotees")
    fam_model=conn.get_model("devotee.family")
    prof_model=conn.get_model("profession.profession")
    incomp=[]
    for val in data:
        count_ids=[]
        dev_ids=dev_model.search([ ('reg_no','=',val[0]) ])  
        if dev_ids:
            prof_ids=prof_model.search([('name','=',val[4] )])
            print "found profession at...............",prof_ids
            if not prof_ids:
                prof_id=prof_model.create({'name':val[4]})
                prof_ids=[prof_id]
            
            
            full_name=val[1]+ ' ' +val[2]
            family={
                     'm2o_jkp':dev_ids[0],
                     'default_name':full_name,
                     'age':val[6],
                     'relation':val[5],
                     'dev_profession':prof_ids and prof_ids[0],
                    }  
            try:
                fam_id=fam_model.create(family)
                print family
                print "created family member is ........................",fam_id
            except:
                " uncreated family members .....",incomp.append(fam_id)
                pass   
            
        else:
            print "devotee not found with reg no :",val[0]
            " uncreated family members .....",incomp.append(fam_id)
    
                
    
           
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
    pass        
    sys.exit()  
    
    if res:
        sys.stdout.flush()
        print "Completed!"
    
    else:
        print "Script_name --help"        
            
