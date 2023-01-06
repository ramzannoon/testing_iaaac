from odoo import http
from odoo.http import content_disposition, Controller, request, route
from datetime import datetime


class HelpdeskTickets(http.Controller):

    @http.route(['/helpdesk/tickets'], type='http', auth="user", website=True, method=['GET'], portal=True)
    def helpdesk_tickets_form(self, **post):
        current_user = http.request.env.user
        # employee_id = request.env['helpdesk.ticket'].sudo().search([('employee_id', '=', current_user.name)])

        department_id = request.env['helpdesk.ticket.team'].sudo().search([])
        categories_id = request.env['helpdesk.ticket.category'].sudo().search([])

        data = {
            'department_id': department_id,
            'categories_id': categories_id,
        }

        return request.render("odoocms_employee_portal.tickets_helpdesk_form", data)

    @http.route(['/helpdesk/tickets/submit'], type='http', auth="user", website=True, method=['GET'], portal=True)
    def helpdesk_tickets_form_submit(self, **post):

        current_user = http.request.env.user
        department = post.get('department_id')
        categories = post.get('categories_id')
        priority = post.get('priority')
        description = post.get('description')

        categories_id = request.env['helpdesk.ticket.category'].sudo().search([('id', '=', categories)])
        department_id = request.env['helpdesk.ticket.team'].sudo().search([('id', '=', department)])

        helpdesk = request.env['helpdesk.ticket'].sudo().create({
            'partner_name': str(current_user.name),
            'name': department_id.name,
            'priority': priority,
            'description': description,
            'category_id': categories_id.id,
            'department_id': department_id.id,

        })
        return request.render("odoocms_employee_portal.tickets_helpdesk_submit", )

    @http.route(['/helpdesk/tickets/recs'], type='http', auth="user", website=True, method=['GET'], portal=True)
    def helpdesk_tickets_recs(self, **post):
        current_user = http.request.env.user

        return request.render("odoocms_employee_portal.tickets_helpdesk_recs", )

    @http.route(['/helpdesk/tickets/back'], type='http', auth="user", website=True, method=['GET'], portal=True)
    def helpdesk_tickets_back(self, **post):
        return request.redirect('/helpdesk/tickets')
