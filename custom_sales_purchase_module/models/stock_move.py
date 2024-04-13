from collections import defaultdict

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero, OrderedSet

import logging

class StockMove(models.Model):
    _inherit = "stock.move"

    def product_price_update_before_done(self, forced_qty=None):
        res=super(StockMove, self).product_price_update_before_done( forced_qty=None)
        for move in self.filtered(lambda move: move._is_in() and
                                               move.with_company(move.company_id).product_id.cost_method=='standard'):
            new_sp = move._get_price_unit()
            move.product_id.with_company(move.company_id.id).sudo().write({'standard_price': move._get_price_unit()})

