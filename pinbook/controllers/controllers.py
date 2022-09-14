# -*- coding: utf-8 -*-
# from odoo import http


# class Pinbook(http.Controller):
#     @http.route('/pinbook/pinbook', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pinbook/pinbook/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pinbook.listing', {
#             'root': '/pinbook/pinbook',
#             'objects': http.request.env['pinbook.pinbook'].search([]),
#         })

#     @http.route('/pinbook/pinbook/objects/<model("pinbook.pinbook"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pinbook.object', {
#             'object': obj
#         })
