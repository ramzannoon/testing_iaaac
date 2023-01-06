from addons.portal.controllers.portal import CustomerPortal
from odoo import http
from odoo.http import content_disposition, Controller, request, route
from datetime import datetime


class PurchaseRequests(http.Controller):

    @http.route(['/purchase/request/recs'], type='http', auth="public", website=True)
    def purchase_recs(self, **post):
        return request.render("odoocms_employee_portal.purchase_request_recs")

    @http.route(['/purchase/request/form'], type='http', auth="public", website=True, method=['GET'], portal=True)
    def purchase_request_form(self, record=None, **post, ):
        current_user = http.request.env.user
        product_id = request.env['product.product'].sudo().search([])
        data = {
            # 'standard_price': product_id.standard_price.id,
            'product_id': product_id,
            'employee_id': current_user.employee_id.id,
            'material_id': current_user,
            'material': '0',
        }
        print(data,444444444444444444444444)
        return request.render("odoocms_employee_portal.purchase_request_form_template", data)

    @http.route(['/purchase/request/line/new'], type='http', auth="public", website=True)
    def purchase_request_form_new_addline(self, **kw):
        current_user = http.request.env.user
        reason_for_purchase = kw.get('reason_for_purchase')
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', http.request.env.context.get('uid'))], limit=1)
        if employee.department_id:
            department_id = employee.department_id.id
        else:
            department_id = request.env['hr.department'].search([], limit=1).id
        vals = {
            'employee_id': employee.id,
            'department_id': department_id,
            'reason_for_purchase': reason_for_purchase,
        }
        material = request.env['product.purchasing.request'].sudo().create(vals)
        line_vals = {
            'product_id': int(kw.get('product_id')),
            'qty':  kw.get('qty'),
            'cost_price': kw.get('product_id.standard_price.id'),
            'requisition_id': material.id,
            # 'reason_for_purchase': str(kw.get('reason_for_purchase')),

        }
        print(line_vals,33333333333333333333333)
        material_line = request.env['product.purchasing.request.line'].sudo().create(line_vals)
        return request.redirect('/purchase/request/open/%s'%(material.id))

    @http.route(['/purchase/request/add_line/new'], type='http', auth="public", website=True)
    def purchase_request_add_linereq(self, **kw):
        employee = request.env['hr.employee'].search([('user_id', '=', http.request.env.context.get('uid'))], limit=1)
        material = request.env['product.purchasing.request'].sudo().search([('id', '=', int(kw.get('purchase_hid')))])
        line_vals = {
            'product_id': int(kw.get('product_id')),
            'qty': float(kw.get('qty')),
            'cost_price': kw.get('product_id.standard_price.id'),
            'requisition_id': material.id,
            # 'reason_for_purchase': str(kw.get('reason_for_purchase')),
        }
        print(line_vals,222222222222222222)
        material_line = request.env['product.purchasing.request.line'].sudo().create(line_vals)
        return request.redirect('/purchase/request/open/%s'%(material.id))

    @http.route(['/purchase/request/open/<int:material_id>'], type='http', auth="public", website=True)
    def purchase_request_open_ext(self, material_id, access_token=None, **kw, ):
        employee_id = http.request.env.user
        values = {}
        product_id = request.env['product.product'].sudo().search([])
        material = request.env['product.purchasing.request'].sudo().search([('id', '=', material_id)], limit=1)
        values.update({
            'material': material,
            'product_id': product_id,
        })
        print(values,555555555555555555555555555555555)
        return request.render("odoocms_employee_portal.purchase_request_form_template", values)

    @http.route(['/purchase/request/form/submit'], type='http', auth="public", website=True, method=['GET', 'POST'],  portal=True)
    def purchase_request_form_submit(self, **post):
        return request.redirect('/purchase/request/recs')


class CustomerPortal(CustomerPortal):

    @http.route(['/purchase/request/form/back'], type='http', auth="public", website=True, method=['GET'], portal=True)
    def purchase_request_back(self, **post):
        return request.redirect('/purchase/request/form')



