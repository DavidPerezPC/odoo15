# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ResParter(models.Model):
    _inherit = 'res.partner'

    x_current_category = fields.Text(string="Diferencias en etiquetas", compute='_get_current_category')

    def _get_current_category(self):
        for rec in self:
            rec.x_current_category = ''
            categories = []
            if rec.category_id:
                for categ in rec.category_id:
                    categories.append(categ.display_name)
                    # print(categ.name)
                rec.x_current_category = categories

    @api.onchange('category_id')
    def get_category_changes(self):
        try:
            partner_id = ''
            for rec in self:
                for current_id in str(rec.id):
                    if current_id.isdigit():
                        partner_id += current_id
                partner_id = rec.env['res.partner'].search([('id', '=', int(partner_id))],limit=1)
                message = ''
                if rec.x_current_category:
                    current_categories = eval(rec.x_current_category)
                    names = rec.category_id.mapped('display_name')
                    for current_categ in rec.category_id:
                        if current_categ.display_name not in current_categories:
                            message = 'Etiqueta añadida: '
                            message += str(current_categ.display_name)
                            current_categories.append(current_categ.display_name)
                            rec.x_current_category = str(current_categories)
                            partner_id.message_post(body=message)
                    for old_categ in current_categories:
                        if old_categ not in names:
                            message = 'Etiqueta eliminada: '
                            message += str(old_categ)
                            current_categories.remove(old_categ)
                            rec.x_current_category = str(current_categories)
                            partner_id.message_post(body=message)
                elif rec.category_id:
                    current_categories = list()
                    for current_categ in rec.category_id:
                        message = 'Etiqueta añadida: '
                        message += str(current_categ.display_name)
                        current_categories.append(current_categ.display_name)
                        rec.x_current_category = str(current_categories)
                        partner_id.message_post(body=message)
                else:
                    pass
        except Exception as error:
            _logger.info(error)
