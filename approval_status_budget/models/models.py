# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ApprovalStatusBudget(models.Model):
    _inherit = 'purchase.order'

    x_approval_status = fields.Char(string="Estado aprobación", compute="status_budget", store=False)
    x_approval_status_store = fields.Char(string="Estado aprobación", store=True)
    user_approvar = fields.Char(string="Aprobador", compute="status_budget", store=False)
    user_approvar_store = fields.Char(string="Aprobador", store=True)

    @api.depends("user_approvar")
    def status_budget(self):
        search = self.env["purchase.order"].search([])
        for rec in search:
            rec.x_approval_status = ''
            rec.x_approval_status_store = ''
            rec.user_approvar = ''
            rec.user_approvar_store = ''
            try:
                approval_line_entry = self.env['studio.approval.entry'].search(
                    [['res_id', '=', rec.id], ['model', 'like', "purchase.order"]])
                approved = approval_line_entry.approved
                approval = approval_line_entry.user_id.display_name
                rec.user_approvar_store = approval
                if approved:
                    rec.x_approval_status_store = "Aprobado"
                elif not approved and approval_line_entry:
                    rec.x_approval_status_store = "Rechazado"
                else:
                    rec.x_approval_status_store = "En espera de aprobación"
            except Exception as e:
                _logger.info(e)
