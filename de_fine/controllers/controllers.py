# -*- coding: utf-8 -*-
# from odoo import http


# class DeFine(http.Controller):
#     @http.route('/de_fine/de_fine', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_fine/de_fine/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_fine.listing', {
#             'root': '/de_fine/de_fine',
#             'objects': http.request.env['de_fine.de_fine'].search([]),
#         })

#     @http.route('/de_fine/de_fine/objects/<model("de_fine.de_fine"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_fine.object', {
#             'object': obj
#         })
