from odoo import models, fields, api
from odoo import exceptions


class SaleOrderReportWizard(models.TransientModel):
    _name = 'sale.order.report.wizard'

    project_id = fields.Many2one('project.project', string='Project')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    @api.constrains('start_date', 'end_date')
    def _comparison_start_end_date(self):
        if self.start_date > self.end_date:
            raise exceptions.ValidationError('Start Date Must Be Less Than End Date')

    def action_get_values(self,  data=None):
        print('Hello')
        self.ensure_one()
        [data] = self.read()
        datas = {
            'ids': [],
            'form': data
        }

        return self.env.ref('sale_order_report.action_print_report_sale').report_action(self, data=datas, config=False)


class RegisterWizardPdfReport(models.AbstractModel):
    _name = 'report.sale_order_report.wizard_report_sale_pdf'
    _description = 'Accession Register Report'

    @api.model
    def _get_report_values(self, docsid, data=None):
        start_date = data['form']['start_date'] or False
        end_date = data['form']['end_date'] or False
        project_id = data['form']['project_id'][0] or False
        project_name = data['form']['project_id'][1] or False
        sale_orders = self.env['sale.order'].search([
            ('project_id', '=', project_id),
            ('date_order', '>=', start_date),
            ('date_order', '<=', end_date),
        ])

        qty = 0
        total_price = 0
        sub_total = 0
        for rec in sale_orders.order_line:
            qty = qty + rec.product_uom_qty
            total_price = total_price + rec.price_unit
            sub_total = sub_total + (rec.product_uom_qty * rec.price_unit)
        docargs = {
            'doc_ids': [],
            'project_name': project_name or False,
            'sale_orders': sale_orders or False,
            'qty': qty or False,
            'total_price': total_price or False,
            'sub_total': sub_total or False
        }
        return docargs

