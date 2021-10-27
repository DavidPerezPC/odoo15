from odoo import api, fields, models

class ScrapOrders(models.Model):
    _inherit = 'stock.scrap'

    def _get_report_values(self, docids):
        docs = self.env['stock.scrap'].browse(docids)
        return {
            'docs' : docs
        }
