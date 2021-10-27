# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class contact_different_define(models.Model):
    _inherit = 'res.partner'

    @api.constrains('property_payment_term_id', 'x_l10n_mx_edi_payment_method_id')
    def diferent_way_to_pay(self):
        for rec in self:
            payment_terms = rec.property_payment_term_id.name
            way_to_pay = rec.x_l10n_mx_edi_payment_method_id.name
            if payment_terms and way_to_pay:
                if payment_terms == "Contado" and way_to_pay == "Por definir":
                    raise UserError("Un cliente de " + "\'" + payment_terms + "\'" + " no puede tener forma de pago " + "\'" +way_to_pay + "\'")
                if payment_terms != "Contado" and way_to_pay != "Por definir":
                    raise UserError("Un cliente de 'Credito' solo puede tener forma de pago 'Por definir'.")
                else:
                    pass
            else:
                pass
