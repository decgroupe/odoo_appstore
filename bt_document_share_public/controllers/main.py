# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016-BroadTech IT Solutions (<http://www.broadtech-innovations.com/>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
##############################################################################

import json
import base64
import logging
import werkzeug

from odoo import http
from odoo.http import request
from odoo.tools import html_escape
from odoo.addons.web.controllers.main import _serialize_exception


class website_account(http.Controller):
    
    @http.route('/web/attachments/token/<string:token>', type='http', auth="none")
    def get_attachments(self, token , **kwargs):
        try:
            attachment_ids = request.env['ir.attachment'].sudo().search([('access_token', '=', token)])
            if attachment_ids:
                for attachment_obj in attachment_ids:
                    filecontent = base64.b64decode(attachment_obj.datas)
                    disposition = 'attachment; filename=%s' % werkzeug.urls.url_quote(attachment_obj.datas_fname)
                    return request.make_response(
                        filecontent,
                        [('Content-Type', attachment_obj.mimetype),
                         ('Content-Length', len(filecontent)),
                         ('Content-Disposition', disposition)])
            else:
                error = {
                'code': 200,
                'message': "Unable to find the attachments",
                }
            return request.make_response(html_escape(json.dumps(error)))
            
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
#                 'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))


# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4: