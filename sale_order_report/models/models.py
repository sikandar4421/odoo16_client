# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one('project.project', string='Project')

    @api.onchange('project_id')
    def get_customer_name(self):
        if self.project_id:
            self.partner_id = self.project_id.partner_id
