from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError
import math
from datetime import datetime, date, timedelta
from pytz import timezone
from dateutil.relativedelta import relativedelta


class StockGenerateReport(models.Model):
    _name = 'stock.generate.report'
    _description = 'Ventana para llenar campos de fecha inicial y final'
    
    @api.constrains('months')
    def _check_valid_date(self):
        if self.months < 0:
            raise ValidationError('No es posible asignar valores negativos a los meses')
    

    def _get_actual_date(self):
        user_tz = self.env.user.tz
        today = datetime.now().astimezone(timezone(user_tz)).date()
        return today

    initial_date = fields.Date(string="Fecha inicial", compute='_get_initial_date')
    end_date = fields.Date(string="Fecha final", required=True, default=_get_actual_date)
    location_id = fields.Many2many('stock.location', string="Ubicación")
    category = fields.Many2many('product.category', string="Categoria")
    product_ids = fields.Many2many('product.product', string='Producto')
    inventory_lines = fields.One2many('stock.duration.days', 'inventory_id',
                                      string="Lineas de inventario", order='order_by')
    company_id = fields.Many2one('res.company', string='Compañia', default=lambda self: self.env.company)
    months = fields.Integer(string="Consumo en meses", readonly=False, default=1, min=1)
    out_of_stock = fields.Boolean(string='Producto sin existencia', default=False)
    consumption_in_months = fields.Boolean(string='En consumo en meses', default=True)
    options_order_by = fields.Selection(string="Opciones de ordenado", selection=[
        ('qty_product', 'Cantidad de producto'),
        ('category', 'Categoría'),
    ])
    type_order_by = fields.Selection(string="Tipo", selection=[
        ('asc', 'Ascendente'),
        ('desc', 'Descendente')
    ])
    order_by = fields.Char(string='Ordenar por', compute='_get_order_by', store=False)

    @api.depends('end_date')
    @api.onchange('months', 'consumption_in_months', 'end_date')
    def _get_initial_date(self):        
        user_tz = self.env.user.tz
        if self.end_date:            
            if self.months == 0:
                date_month_ago = self.end_date - relativedelta(months=0)
                self.initial_date = date_month_ago
            else:
                if self.consumption_in_months:
                    self.initial_date = self.end_date - relativedelta(months=self.months)
        else:
            self.initial_date = datetime.now().astimezone(timezone(user_tz)).date() - relativedelta(months=self.months)

    @api.onchange('options_order_by', 'type_order_by')
    def _get_order_by(self):
        type = self.type_order_by
        if self.options_order_by == 'qty_product':
            self.order_by = 'location_id {}, available_quantity {}'.format(type, type)
        elif self.options_order_by == 'category':
            self.order_by = 'location_id {}, product_uom_id {}'.format(type, type)
        else:
            self.order_by = 'location_id {}'.format(type)

    def load_inventory(self):
        stock_duration_days_obj = self.env['stock.duration.days'].search([])
        stock_duration_days_obj.unlink()
        self.inventory_lines = [((5, 0, 0))]
        self.calculate_inventory(self.location_id, self.category, self.product_ids)

    def calculate_inventory(self, location, category, products):
        domain_stock_quant = []
        domain_stock_quant.append(('location_id.usage', '=', 'internal'))
        domain_stock_quant.append(('company_id','=', self.company_id.id))
        if location:
            domain_stock_quant.append(('location_id', '=', location.ids))
        if category:
            domain_stock_quant.append(('product_id.categ_id', '=', category.ids))
        if products:
            domain_stock_quant.append(('product_id', '=', products.ids))
        if self.out_of_stock:
            domain_stock_quant.append('|')
            domain_stock_quant.append(('quantity', '<=', 0))
            domain_stock_quant.append(('quantity', '>=', 0))
        else:
            domain_stock_quant.append(('quantity', '>', 0))

        stock_quant_obj = self.env['stock.quant'].search(domain_stock_quant)
        lines = []
        for i in stock_quant_obj:
            reserved_ids = self.env['stock.move.line'].search([('state', 'in', ('assigned','partially_available')),
                 ('product_id', '=', i.product_id.id),
                 ('location_id', '=', i.location_id.id),('company_id','=', self.company_id.id)])
            pending_supply = self.env['stock.move'].search(
                [('state', 'not in', ('done','cancel')),
                 ('product_id', '=', i.product_id.id),
                 ('location_id', '=', i.location_id.id),('company_id','=', self.company_id.id)])
            qty_done = self.env['stock.move.line'].search(
                [('state', '=', 'done'),
                 ('product_id', '=', i.product_id.id),
                 ('location_id', '=', i.location_id.id),
                 ('date', '>=', self.initial_date),
                 ('date', '<=', self.end_date),('company_id','=', self.company_id.id)])

            pending_supply_qty = 0.0
            qty_done_value = 0.0
            duration_days = 0

            for move in pending_supply:
                pending_supply_qty += move.product_uom_qty

            for move in qty_done:
                qty_done_value += move.qty_done

            daily_consumption = self.end_date - self.initial_date
            qty = qty_done_value / daily_consumption.days

            if i.quantity > 0 and qty > 0:
                duration_days = i.available_quantity / qty
                if duration_days < 0:
                    duration_days = abs(duration_days)
                decimal_part, int_part = math.modf(duration_days)
                if decimal_part >= 0.5:
                    duration_days = math.ceil(duration_days)
                else:
                    duration_days = int_part

            values = {
                'default_code': i.product_id.default_code,
                'product_id': i.product_id.name,
                'category': i.product_id.categ_id.name,
                'qty_on_hand': round(i.quantity, 2),
                'qty_pendding_supply': round(i.reserved_quantity, 2),
                'qty_per_supply': round(pending_supply_qty,2),
                'qty_product': round(i.available_quantity, 2),
                'daily_consumption_average': round(qty, 2),
                'duration_days': duration_days,
                'product_uom': i.product_uom_id.name,
                'location_id': i.location_id.id,
                'pendding_supply_ids' : reserved_ids.filtered(lambda line: line.state in ('assigned','partially_available')),
                'reserved_ids' : pending_supply.filtered(lambda  line: line.state not in ('done','cancel'))
            }
            lines.append((0, 0, values))
        self.inventory_lines = lines

    def print_report(self):
        return self.env.ref('stock_duration_days.inventory_moves_report').report_action(self)

    def export_report(self):
        return self.env.ref('stock_duration_days.export_inventory_xlsx').report_action(self)