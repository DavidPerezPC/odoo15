from odoo import api, fields, models,_


class CustomLinkPosToInvoice(models.TransientModel):
    _name = 'link.pos.to.invoice'
    _description = 'Enlazar ventas del POS con facturas'

    invoice = fields.Many2one('account.move',string='Factura')
    pos_order = fields.Many2one('pos.order',string='Venta')

    def link_pos(self):
        if self.invoice and self.pos_order:
            self.invoice.invoice_origin = self.pos_order.name
            self.pos_order.account_move = self.invoice.id


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def link_pos_to_invoice(self):
        return {
            'name': _('Enlace a factura'),
            'res_model': 'link.pos.to.invoice',
            'view_mode': 'form',
            'context': {'default_pos_order':self.id},
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
