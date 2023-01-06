from datetime import timedelta


from odoo import models
from urllib.request import urlopen
import io
import logging
import pytz

_logger = logging.getLogger(__name__)


class AttendanceReportXlsx(models.AbstractModel):
    _name = "report.attendance_report.attendance_details_xls_temp_id"
    _description = "Attendance Report XLSX"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, wizard_data):
        date_from = wizard_data.date_from
        date_to = wizard_data.date_to
        employee = wizard_data.employee
        device_user_ids = wizard_data.device_user_ids

        company = self.env.company
        domain = []
        if employee == 'specific':
            domain += [('employee_id', 'in', device_user_ids.ids)]

        attendance_ids = self.env['user.attendance'].search([('timestamp', ">=", date_from), ('timestamp', "<=", date_to),] + domain)
        users = self.env['user.attendance'].read_group(domain=[('id', 'in', attendance_ids.ids)],
                                                                  fields=[],
                                                                  groupby=['employee_id'])
        unique_users = [user['employee_id'][0] for user in users]

        main_heading_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': '14',
            "font_color": 'black',
            'font_name': 'Metropolis',
        })

        header_format = workbook.add_format({
            'bold': 1,
            "font_size": '11',
            'size': 10,
            'top': 1,
            'bottom': 2,
            'left': 1,
            'right': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#8EA9DB'
        })
        data_right_bold = workbook.add_format({
            'bold': 1,
            "align": 'right',
            "valign": 'vcenter',
            'font_size': '11',
            'num_format': '#,##0.00',
        })
        data = workbook.add_format({
            "valign": 'vcenter',
            'font_size': '11',
            'num_format': '#,##0.00',
        })
        date_format = workbook.add_format({
            'num_format': 'dd/mm/yy',
            'align': 'center',
            "valign": 'vcenter',
            'font_size': '9',
        })
        datetime_format = workbook.add_format({
            'num_format': 'dd/mm/yy hh:mm:ss',
            'align': 'center',
            "valign": 'vcenter',
            'font_size': '9',
        })
        worksheet = workbook.add_worksheet('Reordering')

        worksheet.set_column('A:A', 35)
        worksheet.set_column('B:L', 25)

        # CompanyLogo
        worksheet.merge_range('A1:A5', " ")

        # Image get from company logo
        web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url = web_base_url + '/logo.png?company=%d' % company.id
        image_data = io.BytesIO(urlopen(url).read())
        worksheet.insert_image('A1:A5', url,
                               {'image_data': image_data, 'x_scale': 1.2, 'y_scale': 0.8, "align": 'center'})

        # Title
        worksheet.merge_range('B1:F2', company.name, main_heading_format)
        worksheet.merge_range('B4:F5', 'Attendance Detailed Report', main_heading_format)
        worksheet.write('A7', "From :", data_right_bold)
        worksheet.write('B7', date_from, date_format)
        worksheet.write('A8', "To :", data_right_bold)
        worksheet.write('B8', date_to, date_format)

        rows = 9
        worksheet.write(rows, 0,  'Employee', header_format)
        worksheet.write(rows, 1,  'Date', header_format)
        worksheet.write(rows, 2,  'Check-in', header_format)
        worksheet.write(rows, 3,  'Check-out', header_format)
        rows += 1

        day_count = (date_to - date_from).days + 1
        for rec in unique_users:
            user_record = self.env['hr.employee'].browse(rec)
            worksheet.write(rows, 0, user_record.name, data)
            # Loop for start date to end date
            for single_date in [d for d in (date_from + timedelta(n) for n in range(day_count)) if d <= date_to]:
                user_attendance_ids = self.env['user.attendance'].search(
                    [('employee_id', "=", user_record.id)])
                attendance_records = []
                for records in user_attendance_ids:
                    if records.timestamp.date() == single_date:
                        attendance_records.append(records)

                # Date wise Attendance
                worksheet.write(rows, 1, single_date, date_format)
                for user_attendance in attendance_records:
                    if user_attendance.attendance_state_id.name == 'Check-in' and user_attendance.activity_id.name == 'Normal Attendance':
                        worksheet.write(rows, 2, user_attendance.timestamp.astimezone(pytz.timezone('Asia/Karachi')).strftime('%d-%m-%Y %H:%M:%S'), datetime_format)
                    if user_attendance.attendance_state_id.name == 'Check-out' and user_attendance.activity_id.name == 'Normal Attendance':
                        worksheet.write(rows, 3, user_attendance.timestamp.astimezone(pytz.timezone('Asia/Karachi')).strftime('%d-%m-%Y %H:%M:%S'), datetime_format)
                rows += 1
            rows += 1
