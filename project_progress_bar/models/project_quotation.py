from odoo import models, fields, api, _


class ProjectQuotation(models.Model):
    _name = 'project.quotation'
    _description = 'To create quotation for project'

    name = fields.Char('Project Name')
    subject = fields.Char('Quotation Subject')
    attention = fields.Char("Attention")
    date = fields.Date('Date')
    ref = fields.Char('Ref')
    discount = fields.Integer('Special Discount')
    total = fields.Integer('Total Amount')
    grand_total = fields.Integer('Grand Total')
    quotation_line = fields.One2many('project.quotation.line', 'quotation_id')
    note = fields.Html(string="Terms and conditions",)

    def get_items(self):
        items = self.env['project.quotation.setup'].search([])
        for rec in items:
            data = {
                'name': rec.name,
                'qty': rec.qty,
                'rate': rec.rate,
                'unit': rec.unit.id,
                'quotation_id': self.id
            }
            self.env['project.quotation.line'].sudo().create(data)


class ProjectQuotationLine(models.Model):
    _name = 'project.quotation.line'
    _description = "Quotation Line"

    name = fields.Char('Description')
    #sequence = fields.Integer(string="Sequence", default=10)
    unit = fields.Many2one('uom.uom', string="Unit")
    qty = fields.Integer('Quantity')
    rate = fields.Monetary("Rate")
    price_subtotal = fields.Monetary('Amount', compute='_get_sub_total')
    quotation_id = fields.Many2one('project.quotation')
    currency_id = fields.Many2one(
        'res.currency',
        store=True, precompute=True)

    display_type = fields.Selection(
        selection=[
            ('line_section', "Section"),
            ('line_note', "Note"),
        ],
        default=False)

    @api.depends('rate', 'qty')
    def _get_sub_total(self):
        for rec in self:
            rec.price_subtotal = rec.qty * rec.rate


class ProjectQuotationSetup(models.Model):
    _name = 'project.quotation.setup'

    name = fields.Char("Item Name")
    unit = fields.Many2one("uom.uom", stinr="Unit")
    qty = fields.Integer('Quantity')
    rate = fields.Float('Rate')