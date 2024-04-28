
from odoo import api, fields, models


class ProjectProject(models.Model):
    """Inherits the project Model for adding new fields and functions"""
    _inherit = "project.project"

    progressbar = fields.Float(string='Progress',
                               compute='_compute_progress_bar',
                               help='Calculate the progress of the task '
                                    'based on the task stage')
    is_progress_bar = fields.Boolean(string='Is Progress Bar',
                                     help='Status of the task based the '
                                          'stage')
    max_rate = fields.Integer(default=100)
    total_cost = fields.Float('Project Cost')

    @api.depends('task_ids')
    def _compute_progress_bar(self):
        """Compute functionality for the task based on the progress bar"""
        for rec in self:
            progressbar_tasks = self.env['project.task'].search([('project_id', '=', rec.id),('parent_id', '=', None)])
            if progressbar_tasks:
                for tasks in progressbar_tasks:
                    rec.progressbar += int(tasks.completed_sub_task)
            else:
                rec.progressbar = 0

