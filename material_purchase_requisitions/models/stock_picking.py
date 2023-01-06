# -*- coding: utf-8 -*-

from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    custom_requisition_id = fields.Many2one(
        'material.purchase.requisition',
        string='Purchase Requisition',
        readonly=True,
        copy=True
    )

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        if self.origin:
            internal_transfer_requisition = self.env['internal.transfer.requisition'].search([('name', '=', self.origin)])
            if internal_transfer_requisition:
                internal_transfer_requisition.state = 'receive'
        return res


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    custom_requisition_line_id = fields.Many2one(
        'material.purchase.requisition.line',
        string='Requisitions Line',
        copy=True
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
