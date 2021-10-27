from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    x_order_customer_date = fields.Date(string="Fecha orden de compra")

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        try:
            if self.x_order_customer_date:
                res['x_order_reference_date'] = self.x_order_customer_date
            if self.x_order_reference:
                res['x_order_reference'] = self.x_order_reference
        except Exception as error:
            _logger.info(error)
        return res