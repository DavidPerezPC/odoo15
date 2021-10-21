# -*- coding: utf-8 -*-

from odoo import models, fields, api


class stock_delivery_note_acc(models.Model):
    _inherit = "stock.picking"
    
    # Campo Remision que representa un tipo de documento emitido por el proveedor para validar que el pedido o parte del
    #pedido ha sido recibido
    x_remis = fields.Char('Remision',
                                help='Document type from provider to validate a delivery slip')

    def get_account_stock_account_move_lines(self):
        self.ensure_one()
        vals = []
        for stock_move in self.move_lines:
            for account_move in stock_move.account_move_ids:
                for account_move_line in account_move.line_ids:
                    vals.append({'name': account_move_line.account_id.display_name,
                    'debit': account_move_line.debit,
                    'credit': account_move_line.credit})
        acount_list = set([a.get('name') for a in vals])
        new_vals = []
        for account in acount_list:
            new_vals.append({'name': account,
                    'debit': sum((a.get('name') == account) and a.get('debit') for a in vals),
                    'credit': sum((a.get('name') == account) and a.get('credit') for a in vals)})
        return new_vals
    



    
