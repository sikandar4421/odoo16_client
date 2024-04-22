# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    #project_id = fields.Many2one('project.project', string='Project')

    @api.onchange('project_list')
    def get_customer_name(self):
        if self.project_list:
            self.partner_id = self.project_list.partner_id
