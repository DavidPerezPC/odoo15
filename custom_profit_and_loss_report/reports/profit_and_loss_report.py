from odoo import api, fields, models


class ReportCustomProfitLoss(models.AbstractModel):
    _name = 'report.custom_profit_and_loss_report.custom_profit_and_loss'
    _description = 'Reprte de ganancias y perdidas por zonas'

    def _get_report_values(self, docids, data=None):
        docs = self.env['custom.profit.loss'].browse(docids)

        return {
            'docs' : docs
        }


