# -*- coding: utf-8 -*-
# from odoo import http


# class DeInvoice(http.Controller):
#     @http.route('/de_invoice/de_invoice', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_invoice/de_invoice/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_invoice.listing', {
#             'root': '/de_invoice/de_invoice',
#             'objects': http.request.env['de_invoice.de_invoice'].search([]),
#         })

#     @http.route('/de_invoice/de_invoice/objects/<model("de_invoice.de_invoice"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_invoice.object', {
#             'object': obj
#         })
