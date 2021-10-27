# -*- coding: utf-8 -*-
'''
    /*************************************************************************
    * Description
    * Se agregó un nuevo método para calcular el importe pagado y rectificado en el modelo account.move
    * 1.0
    * Author:
    * Erick Enrique Abrego Gonzalez
    * Date:
    * 17/06/2021
    *************************************************************************/
'''

from odoo import models, fields, api


class difference_payment_amount(models.Model):
    _inherit = 'account.move'   
    
  

    x_amount_paid = fields.Monetary(string='Cantidad pagada', readonly=True,store=False,
                                 compute='_calculate_amount_paid')
    x_amount_credit_note = fields.Monetary(string='Cantidad rectificada', readonly=True,store=False,
                                        compute='_calculate_amount_credit_note')

    x_amount_paid_value = fields.Monetary(string='Importe pagado',store=True,readonly=True)
    x_amount_credit_note_value = fields.Monetary(string='Importe rectificado', store=True, readonly=True)

   
    
    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id'
    )
    def _calculate_amount_paid(self):
        for move in self:
            move.ensure_one()
            move.x_amount_paid = 0
            move.x_amount_paid_value = 0
            for pay in self._get_reconciled_info_JSON_values():                
                account_id = pay.get('move_id')
                account_id_obj = self.env['account.move'].search([('id','=', account_id )])
                if account_id_obj.move_type == 'entry':
                    move['x_amount_paid'] += pay.get('amount')
                    move['x_amount_paid_value'] += pay.get('amount')
                else:
                    pass

    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id',
    )
    
    def _calculate_amount_credit_note(self):
        for move in self:
            move.ensure_one()
            move.x_amount_credit_note = 0
            move.x_amount_credit_note_value = 0
            for pay in self._get_reconciled_info_JSON_values():               
                account_id = pay.get('move_id')
                account_id_obj = self.env['account.move'].search([('id', '=', account_id)])
                if account_id_obj.move_type == 'out_refund':
                    move['x_amount_credit_note'] += pay.get('amount')
                    move['x_amount_credit_note_value'] += pay.get('amount')
                else:
                    pass
    
    def calculate_credit_note(self):        
        for move in self:
            move.ensure_one()
            note = 0
            for pay in self._get_reconciled_info_JSON_values():
                account_id = pay.get('move_id')
                account_id_obj = self.env['account.move'].search([('id', '=', account_id)])
                if account_id_obj.move_type == 'out_refund':
                    note += pay.get('amount')
                else:
                    pass
            return note

    def calculate_paid(self):
        for move in self:
            move.ensure_one()
            paid = 0
            for pay in self._get_reconciled_info_JSON_values():
                account_id = pay.get('move_id')
                account_id_obj = self.env['account.move'].search([('id','=', account_id )])
                if account_id_obj.move_type == 'entry':
                    paid += pay.get('amount')
                else:
                    pass
            return paid
