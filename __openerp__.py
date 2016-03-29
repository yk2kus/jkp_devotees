
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2011-2015 OpenERP4you  (http://openerp4you.in). 
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
#    or take permission from OpenERP4you before resell..
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#    
##############################################################################

{
    "name": "Devotee JKP",
    "version": "1.0",
    "depends": ["base","mail"],
    "author": "Yogesh Kushwaha",
    "category": "Custom",
    "description": """
    This module is designed to keep track on devotees and provide automated functionalities 
    unique -> First Name and Father's Name 
            -> Father's Name and DoB
    
    """,
    "init_xml": [],
    'data': [
                   'security/security_view.xml',
                   'security/ir.model.access.csv',
                   'wizard/xml/check_duplicate_view.xml',  
                   'jkp_calendar_view.xml',                 
                   'jkp_devotees_view.xml',
                   'wizard/xml/send_sms_view.xml',
                   'devotee_sequence_view.xml',
#                   'devotee_mail_view.xml',
                  # 'devotee_script_mail_view.xml', 
                   
                   'wizard/xml/birthday_view.xml',
                   'wizard/xml/import_data_view.xml',
                   'wizard/xml/pracharak_wise_view.xml',
                   'wizard/xml/city_wise_view.xml',
                   'wizard/xml/prominent_devotees.xml',
                   'wizard/xml/sms_report_view.xml',
                   'wizard/xml/export_xls_view.xml',
                   'wizard/xml/devotees_report_view.xml',
                   'wizard/xml/import_messages_logs_view.xml',
                   'wizard/xml/logs_delete_view.xml',
                   'report/devotees_report_view.xml',
                   
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
    'css': [],
#    'certificate': 'certificate',
}
