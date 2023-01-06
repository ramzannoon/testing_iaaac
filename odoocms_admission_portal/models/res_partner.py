from odoo import api, fields, models, _


class ResPartner(models.Model):
	_inherit = 'res.partner'

	cnic = fields.Char(string='CNIC')
	is_student = fields.Boolean(string="Is Student")
	program_id = fields.Many2one('odoocms.program', string='Program')


class ResCompany(models.Model):
	_inherit = "res.company"

	short_name = fields.Char('Short Name')
