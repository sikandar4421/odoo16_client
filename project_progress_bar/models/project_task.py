
from odoo import api, fields, models


class ProjectTask(models.Model):
    """Inherits the project Task Model for adding new fields and functions"""
    _inherit = "project.task"

    progress_bar = fields.Float(string='Progress Bar',
                                help='Calculate the progress of the task '
                                     'based on the task stage',
                                compute='_compute_task__progress_bar')
    stage_is_progress = fields.Boolean(related='stage_id.is_progress_stage',
                                       help='Status of the task based the '
                                            'stage')
    percentage_each_stage = fields.Float(compute='_get_each_stage_percentage', stroe=True, string='Total %')
    max_per_each_stage = fields.Float()
    completed_no_each_stage = fields.Float(compute='get_complete_each_stage', store=True, string='SubTask %')
    completed_sub_task = fields.Float(compute='get_complete_each_stage', string='Progress')

    # fields for percentage on task sub-task
    complete_work = fields.Float('Completed Work')
    per_graph = fields.Float(compute='get_completed_work')

    hide_btn_subtask = fields.Boolean(default=False)

    ##project cost division on each task
    amt_per_each_stage = fields.Float('stage % amt')
    amt_single = fields.Float('% per Task')
    #amt_sing_subtask holdes the % amt of esch subtask from subtask amount
    amt_single_subtask = fields.Float('% amt each sub task')


    # @api.depends('stage_id', 'project_id')
    # def get_amount_task(self):
    #     for rec in self:
    #         rec.amt_per_each_stage = (rec.project_id.total_cost * rec.stage_id.progress_bar)/100
            # print(rec.amt_per_each_stage)
            # import pdb
            # pdb.set_trace()

    def get_subtask(self):
        tasks = self.env['task.subtask'].search([('stage', '=', self.stage_id.id)])
        if tasks:
            SubTask = self.env['project.task']
            for line in tasks:
                data = {
                    'parent_id': self.id,
                    'ancestor_id': self.id,
                    'name': line.name,
                    'stage_id': line.stage.id,
                }
                SubTask.sudo().create(data)
            self.hide_btn_subtask = True

    @api.onchange('complete_work')
    def check_kanban(self):
        for rec in self:
            if rec.complete_work == 100.0:
                rec.kanban_state = 'done'
            else:
                rec.kanban_state = 'normal'

    @api.depends('complete_work')
    def get_completed_work(self):
        """Compute functionality to display percentage on task page sub-task tree view """
        for rec in self:
            rec.per_graph = rec.complete_work

    @api.depends('stage_id')
    def _compute_task__progress_bar(self):
        """Compute functionality for the task based on the progress bar"""
        for rec in self:
            rec.progress_bar = rec.stage_id.progress_bar

    @api.depends('stage_id')
    def _get_each_stage_percentage(self):
        """Compute functionality to get percentage on project task dynamically"""
        for rec in self:
            total_task_each_stage = self.env['project.task'].search_count([
                ('project_id', '=', rec.project_id.id),('stage_id', '=', rec.stage_id.id),('parent_id', '=', None)
            ])
            rec.percentage_each_stage = rec.stage_id.progress_bar / total_task_each_stage

            #for price on each task
            rec.amt_per_each_stage = (rec.project_id.total_cost * rec.stage_id.progress_bar) / 100
            rec.amt_single = rec.amt_per_each_stage / total_task_each_stage


    @api.depends('stage_id')
    def get_complete_each_stage(self):
        """Compute functionality to get percentage on subtask of project task dynamically and show overall percentage of project"""
        for rec in self:
            rec.completed_no_each_stage = 0
            total_sub_task = self.env['project.task'].search_count([
                ('project_id', '=', rec.project_id.id),('stage_id', '=', rec.stage_id.id),('parent_id', '=', rec.id)
            ])
            if total_sub_task:
                rec.completed_no_each_stage = rec.percentage_each_stage / total_sub_task
                rec.amt_single_subtask = rec.amt_single / total_sub_task
            # else:
            #     rec.completed_no_each_stage = rec.percentage_each_stage
            print(rec.completed_no_each_stage,'each')
            # calculate percentage of each task complated etc
            progressbar_tasks = self.env['project.task'].search(
                [('kanban_state', '=', 'done'),('parent_id', '=', rec.id)])
            progressbar_tasks_not_sub = self.env['project.task'].search(
                [('kanban_state', '=', 'done'), ('parent_id', '=', None)])
            print(progressbar_tasks_not_sub,'fdfdf')
            if progressbar_tasks:
                rec.completed_sub_task = 0
                for tasks in progressbar_tasks:
                    rec.completed_sub_task += rec.completed_no_each_stage
            elif progressbar_tasks_not_sub:
                rec.completed_sub_task = 0
                for parent_task in progressbar_tasks_not_sub:
                    print(parent_task.percentage_each_stage)
                    parent_task.completed_sub_task = parent_task.percentage_each_stage
            else:
                rec.completed_sub_task = 0


