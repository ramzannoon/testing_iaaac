# -*- coding: utf-8 -*-
{
    'name': "Attendance Report",
    'version': '13.0.0.2',
    'summary': """Attendance Report""",
    'description': 'Attendance Report',
    'category': 'Attendance ',
    'author': "IDT",
    'company': 'IDT',
    'website': 'http://www.infinitedt.com',
    'depends': ['web', 'hr_attendance', 'to_attendance_device'],
    'data': [
        'reports/reports.xml',
        'wizard/attendance_details_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
