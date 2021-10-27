
from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class AccountChangeDate(models.TransientModel):
    _name = 'account.change.date'
    _description = 'Cambio de fecha factura'

    name = fields.Char(string='Asiento contable')
    date = fields.Datetime(string="Fecha de emisión")
    move_id = fields.Many2one('account.move', string="Asiento contable")

    def change_date(self):
        try:
            if self.move_id:
                if self.move_id.edi_state == 'to_send':
                    self.move_id.l10n_mx_edi_post_time = self.date
        except Exception as error:
            _logger.info(error)

