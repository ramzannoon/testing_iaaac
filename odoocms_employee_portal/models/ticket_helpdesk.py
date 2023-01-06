from odoo import fields, models


class Helpdesk(models.Model):
    _inherit = 'helpdesk.ticket'

    department_id = fields.Many2one('helpdesk.ticket.team', string="HelpDesk" )

    employee = fields.Many2one('res.users', string="Employee", domain=lambda self: [
        ('groups_id', 'in', self.env.ref('base.group_portal').id)])


class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'
