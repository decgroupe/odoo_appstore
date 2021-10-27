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
#    GNU Affero General Public License for more details
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
##############################################################################

from odoo import api, fields, models


class AttachmentLink(models.TransientModel):
    _name = 'attachment.link'
    _description = 'Attachment Link'
    

    line_ids = fields.One2many('attachment.link.lines','link_id', 'Lines')
   
    @api.model
    def default_get(self, fields):
        res = super(AttachmentLink, self).default_get(fields)
        context = self._context or {} 
        active_model = context.get('active_model')
        active_id = context.get('active_id')
        config_obj = self.env['ir.config_parameter'].get_param('web.base.url')
        attachment_url = config_obj + "/web/attachments/token/"
        attach_name = self.env['ir.attachment'].search([('res_id', '=', active_id),('res_model', '=', active_model)])
        res['line_ids'] = []
        for att_obj in attach_name:
            if att_obj.access_token:
                att_link = attachment_url + att_obj.access_token
                res['line_ids'].append((0, 0, {'name':att_obj.name, 'link':att_link, 'click_link':'Click Here'}))
        return res



class AttachmentLinkLines(models.TransientModel):
    _name = 'attachment.link.lines'
    _description = 'Attachment Link Lines'
    

    name = fields.Char('Name')
    link = fields.Char('Link', readonly=True)
    link_id = fields.Many2one('attachment.link','Link Id')
    click_link = fields.Char('Link')

# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
