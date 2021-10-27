from odoo import api, fields, models

class MRPProduction(models.Model):
    _inherit = 'mrp.production'

    state = fields.Selection(selection_add=[('unbuild','Desconstruida')])