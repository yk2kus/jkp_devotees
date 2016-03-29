#! /usr/bin/env python
# -*- coding: utf-8 -*-

import openerplib

conn=openerplib.get_connection(hostname='localhost', database='new_server', login='admin', password='a')
obj=conn.get_model("jkp.devotees")

for i in range(8000,8400):
	id=i
	z=str(i).zfill(5)
	seq='DEV' + z
	ids=obj.search([])
	print ids
	print seq	     
	try:
		obj.write(id,{'sequence':seq})
	except:
		print "========================================="





	
	
	
