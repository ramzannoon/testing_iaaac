# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AttendanceDetails(models.TransientModel):
    _name = "attendance.details"
    _description = "Attendance Details Report"

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    employee = fields.Selection([('all', 'All'),
                                 ('specific', 'Specific')], string='Employees', required=True, default='all')
    device_user_ids = fields.Many2many('hr.employee', string='Employees')

    def action_print_report(self):
        datas = {'active_ids': self.id}
        return self.env.ref('attendance_report.action_attendance_report').report_action(self, data=datas)
