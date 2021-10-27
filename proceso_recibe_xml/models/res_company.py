from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    x_server_address = fields.Char(string='Servidor', store=True)
    x_database = fields.Char(string='Base de datos externa', store=True)

