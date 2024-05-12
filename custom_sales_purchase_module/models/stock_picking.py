from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_note_no=fields.Char(string="Delivery Note No.")
    date_of_delivery=fields.Datetime(string='Date of Delivery')