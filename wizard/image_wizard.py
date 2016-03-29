# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2011-2015 OpenERP Resource  (http://openerpresource.com). 
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
#    or take permission from Openerp Resource before resell..
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#    
##############################################################################

from osv import osv, fields
import base64
import os
from openerp import _


class wiz_image(osv.osv_memory):
    _name = 'wiz.image'
    
    _columns = {
                'image':fields.binary('Image'),
                'image_name':fields.char('Image Name',size=64,required=True,readonly=True),
                
                }
    
    def default_get(self, cr, uid, fields, context=None):
        if not context:
            context = {}
        ids = context.get('active_ids',[])
        model = context.get('active_model')
        res = super(wiz_image, self).default_get(cr, uid, fields, context=context)
        if model == None:
            return res
        
        for line in self.pool.get(model).name_get(cr, uid, ids):
            if len(line) > 0:
                if 'image_name' in fields:
                    name = line[1].replace('/','-')
                    name = line[1].replace(' ','')
                    name = line[1].strip()
                    res.update({'image_name':name+'.jpg'})
        return res
        
        
    def create_image(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        prod_ids = context.get('active_ids',[])
        model = context.get('active_model')
        if model == None:
            return {'type':'ir.actions.act_window_close'}
        each = self.read(cr, uid, ids, ['image_name','image'])
        if each[0]['image_name'] and not each[0]['image']:
            raise osv.except_osv(_('UserError'), _('Please select the image..'))
        try:
            if each[0]['image_name'] and each[0]['image']:
                bin = base64.decodestring(each[0]['image'])
                fname = each[0]['image_name']
                filename = str(os.getcwd()+'/Photo/Devotees/'+each[0]['image_name'])
                f = open(filename , 'wb')
                f.write(bin)
                self.pool.get(model).write(cr, uid, prod_ids, {'image_url':each[0]['image_name']})
            
        except:
            pass
               
        return {'type':'ir.actions.act_window_close'}
