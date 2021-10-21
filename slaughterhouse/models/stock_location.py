from odoo import models, fields, api


class StockLocation(models.Model):
    _inherit = 'stock.location'

    is_loss_of_inventories = fields.Boolean(string="Is loss of inventories", default=False, store=True,
                                            help="The purpose of this field is to know if the location is lost from inventory")
