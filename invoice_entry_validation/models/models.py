# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class invoice_entry_validation(models.Model):    
    _inherit = 'account.move'

    @api.constrains('partner_id', 'x_delivery_reference')
    def alert_user_invoice(self):
        for rec in self:
            coincidences = self.env['account.move'].search(
                [('x_delivery_reference', '=', rec.x_delivery_reference), ('x_delivery_reference', '!=', False),
                 ('partner_id', '=', rec.partner_id.id), ('move_type', '=', 'out_invoice')])
            for i in coincidences:
                if i.x_delivery_reference != '0':
                    if len(coincidences) >= 2:
                        data = coincidences[1]
                        if len(coincidences) > 1:
                            raise UserError('El folio de entrada: ' + str(data.x_delivery_reference) +
                                            ' ya se encuentra relacionado con la factura: ' + str(data.name) +
                                            ' y no se permite generar dos documentos con la misma entrada, favor de validar.')

