# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class mark_performing_delivery_note_movements(models.Model):    
    _inherit = 'pos.session'
    
    @api.model
    def _mark_state(self, lista):
        try:
            for rec in lista:
                for i in rec.picking_ids:
                    products_qtys = i.move_line_ids_without_package.mapped('product_uom_qty')
                    qtys_dones = i.move_line_ids_without_package.mapped('qty_done')
                    sum_products_qtys = sum(products_qtys)
                    sum_qtys_dones = sum(qtys_dones)
                    if i.state == 'draft':
                        i.action_confirm()
                        i.action_assign()
                        if sum_products_qtys == sum_qtys_dones:                            
                            i.button_validate()
                    elif i.state in ('assigned', 'confirmed'):
                        i.action_assign()
                        if sum_products_qtys == sum_qtys_dones:
                            i.button_validate()
        except Exception as e:
            _logger.info(e)
