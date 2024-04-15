from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    name = fields.Char('Order Reference', required=True, index=True, copy=False,readonly=True,states={'draft': [('readonly', False)]}, default='')
    manual_create_date=fields.Datetime(string="Create Date",required=True)

    @api.model
    def create(self, vals_list):
        if 'name' in vals_list.keys():
            get_name_existency = self.env['purchase.order'].sudo().search([('name', '=', vals_list['name'])])
            if get_name_existency:
                raise ValidationError('This Purchase Order Number Already Exists in System, You can not use it')
        res = super(PurchaseOrder, self).create(vals_list)
        return res

    def write(self, vals):
        if 'name' in vals.keys():
            get_name_existency = self.env['purchase.order'].sudo().search([('name', '=', vals['name'])])
            if get_name_existency:
                raise ValidationError('This Purchase Order Already Exists in System, You can not use it')
        res = super(PurchaseOrder, self).write(vals)
        return res