# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_held_order = fields.Boolean(string='Orden retenida', compute='_compute_held_order', store=True)

    @api.depends('partner_id','x_studio_facturas_vencidas', 'x_studio_precio_modificado', 'x_studio_credito_excedido')
    def _compute_held_order(self):
        for rec in self:
            rec.x_held_order = False
            is_price_upd = rec.x_studio_precio_modificado
            is_invoice_exp = rec.x_studio_facturas_vencidas
            is_credit_exc = rec.x_studio_credito_excedido

            if rec.partner_id.is_company:
                partner = rec.partner_id
            else:
                partner = rec.partner_id.parent_id

            tags = []
            price_changes = []
            expired_invoices = []
            exceeded_credit = []
            for categ in partner.category_id:
                print(categ.display_name)
                if categ.parent_id.name == 'Excluir retención por':
                    tags.append(categ)
            if tags:
                for tag in tags:
                    if tag.name == 'Cambio de precio':
                        price_changes.append(tag)
                    elif tag.name == 'Facturas vencidas':
                        expired_invoices.append(tag)
                    elif tag.name == 'Límite de crédito':
                        exceeded_credit.append(tag)
            else:
                if is_price_upd or is_credit_exc or is_invoice_exp:
                    rec.x_held_order = True

            if price_changes and not expired_invoices and not exceeded_credit:
                if is_price_upd and not (is_invoice_exp or is_credit_exc):
                    rec.x_held_order = False
                if is_invoice_exp:
                    rec.x_held_order = True
                if is_credit_exc:
                    rec.x_held_order = True

            elif price_changes and expired_invoices and not exceeded_credit:
                if is_price_upd and not is_credit_exc:
                    rec.x_held_order = False
                if is_invoice_exp and not is_credit_exc:
                    rec.x_held_order = False
                if is_credit_exc:
                    rec.x_held_order = True

            elif not price_changes and expired_invoices and not exceeded_credit:
                if is_price_upd:
                    rec.x_held_order = True
                if is_invoice_exp and not is_credit_exc and not is_price_upd:
                    rec.x_held_order = False
                if is_credit_exc:
                    rec.x_held_order = True

            elif not price_changes and not expired_invoices and exceeded_credit:
                if is_price_upd:
                    rec.x_held_order = True
                if is_invoice_exp:
                    rec.x_held_order = True
                if is_credit_exc and not is_invoice_exp and not is_price_upd:
                    rec.x_held_order = False
            elif not price_changes and expired_invoices and exceeded_credit:
                if is_price_upd:
                    rec.x_held_order = True
                if is_invoice_exp and not is_price_upd:
                    rec.x_held_order = False
                if is_credit_exc and not is_price_upd:
                    rec.x_held_order = False
