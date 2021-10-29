# -*- coding: utf-8 -*-
# from odoo import http


# class Stall(http.Controller):
#     @http.route('/stall/stall/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stall/stall/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stall.listing', {
#             'root': '/stall/stall',
#             'objects': http.request.env['stall.stall'].search([]),
#         })

#     @http.route('/stall/stall/objects/<model("stall.stall"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stall.object', {
#             'object': obj
#         })
