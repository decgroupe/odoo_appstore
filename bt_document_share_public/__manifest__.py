# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2018-BroadTech IT Solutions (<http://www.broadtech-innovations.com/>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
##############################################################################

{
    'name': 'Document Share Public',
    'category': 'Document Management',
    'summary': 'Attachment Download',
    'version': '0.1',
    'license':'AGPL-3',
    'description': """
    Attachment Download.
        """,
    'author' : 'BroadTech IT Solutions Pvt Ltd',
    'website' : 'http://www.broadtech-innovations.com',
    'depends': ['mail', 'document'],
    'images': ['static/description/banner.jpg'],
    'data': [        
        'views/ir_attachment_view.xml',        
        'views/templates.xml',
        'wizard/attachment_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
        'static/src/xml/attachment.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
