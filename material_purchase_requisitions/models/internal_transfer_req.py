# -*- coding: utf-8 -*-

from odoo import models, fields, api


class IntTransferReq(models.Model):
    _name = 'internal.transfer.requisition'
    _description = 'Internal Transfer Requisition'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', index=True, readonly=1)

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, track_visibility='onchange')
    department_id = fields.Many2one('hr.department', string='Department', required=True, track_visibility='onchange', store=True, compute='_get_department')
    request_date = fields.Date(string='Requisition Date', required=True, track_visibility='onchange', default=fields.Datetime.now,)
    description = fields.Char(string='Description')

    location_id = fields.Many2one('stock.location', string='Source Location', track_visibility='onchange')
    dest_location_id = fields.Many2one('stock.location', string='Destination Location', track_visibility='onchange')
    custom_picking_type_id = fields.Many2one('stock.picking.type', string='Picking Type', track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'New'),
        ('dept_confirm', 'DEAN/HOD Approval'),
        ('approved', 'Approved'),
        ('receive', 'Received'),
        ('cancel', 'Cancelled'),
        ('reject', 'Rejected')],
        default='draft',
        track_visibility='onchange',
    )
    department_approval = fields.Boolean(string="Department Approve", default=False, copy=False)
    department_approval_user = fields.Many2one('res.users', string="Department Approve User", default=False, copy=False)

    internal_transfer_req_ids = fields.One2many('internal.transfer.requisition.line', 'internal_picking_req_id')



    @api.depends('employee_id')
    def _get_department(self):
        for rec in self:
            if rec.employee_id and rec.employee_id.department_id:
                rec.department_id = rec.employee_id.department_id.id



    @api.model
    def create(self, vals):
        location_id = self.env['stock.location'].sudo().search([('id', '=', 8)])
        dest_location_id = self.env['stock.location'].sudo().search([('id', '=', 5)])
        stock_picking_type = self.env['stock.picking.type'].sudo().search([('id', '=', 5)])
        name = self.env['ir.sequence'].next_by_code('internal.requisition.seq')
        vals.update({
            'name': name,
            'location_id': location_id.id,
            'dest_location_id': dest_location_id.id,
            'custom_picking_type_id': stock_picking_type.id,
        })
        res = super(IntTransferReq, self).create(vals)
        return res

    # @api.onchange('employee_id')
    # def _onchange_employee_id(self):
    #     for rec in self:
    #         if rec:
    #             rec.department_id = rec.employee_id.department_id.id


    def transfer_confirm(self):
        for rec in self:
            rec.state = 'dept_confirm'

    def manager_approve(self):
        for rec in self:
            if not self.env.user.user_has_groups(
                    'material_purchase_requisitions.group_purchase_requisition_department') or rec.department_id.manager_id.sudo().user_id.id != self.env.uid:
                raise models.ValidationError('You are not Allowed to approve this Requisition!!')
            else:
                picking_line_list = []
                for line in rec.internal_transfer_req_ids:
                    picking_line_vals = {
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.qty,
                        'name': line.description,
                        'product_uom': line.product_id.uom_id.id
                    }
                    picking_line_list.append((0, 0, picking_line_vals))
                picking_vals = {
                    'partner_id': rec.employee_id.address_home_id.id,
                    'origin': rec.name,
                    'picking_type_id': rec.custom_picking_type_id.id,
                    'location_id': rec.location_id.id,
                    'location_dest_id': rec.dest_location_id.id,
                    'scheduled_date': fields.Datetime.now(),
                    'custom_requisition_id': rec.id,
                    'move_ids_without_package': picking_line_list
                }
                self.env['stock.picking'].create(picking_vals)
                rec.state = 'approved'
                self.department_approval = True
                self.department_approval_user = self.env.user

    def show_picking(self):
        for rec in self:
            res = self.env.ref('stock.action_picking_tree_all')
            res = res.read()[0]
            res['domain'] = str([('custom_requisition_id', '=', rec.id)])
        return res



    def requisition_reject(self):
        for rec in self:
            rec.state = 'reject'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


class IntTransferReqLines(models.Model):
    _name = 'internal.transfer.requisition.line'
    _description = 'Internal Transfer Requisition Line'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    description = fields.Char(string='Description', related='product_id.name')
    internal_picking_req_id = fields.Many2one('internal.transfer.requisition')
    qty = fields.Float(string='Qty')



class PickingInherit(models.Model):
    _inherit = 'stock.picking'

    custom_requisition_id = fields.Many2one('internal.transfer.requisition')
