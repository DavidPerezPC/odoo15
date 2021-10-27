from odoo import api, fields, models,_

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def link_sale_to_invoice(self):
        return {
            'name': _('Enlace a factura'),
            'res_model': 'link.sale.to.invoice',
            'view_mode': 'form',
            'context': {'default_sale_order':self.id},
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
