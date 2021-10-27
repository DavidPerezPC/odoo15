# -*- coding: utf-8 -*-
'''
    /*************************************************************************
    * Description
     - Se modificó el método '_create_payments' del modelo 'account.payment.register' para que asignara
       correctamente el valor seleccionado en la forma de pago.
    * VERSION
      1.1
    * Author:
      Erick Enrique Abrego Gonzalez
    * Date:
      19/07/2021
    *************************************************************************/
'''
from odoo import models, fields, api

class custom_get_correct_payment_method(models.TransientModel):
    _inherit = 'account.payment.register'

    def _create_payments(self):
        payments = super(custom_get_correct_payment_method, self)._create_payments()
        for i in payments:
            i.l10n_mx_edi_payment_method_id = self.l10n_mx_edi_payment_method_id.id
        return payments