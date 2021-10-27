# -*- coding: utf-8 -*-

from odoo import models, fields, api


class add_territory(models.Model):
    _inherit = 'sale.order'

    x_territory = fields.Many2one("zone.pam", related="partner_id.x_zone", string="Territorio", store=True)
    x_sector = fields.Many2one("res.partner.industry", related="partner_id.industry_id", string="Sector", store=True)


class add_sector(models.Model):
    _inherit = 'pos.order'

    x_territory = fields.Many2one("zone.pam", related="partner_id.x_zone", string="Territorio", store=True)
    x_sector = fields.Many2one("res.partner.industry", related="partner_id.industry_id", string="Sector", store=True)
    x_warehouse_id = fields.Many2one("stock.warehouse",related='user_id.property_warehouse_id',string="Almacén", store=True)
    x_warehouse_compute = fields.Many2one("stock.warehouse", compute="_compute_warehouse_id", string="Almacén computado", store=False)
    x_invoice_status = fields.Selection(string="Estado factura", selection=[('invoiced', 'Facturado'), ('to invoice', 'A facturar'), ('no', 'Nada que Facturar')], compute="_def_invoice_status", readonly=True, store=True)
    
    
    @api.depends('state')
    def _def_invoice_status(self):
        for rec in self:
            state_pos = rec.state
            if state_pos:
                if state_pos == "invoiced":
                    rec.x_invoice_status = "invoiced"
                elif state_pos == "paid":
                    rec.x_invoice_status = "to invoice"
                else:
                    rec.x_invoice_status = "no"
            else:
                rec.x_invoice_status = "no"


    @api.depends('user_id')
    def _compute_warehouse_id(self):
        for rec in self:
            if rec.user_id:
                if rec.user_id.property_warehouse_id:
                    rec.x_warehouse_id = rec.user_id.property_warehouse_id
                    rec.x_warehouse_compute = rec.user_id.property_warehouse_id
                    
                else:
                    rec.x_warehouse_id = False
                    rec.x_warehouse_compute = False
                    
            else:
                rec.x_warehouse_id = False
                rec.x_warehouse_compute = False
                



class modify_view_pivot(models.Model):
    _inherit = 'sale.report'

    x_territory = fields.Many2one("zone.pam", string="Territorio", store=True, readonly=True)
    x_sector = fields.Many2one("res.partner.industry", string="Sector", store=True, readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):

        fields['x_territory'] = ", s.x_territory as x_territory"
        fields['x_sector'] = ", s.x_sector as x_sector"
        fields['warehouse_id'] = ",pos.x_warehouse_id AS warehouse_id"
        fields['invoice_status'] = ",pos.x_invoice_status AS invoice_status"
        groupby += ',s.x_territory,s.x_sector'
        res = super(modify_view_pivot, self)._query(with_clause, fields, groupby, from_clause)
        res = res.replace('NULL AS invoice_status', 'pos.x_invoice_status AS invoice_status')
        res = res.replace('NULL AS warehouse_id','pos.x_warehouse_id AS warehouse_id')
        res = res.replace('NULL AS x_territory','pos.x_territory AS x_territory')
        res = res.replace('NULL AS x_sector','pos.x_sector AS x_sector')
        res = res[:-1] + ',\n\tpos.x_warehouse_id,pos.x_territory,pos.x_sector,pos.x_invoice_status\n)'
        return res


class ReportPosOrder(models.Model):
    _inherit = 'report.pos.order'

    x_territory = fields.Many2one("zone.pam", string="Territorio", store=True, readonly=True)
    x_sector = fields.Many2one("res.partner.industry", string="Sector", store=True, readonly=True)
    x_warehouse_id = fields.Many2one("stock.warehouse", string="Almacén", store=True, readonly=True)


    def _select(self):
        return super(ReportPosOrder, self)._select() + ", s.x_territory, s.x_sector, s.x_warehouse_id"



