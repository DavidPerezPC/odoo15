# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import datetime, timedelta
import math
import locale

from dateutil.relativedelta import relativedelta


class CustomProfitAndLoss(models.TransientModel):
    _name = 'custom.profit.loss'
    _description = 'Reporte de estado de la compañía'

    company_id = fields.Many2one('res.company', string='Compañía', default=lambda self: self.env.company)
    account_period = fields.Selection(string='Periodo contable', selection=[
        ('current_month', 'Este mes'),
        ('current_trimester', 'Este trimeste'),
        ('current_year', 'Este año financiero'),
        ('last_month', 'Último mes'),
        ('last_quarter', 'Último cuarto'),
        ('last_year', 'Último año fiscal'),
        ('custom', 'Perzonalizado')
    ], default='current_month')
    comparison = fields.Selection(string='Comparación', selection=[
        ('without_comparison', 'Sin comparación'),
        ('previous_period', 'Periodo previo'),
        ('same_period', 'Mismo periodo del último año'),
        ('custom', 'Perzonalizado')
    ], default='without_comparison')
    extend_option = fields.Selection(string='Opciones de filtrado', selection=[
        ('posted_entries', 'Solo entradas publicadas'),
        ('all', 'Incluir entradas no publicadas')
    ], default="posted_entries")
    zone_filter = fields.Selection(string='Tipo de reporte', selection=[
        ('zone', 'Por zonas'),
    ], default='zone')

    account_analytic_ids = fields.Many2many('account.analytic.account', string='Cuentas bancarias')
    account_journal_ids = fields.Many2many('account.journal', string='Diarios')
    account_analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Categoría')
    initial_date = fields.Date(string="Fecha inicial del periodo")
    end_date = fields.Date(string='Fecha final del periodo')
    initial_date_comparison = fields.Date(string="Fecha inicial del periodo")
    end_date_comparison = fields.Date(string='Fecha final del periodo')
    number_of_periods = fields.Integer(string='Número de periodos')

    def print_report(self):
        return self.env.ref('custom_profit_and_loss_report.custom_profit_and_loss_report').report_action(self)

    def export_xlsx(self):
        return {
            'type': 'ir_actions_account_report_download',
            'data': {'model': self.env.context.get('model'),
                     'output_format': 'xlsx',
                     'financial_id': self.env.context.get('id'),
                     }
        }

    @api.onchange('account_period')
    def _calculate_initial_date(self):
        if self.account_period == 'current_month':
            self.initial_date = datetime.today().replace(day=1)
            self.end_date = self.initial_date + relativedelta(months=1) - timedelta(days=1)
        elif self.account_period == 'current_trimester':
            self.initial_date = datetime.today().replace(day=1) - relativedelta(months=2)
            self.end_date = self.initial_date + relativedelta(months=3) - timedelta(days=1)
        elif self.account_period == 'current_year':
            self.initial_date = datetime.today().replace(day=1, month=1)
            self.end_date = datetime.today().replace(day=31, month=12)
        elif self.account_period == 'last_month':
            self.initial_date = datetime.today().replace(day=1) - relativedelta(months=1)
            self.end_date = datetime.today().replace(day=1) - timedelta(days=1)
        elif self.account_period == 'last_quarter':
            initial_quarter = math.ceil(datetime.today().month / 3.)
            if initial_quarter == 1:
                self.initial_date = datetime.today().replace(day=1, month=10) - relativedelta(years=1)
                self.end_date = datetime.today().replace(day=31, month=12) - relativedelta(years=1)
            elif initial_quarter == 2:
                self.initial_date = datetime.today().replace(day=1, month=1)
                self.end_date = datetime.today().replace(day=31, month=3)
            elif initial_quarter == 3:
                self.initial_date = datetime.today().replace(day=1, month=4)
                self.end_date = datetime.today().replace(day=30, month=6)
            else:
                self.initial_date = datetime.today().replace(day=1, month=7)
                self.end_date = datetime.today().replace(day=30, month=9)
        elif self.account_period == 'last_year':
            self.initial_date = datetime.today().replace(day=1, month=1) - relativedelta(years=1)
            self.end_date = self.initial_date.replace(day=31, month=12)
        else:
            pass

    def get_account_tags(self):
        tag_names = ''
        for i, tag in enumerate(self.account_analytic_tag_ids):
            result = ''.join([a for a in tag.name if not a.isdigit()])
            if i == 0:
                tag_names = tag_names + result
            else:
                tag_names = tag_names + ' y ' + result
        return str(tag_names).upper()

    def get_date(self):
        date = ''
        locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))
        if self.account_period == 'current_month' or self.account_period == 'last_month':
            initial_date = self.initial_date.strftime("%B")
            return ' al mes de ' + initial_date
        else:
            initial_date = self.initial_date.strftime("%d de %B del %Y")
            end_date = self.end_date.strftime("%d de %B del %Y")
            date_range = ' del ' + initial_date + ' al ' + end_date
            return date_range

    def get_move_values(self, type):
        domain = list()
        domain.append(('date', '>=', self.initial_date))
        domain.append(('date', '<=', self.end_date))
        domain.append(('company_id', '=', self.env.company.id))
        domain.append(('account_id.user_type_id.name', '=', type))
        if self.extend_option == 'posted_entries':
            domain.append(('parent_state', '=', 'posted'))
        else:
            domain.append(('parent_state', 'in', ('posted', 'draft')))
        if self.account_journal_ids:
            domain.append(('journal_id', '=', self.account_journal_ids.ids))
        if self.account_analytic_ids:
            domain.append(('analytic_account_id', '=', self.account_analytic_ids.ids))
        if self.account_analytic_tag_ids:
            domain.append(('analytic_tag_ids', '=', self.account_analytic_tag_ids.ids))

        account_move_line = self.env['account.move.line'].search(domain)
        return account_move_line

    def calculate_amount(self, zone=None, type=None, discount=None,account=None):
        moves = self.get_move_values(type)
        amount = 0
        for move in moves:
            if account:
                if discount == False:
                    if (move.account_id.user_type_id.name == type and str(zone) in str(
                            move.analytic_account_id.group_id.name).lower()
                            and move.account_id.is_discount_account == False and move.account_id == account):
                        amount += move.amount_currency
                else:
                    if (move.account_id.user_type_id.name == type and str(zone) in str(
                            move.analytic_account_id.group_id.name).lower()
                            and move.account_id.is_discount_account == True and move.account_id == account):
                        amount += move.amount_currency
            else:
                if discount == False:
                    if (move.account_id.user_type_id.name == type and str(zone) in str(
                            move.analytic_account_id.group_id.name).lower()
                            and move.account_id.is_discount_account == False):
                        amount += move.amount_currency
                else:
                    if (move.account_id.user_type_id.name == type and str(zone) in str(
                            move.analytic_account_id.group_id.name).lower()
                            and move.account_id.is_discount_account == True):
                        amount += move.amount_currency

        return round(amount, 2)





