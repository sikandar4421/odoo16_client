from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True,default=lambda self: _(''))

    manual_create_date=fields.Datetime(string="Create Date",required=True)
    @api.model
    def create(self, vals_list):
        if 'name' in vals_list.keys():
            get_name_existency=self.env['sale.order'].sudo().search([('name','=',vals_list['name'])])
            if get_name_existency:
                raise ValidationError('This Sale Order Number Already Exists in System, You can not use it')
        res=super(SaleOrder, self).create(vals_list)
        return res

    def write(self, vals):
        if 'name' in vals.keys():
            get_name_existency=self.env['sale.order'].sudo().search([('name','=',vals['name'])])
            if get_name_existency:
                raise ValidationError('This Sale Order Already Exists in System, You can not use it')
        res=super(SaleOrder, self).write(vals)
        return res

    def action_confirm(self):
        for rec in self:
            res=super(SaleOrder, rec).action_confirm()
            for line in rec.order_line:
                get_uom_categ = line.product_uom.category_id

                get_uom = get_uom_categ.uom_ids.filtered(lambda x: x.id == line.product_uom.id)

                for uom in get_uom:
                    if uom.uom_type == 'bigger':
                        line.product_id.with_company(line.company_id.id).sudo().write(
                            {'standard_price': line.cost_price/uom.ratio})

                    elif uom.uom_type == 'smaller':
                        line.product_id.with_company(line.company_id.id).sudo().write(
                            {'standard_price': line.cost_price * uom.ratio})

                    else:
                        line.product_id.with_company(line.company_id.id).sudo().write(
                            {'standard_price': line.cost_price})    
            return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    cost_price=fields.Float(string="Cost Price")
    extra_percentage=fields.Float(string="Extra %")
    uom_qty=fields.Float(string="UOM Quantity")

    price_unit = fields.Float(
        string="Unit Price",
        compute='_compute_price_unit_customize',
        digits='Product Price',
        store=True, readonly=False, required=True, precompute=True)

    @api.onchange('product_id','product_uom')
    def set_cost_price(self):
        for rec in self:
            get_uom_categ = rec.product_uom.category_id

            get_uom=get_uom_categ.uom_ids.filtered(lambda x:x.id==rec.product_uom.id)

            for uom in get_uom:
                if uom.uom_type == 'bigger':
                    rec.cost_price=rec.product_id.standard_price*uom.ratio

                elif uom.uom_type == 'smaller':
                    rec.cost_price=rec.product_id.standard_price/uom.ratio

                else:
                    rec.cost_price = rec.product_id.standard_price


    @api.depends('product_id', 'product_uom', 'product_uom_qty','extra_percentage','cost_price')
    def _compute_price_unit_customize(self):
        for rec in self:
            rec.price_unit = rec.cost_price + (rec.cost_price * (rec.extra_percentage / 100))
            # get_uom_categ=rec.product_uom.category_id
            # get_uom = get_uom_categ.uom_ids.filtered(lambda x: x.id == rec.product_uom.id)
            #
            # for uom in get_uom:
            #     if uom.uom_type == 'bigger':
            #         rec.price_unit = (rec.cost_price + (rec.cost_price * (rec.extra_percentage / 100)))
            #
            #     elif uom.uom_type == 'smaller':
            #         rec.price_unit = (rec.cost_price + (
            #                     rec.cost_price * (rec.extra_percentage / 100)))
            #
            #     else:
            #         rec.price_unit = rec.cost_price + (rec.cost_price * (rec.extra_percentage / 100))



