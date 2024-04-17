from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class ProductPrice(models.TransientModel):
    _name = 'product.uom.price'

    product_id=fields.Many2one('product.product',string="Product")
    line_ids=fields.One2many('product.uom.price.line','product_uom_price_id')

    @api.onchange('product_id')
    def set_line_values(self):
        for rec in self:
            product_uom=rec.product_id.uom_id
            get_uom_categ = product_uom.category_id

            get_uom = get_uom_categ.uom_ids
            val_list=[]
            rec.line_ids=[(5,0,0)]
            for uom in get_uom:
                if uom.uom_type == 'bigger':
                    val_list.append((0,0,{
                        'uom_id':uom.id,
                        'ratio':uom.ratio,
                        'cost_price':rec.product_id.standard_price * uom.ratio,
                        'sale_price':rec.product_id.lst_price * uom.ratio
                    }))

                elif uom.uom_type == 'smaller':
                    val_list.append((0, 0, {
                        'uom_id': uom.id,
                        'ratio': uom.ratio,
                        'cost_price': rec.product_id.standard_price / uom.ratio,
                        'sale_price': rec.product_id.lst_price / uom.ratio
                    }))

                else:
                    val_list.append((0, 0, {
                        'uom_id': uom.id,
                        'ratio': uom.ratio,
                        'cost_price': rec.product_id.standard_price,
                        'sale_price': rec.product_id.lst_price
                    }))
            rec.line_ids=val_list


class ProductPriceLine(models.TransientModel):
    _name = 'product.uom.price.line'

    product_uom_price_id=fields.Many2one('product.uom.price')
    uom_id=fields.Many2one('uom.uom',string='Unit')
    ratio=fields.Float(string="Ratio")
    cost_price=fields.Float(string="Cost Price")
    sale_price=fields.Float(string="Sale Price")