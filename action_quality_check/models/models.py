# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class action_quality_check(models.Model):
    _inherit = 'quality.check'

    def ActionQualityCheck(self):
        search = self.env['quality.check'].search(
            [('quality_state', '=', 'none'), ('test_type_id', '=', 'Register Consumed Materials')])
        for rec in search:
            try:
                rec.do_pass()
            except Exception as e:
                _logger.info(e)
