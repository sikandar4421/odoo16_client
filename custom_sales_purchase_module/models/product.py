from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class ProductTemplate(models.Model):
    _inherit = 'product.product'

    lst_price = fields.Monetary(
        'Sales Price', default=0.0,
        digits='Product Price',
        help="Price at which the product is sold to customers.",
        compute="set_latest_sale_price"
    )

    @api.depends('detailed_type')
    def set_latest_sale_price(self):
        for rec in self:
            rec.lst_price = 0
            if rec.ids:
                get_hisghest_sale=self.env['sale.order'].sudo().search([('company_id','=',self.env.company.id),
                                                                     ('state','in',('sale','done')),
                                                                        ('order_line.product_id','=',rec.ids[0])],order='id desc',limit=1)
                if get_hisghest_sale:
                    filter_line=get_hisghest_sale.order_line.filtered(lambda x:x.product_id.id==rec.ids[0])
                    for line in filter_line:
                        rec.lst_price=line.price_unit
