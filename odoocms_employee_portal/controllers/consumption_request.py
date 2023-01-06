from addons.portal.controllers.portal import CustomerPortal
from odoo import http
from odoo.http import content_disposition, Controller, request, route
from datetime import datetime

from datetime import date
from datetime import datetime


class PurchaseConsumptionRequests(http.Controller):

    @http.route(['/purchase/consumption/recs'], type='http', auth="user", website=True, method=['GET'], portal=True)
    def purchase_recs(self, **post):
        return request.render("odoocms_employee_portal.consumption_request_recs")


    @http.route(['/purchase/consumption/form'], type='http', auth="user", website=True, method=['GET'], portal=True)
    def purchase_request_form(self, **post):
        current_user = http.request.env.user
        product_id = request.env['product.product'].sudo().search([])
        data = {
            'product_id': product_id,
            'employee_id': current_user.employee_id.id,
            'material_id': current_user,
            'material': '0',
        }
        return request.render("odoocms_employee_portal.consumption_request_form_template", data)

    @http.route(['/consumption/request/line/new'], type='http', auth="public", website=True)
    def purchase_request_consumption_form_new_addline(self, **kw):
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', http.request.env.context.get('uid'))], limit=1)
        location_id = request.env['stock.location'].sudo().search([('id', '=', 8)])
        dest_location_id = request.env['stock.location'].sudo().search([('id', '=', 5)])
        stock_picking_type = request.env['stock.picking.type'].sudo().search([('id', '=', 5)])

        if employee.department_id:
            department_id = employee.department_id.id
        else:
            department_id = request.env['hr.department'].search([], limit=1).id
        vals = {
            'employee_id': employee.id,
            'department_id': department_id,
            'request_date':  datetime.today().date(),
            'location_id': location_id.id,
            'dest_location_id': dest_location_id.id,
            'custom_picking_type_id': stock_picking_type.id,
        }
        material = request.env['internal.transfer.requisition'].sudo().create(vals)
        line_vals = {
            'product_id': int(kw.get('product_id')),
            'qty': float(kw.get('qty')),
            # 'cost_price': kw.get('cost_price'),
            'internal_picking_req_id': material.id,
            'description': (kw.get('description')),
        }
        material_line = request.env['internal.transfer.requisition.line'].sudo().create(line_vals)
        return request.redirect('/consumption/request/open/%s'%(material.id))


    @http.route(['/consumption/request/add_line/new'], type='http', auth="public", website=True)
    def purchase_request_add_linereq(self, **kw):
        material = request.env['internal.transfer.requisition'].sudo().search([('id', '=', int(kw.get('purchase_hid')))])
        line_vals = {
            'product_id': int(kw.get('product_id')),
            'qty': float(kw.get('qty')),
            'internal_picking_req_id': material.id,
            'description': (kw.get('description')),

        }
        material_line = request.env['internal.transfer.requisition.line'].sudo().create(line_vals)
        return request.redirect('/consumption/request/open/%s'%(material.id))

    @http.route(['/consumption/request/open/<int:material_id>'], type='http', auth="public", website=True)
    def purchase_request_open_ext(self, material_id, access_token=None, **kw, ):
        employee_id = http.request.env.user
        values = {}
        product_id = request.env['product.product'].sudo().search([])
        material = request.env['internal.transfer.requisition'].sudo().search([('id', '=', material_id)], limit=1)
        values.update({
            'material': material,
            'product_id': product_id,
        })
        return request.render("odoocms_employee_portal.consumption_request_form_template", values)

    @http.route(['/consumption/request/form/submit'], type='http', auth="public", website=True, method=['GET', 'POST'],  portal=True)
    def purchase_request_form_submit(self, **post):
        return request.redirect('/consumption/request/recs')


class CustomerPortal(CustomerPortal):

    @http.route(['/consumption/request/form/back'], type='http', auth="public", website=True, method=['GET'], portal=True)
    def purchase_request_back(self, **post):
        return request.redirect('/consumption/request/form')



# class PurchaseRequests(http.Controller):
#
#     @http.route(['/purchase/consumption/recs'], type='http', auth="user", website=True, method=['GET'], portal=True)
#     def purchase_recs(self, **post):
#         return request.render("odoocms_employee_portal.consumption_request_recs")
#
#     @http.route(['/purchase/consumption/form'], type='http', auth="user", website=True, method=['GET'], portal=True)
#     def purchase_request_form(self, **post):
#         product_id = request.env['product.product'].sudo().search([])
#         data = {
#             'product_id': product_id,
#         }
#         return request.render("odoocms_employee_portal.consumption_request_form_template", data)
#
#     @http.route(['/purchase/consumption/form/submit'], type='http', auth="user", website=True, method=['GET','POST'], portal=True)
#     def purchase_consumption_form_submit(self, **post):
#         current_user = http.request.env.user
#
#         product_id = post.get('product_id')
#         product_uom_qty = post.get('product_uom_qty')
#         note = post.get('note')
#
#         request.env['internal.transfer.requisition'].sudo().create({
#             'employee_id': current_user.employee_id.id,
#             'department_id': current_user.employee_id.department_id.id,
#             'request_date': datetime.today().date(),
#             'description': note,
#             'internal_transfer_req_ids': [(0, 0, {
#                 'product_id': int(product_id),
#                 'qty': int(product_uom_qty),
#             })]
#         })
#
#         return request.render("odoocms_employee_portal.purchase_consumption_form_submit",)
#
#     @http.route(['/purchase/request/form/back'], type='http', auth="user", website=True, method=['GET'], portal=True)
#     def purchase_request_back(self, **post):
#         return request.redirect('/purchase/consumption/form')

