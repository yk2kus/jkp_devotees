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
    
    
    
    country = 0
    state = 1
    district = 2
    tahsil = 3
    post = 4
    pin = 5
    
    conn=openerplib.get_connection(hostname=host, database=db, login=login, password=passw)
    import ast
    
    con_model=conn.get_model("res.country")
    state_model=conn.get_model("res.country.state")
    dist_model=conn.get_model("res.district")
    tah_model=conn.get_model("res.tahsil")
    post_model=conn.get_model("post.office")
    
    for val in data:
        count_ids=[]
	        
    	if val[0]:
            print "country....1",val[0]
            count_ids=[105]			
    	    print "country ids ",count_ids
            
        try:
            if val[1]:
                print "state....",val[1]
                state_ids=state_model.search([ ('name','=',val[1]),('country_id','=',count_ids and count_ids[0] or False) ])
                if not state_ids:
                    state_id=state_model.create({'name':val[1],'country_id':count_ids and count_ids[0]})
                    state_ids=[state_id]
        except:
            continue
            
        try:        
            if val[2]:
                print "district....",val[2]
                dist_ids=dist_model.search([ ('name','=',val[2]),('state_id','=',state_ids and state_ids[0]) ])
                if not dist_ids:
                    dist_id=dist_model.create({'name':val[2],'state_id':state_ids and state_ids[0]})
                    dist_ids=[dist_id]
        except:
            continue    
                
        try:
            if val[3]:
                print "Tahsil....",val[3]
                tah_ids=tah_model.search([ ('name','=',val[3]),('dist_id','=',dist_ids and dist_ids[0]) ])
                if not tah_ids:
                    tah_id=tah_model.create({'name':val[3],'dist_id':dist_ids and dist_ids[0]})
                    tah_ids=[tah_id]
        except:
            continue 
                
        try:
            if val[4]and val[5]:
                print "Post,Code ....",val[4] ,val[5]
                post_ids=post_model.search([('name','=',val[4]),('distt_id','=',dist_ids and dist_ids[0])])
                if not post_ids:
                    post_id=post_model.create({'name':val[4],'distt_id':dist_ids and dist_ids[0],'code':val[5] })
                    post_ids=[post_id]
        except:
           continue           
	
                
    
           
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
            
