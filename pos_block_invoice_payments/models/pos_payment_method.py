from odoo import api, fields, models, _
from odoo.exceptions import UserError

class CustomPosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"
    
    instant_payment = fields.Boolean(
        string='Generar pago',
        default=True,
        help='Seleccione para generar el pago.')
    