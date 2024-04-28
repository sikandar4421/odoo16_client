from odoo import api, fields, models


class SubTask(models.Model):
    _name = "task.subtask"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Create Subtask For each stage"

    name = fields.Char('Name')
    stage = fields.Many2one('project.task.type', string='Stage')

