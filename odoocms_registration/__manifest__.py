
{
    "name": "OdooCMS Registration",
    'version': '13.0.0.14',
    'license': 'LGPL-3',
    'category': 'OdooCMS',
    'sequence': 3,
    'summary': "Registration Management Module of OdooCMS",
    'author': 'IDT',
    'company': 'IDT',
    'website': 'http://www.infinitedt.com',
    "depends": ['odoocms'],
    "data": [
        'security/odoocms_registration_security.xml',
        'security/ir.model.access.csv',
        'data/registration_data.xml',
        'data/sequence.xml',
        'menu/registration_menu_view.xml',

        'views/batch_section_view.xml',
        'views/term_scheme_view.xml',
        'views/class_view.xml',
        'views/course_registration_view.xml',
        'views/course_registration_bulk_view.xml',
        'views/course_registration_bulk2_view.xml',
        'views/student_registration_view.xml',
        'views/student_view.xml',
        'views/student_registration_load_view.xml',
        'views/student_request_view.xml',
        'views/inherits_view.xml',
        'views/faculty_staff_view.xml',
        'views/class_generator_view.xml',
        'views/res_config_setting_view.xml',

        'views/course_freeze.xml',

        # 'wizard/register_scheme_course_view.xml',
        'wizard/assign_section_wiz_view.xml',
        'wizard/promote_students.xml',
    ],
    'images': ['static/description/banner.jpg'],
    "installable": True,
    "auto_install": False,
    'application': True,
}
