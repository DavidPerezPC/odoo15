# -*- coding: utf-8 -*-
# from odoo import http


# class Slaughterhouse(http.Controller):
#     @http.route('/slaughterhouse/slaughterhouse/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/slaughterhouse/slaughterhouse/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('slaughterhouse.listing', {
#             'root': '/slaughterhouse/slaughterhouse',
#             'objects': http.request.env['slaughterhouse.slaughterhouse'].search([]),
#         })

#     @http.route('/slaughterhouse/slaughterhouse/objects/<model("slaughterhouse.slaughterhouse"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('slaughterhouse.object', {
#             'object': obj
#         })
