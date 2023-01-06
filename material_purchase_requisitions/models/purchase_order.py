# -*- coding: utf-8 -*-

from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    custom_requisition_id = fields.Many2one(
        'material.purchase.requisition',
        string='Requisitions',
        copy=False
    )

    approved_by = fields.Many2one('res.users', string="Approved By")

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        self.approved_by = self.env.user
        return res


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    warranty = fields.Char(string="Warranty")

    custom_requisition_line_id = fields.Many2one(
        'material.purchase.requisition.line',
        string='Requisitions Line',
        copy=False
    )
    terms_and_conditions = fields.Char(string='Terms and Conditions')
