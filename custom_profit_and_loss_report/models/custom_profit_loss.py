# -*- coding: utf-8 -*-

from odoo import api, models, fields
from datetime import datetime, timedelta
import math
import locale
from dateutil.relativedelta import relativedelta

class CustomProfitAndLoss(models.TransientModel):
    _name = 'custom.profit.loss'
    _description = 'Reporte de estado de la compañía'

    company_id = fields.Many2one('res.company', string='Compañía', default=lambda self: self.env.company.id)
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
        return self.env.ref('custom_profit_and_loss_report.custom_profit_and_loss_report_xlsx').report_action(self)

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

    def get_move_state(self):
        if self.extend_option == 'posted_entries':
            return 'CON ENTRADAS PUBLICADAS'
        else:
            return 'CON ENTRDAS EN BORRADOR'

    def get_move_values(self):
        domain = list()
        domain.append(('date', '>=', self.initial_date))
        domain.append(('date', '<=', self.end_date))
        domain.append(('company_id', '=', self.company_id.id))
        domain.append(('account_id.user_type_id', 'in', (13, 14, 15, 16, 17)))
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

    def get_lines_pdf(self):
        values = self.get_move_values()
        expenses = list()
        exp = list()

        moves = dict(Incomes=None,Discounts=None,Others=None,Costs=None,Depreciations=None,Expenses=None,Total=None)
        expeneses_dict = dict()

        # Variables
        sin_inc, tij_inc, mex_inc, son_inc, nor_inc, eu_inc, occ_inc, bcs_inc, chi_inc, ind_inc = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        sin_des, tij_des, mex_des, son_des, nor_des, eu_des, occ_des, bcs_des, chi_des, ind_des = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        sin_oth, tij_oth, mex_oth, son_oth, nor_oth, eu_oth, occ_oth, bcs_oth, chi_oth, ind_oth = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        sin_cos, tij_cos, mex_cos, son_cos, nor_cos, eu_cos, occ_cos, bcs_cos, chi_cos, ind_cos = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        sin_dep, tij_dep, mex_dep, son_dep, nor_dep, eu_dep, occ_dep, bcs_dep, chi_dep, ind_dep = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        sin_ex, tij_ex, mex_ex, son_ex, nor_ex, eu_ex, occ_ex, bcs_ex, chi_ex, ind_ex = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        for rec in values:
            type_account = rec.account_id.user_type_id.id
            is_disc = rec.account_id.x_is_discount_account
            group = rec.analytic_account_id.group_id.name

            if type_account == 13 and is_disc == False:
                if 'sinaloa' in str(group).lower():
                    sin_inc += rec.debit - rec.credit
                elif 'tijuana' in str(group).lower():
                    tij_inc += rec.debit - rec.credit
                elif 'mexicali' in str(group).lower():
                    mex_inc += rec.debit - rec.credit
                elif 'sonora' in str(group).lower():
                    son_inc += rec.debit - rec.credit
                elif 'noreste' in str(group).lower():
                    nor_inc += rec.debit - rec.credit
                elif 'estados unidos' in str(group).lower():
                    eu_inc += rec.debit - rec.credit
                elif 'occidente' in str(group).lower():
                    occ_inc += rec.debit - rec.credit
                elif 'baja sur' in str(group).lower():
                    bcs_inc += rec.debit - rec.credit
                elif 'chihuahua' in str(group).lower():
                    chi_inc += rec.debit - rec.credit
                # elif 'false' in str(group).lower():
                else:
                    ind_inc += rec.debit - rec.credit

            elif type_account == 13 and is_disc == True:
                if 'sinaloa' in str(group).lower():
                    sin_des += rec.debit - rec.credit
                elif 'tijuana' in str(group).lower():
                    tij_des += rec.debit - rec.credit
                elif 'mexicali' in str(group).lower():
                    mex_des += rec.debit - rec.credit
                elif 'sonora' in str(group).lower():
                    son_des += rec.debit - rec.credit
                elif 'noreste' in str(group).lower():
                    nor_des += rec.debit - rec.credit
                elif 'estados unidos' in str(group).lower():
                    eu_des += rec.debit - rec.credit
                elif 'occidente' in str(group).lower():
                    occ_des += rec.debit - rec.credit
                elif 'baja sur' in str(group).lower():
                    bcs_des += rec.debit - rec.credit
                elif 'chihuahua' in str(group).lower():
                    chi_des += rec.debit - rec.credit
                # elif 'false' in str(group).lower():
                else:
                    ind_des += rec.debit - rec.credit

            elif type_account == 14:
                if 'sinaloa' in str(group).lower():
                    sin_oth += rec.debit - rec.credit
                elif 'tijuana' in str(group).lower():
                    tij_oth += rec.debit - rec.credit
                elif 'mexicali' in str(group).lower():
                    mex_oth += rec.debit - rec.credit
                elif 'sonora' in str(group).lower():
                    son_oth += rec.debit - rec.credit
                elif 'noreste' in str(group).lower():
                    nor_oth += rec.debit - rec.credit
                elif 'estados unidos' in str(group).lower():
                    eu_oth += rec.debit - rec.credit
                elif 'occidente' in str(group).lower():
                    occ_oth += rec.debit - rec.credit
                elif 'baja sur' in str(group).lower():
                    bcs_oth += rec.debit - rec.credit
                elif 'chihuahua' in str(group).lower():
                    chi_oth += rec.debit - rec.credit
                # elif 'false' in str(group).lower():
                else:
                    ind_oth += rec.debit - rec.credit

            elif type_account == 17:
                if 'sinaloa' in str(group).lower():
                    sin_cos += rec.debit - rec.credit
                elif 'tijuana' in str(group).lower():
                    tij_cos += rec.debit - rec.credit
                elif 'mexicali' in str(group).lower():
                    mex_cos += rec.debit - rec.credit
                elif 'sonora' in str(group).lower():
                    son_cos += rec.debit - rec.credit
                elif 'noreste' in str(group).lower():
                    nor_cos += rec.debit - rec.credit
                elif 'estados unidos' in str(group).lower():
                    eu_cos += rec.debit - rec.credit
                elif 'occidente' in str(group).lower():
                    occ_cos += rec.debit - rec.credit
                elif 'baja sur' in str(group).lower():
                    bcs_cos += rec.debit - rec.credit
                elif 'chihuahua' in str(group).lower():
                    chi_cos += rec.debit - rec.credit
                # elif 'false' in str(group).lower():
                else:
                    ind_cos += rec.debit - rec.credit

            elif type_account == 16:
                if 'sinaloa' in str(group).lower():
                    sin_dep += rec.debit - rec.credit
                elif 'tijuana' in str(group).lower():
                    tij_dep += rec.debit - rec.credit
                elif 'mexicali' in str(group).lower():
                    mex_dep += rec.debit - rec.credit
                elif 'sonora' in str(group).lower():
                    son_dep += rec.debit - rec.credit
                elif 'noreste' in str(group).lower():
                    nor_dep += rec.debit - rec.credit
                elif 'estados unidos' in str(group).lower():
                    eu_dep += rec.debit - rec.credit
                elif 'occidente' in str(group).lower():
                    occ_dep += rec.debit - rec.credit
                elif 'baja sur' in str(group).lower():
                    bcs_dep += rec.debit - rec.credit
                elif 'chihuahua' in str(group).lower():
                    chi_dep += rec.debit - rec.credit
                # elif 'false' in str(group).lower():
                else:
                    ind_dep += rec.debit - rec.credit
            elif type_account == 15:
                exp.append(rec)
                account_name = str(rec.account_id.code) + ' ' + str(rec.account_id.name)
                if account_name not in expenses:
                    expenses.append(account_name)
        count = 0
        expenses.sort()
        total_exp = 0
        for account in expenses:
            sin_exp, tij_exp, mex_exp, son_exp, nor_exp, eu_exp, occ_exp, bcs_exp, chi_exp, ind_exp = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            # Imprimimos el nombre de la cuenta
            count += 1
            print(count)
            for rec in exp:
                analytic_distribution = False
                if rec.analytic_tag_ids:
                    for tag in rec.analytic_tag_ids:
                        if tag.active_analytic_distribution:
                            analytic_distribution = True

                group = rec.analytic_account_id.group_id.name
                if rec.account_id.code in account:
                    if not analytic_distribution:
                        if 'sinaloa' in str(group).lower():
                            sin_exp += rec.debit - rec.credit
                        elif 'tijuana' in str(group).lower():
                            tij_exp += rec.debit - rec.credit
                        elif 'mexicali' in str(group).lower():
                            mex_exp += rec.debit - rec.credit
                        elif 'sonora' in str(group).lower():
                            son_exp += rec.debit - rec.credit
                        elif 'noreste' in str(group).lower():
                            nor_exp += rec.debit - rec.credit
                        elif 'estados unidos' in str(group).lower():
                            eu_exp += rec.debit - rec.credit
                        elif 'occidente' in str(group).lower():
                            occ_exp += rec.debit - rec.credit
                        elif 'baja sur' in str(group).lower():
                            bcs_exp += rec.debit - rec.credit
                        elif 'chihuahua' in str(group).lower():
                            chi_exp += rec.debit - rec.credit
                        else:
                        # elif 'false' in str(group).lower():
                            ind_exp += rec.debit - rec.credit
                    else:
                        if rec.analytic_account_id:
                            for line in rec.analytic_line_ids:
                                group_line = line.account_id.group_id.name
                                if not abs(line.amount) == abs(rec.debit - rec.credit):
                                    if 'sinaloa' in str(group_line).lower():
                                        sin_exp += -line.amount
                                    elif 'tijuana' in str(group_line).lower():
                                        tij_exp += -line.amount
                                    elif 'mexicali' in str(group_line).lower():
                                        mex_exp += -line.amount
                                    elif 'sonora' in str(group_line).lower():
                                        son_exp += -line.amount
                                    elif 'noreste' in str(group_line).lower():
                                        nor_exp += -line.amount
                                    elif 'estados unidos' in str(group_line).lower():
                                        eu_exp += -line.amount
                                    elif 'occidente' in str(group_line).lower():
                                        occ_exp += -line.amount
                                    elif 'baja sur' in str(group_line).lower():
                                        bcs_exp += -line.amount
                                    elif 'chihuahua' in str(group_line).lower():
                                        chi_exp += -line.amount
                                    # elif 'false' in str(group_line).lower():
                                    else:
                                        ind_exp += -line.amount
                        else:
                            if rec.analytic_line_ids:
                                for line in rec.analytic_line_ids:
                                    group_line = line.account_id.group_id.name
                                    if 'sinaloa' in str(group_line).lower():
                                        sin_exp += -line.amount
                                    elif 'tijuana' in str(group_line).lower():
                                        tij_exp += -line.amount
                                    elif 'mexicali' in str(group_line).lower():
                                        mex_exp += -line.amount
                                    elif 'sonora' in str(group_line).lower():
                                        son_exp += -line.amount
                                    elif 'noreste' in str(group_line).lower():
                                        nor_exp += -line.amount
                                    elif 'estados unidos' in str(group_line).lower():
                                        eu_exp += -line.amount
                                    elif 'occidente' in str(group_line).lower():
                                        occ_exp += -line.amount
                                    elif 'baja sur' in str(group_line).lower():
                                        bcs_exp += -line.amount
                                    elif 'chihuahua' in str(group_line).lower():
                                        chi_exp += -line.amount
                                    # elif 'false' in str(group_line).lower():
                                    else:
                                        ind_exp += -line.amount
                            else:
                                if 'sinaloa' in str(group).lower():
                                    sin_exp += rec.debit - rec.credit
                                elif 'tijuana' in str(group).lower():
                                    tij_exp += rec.debit - rec.credit
                                elif 'mexicali' in str(group).lower():
                                    mex_exp += rec.debit - rec.credit
                                elif 'sonora' in str(group).lower():
                                    son_exp += rec.debit - rec.credit
                                elif 'noreste' in str(group).lower():
                                    nor_exp += rec.debit - rec.credit
                                elif 'estados unidos' in str(group).lower():
                                    eu_exp += rec.debit - rec.credit
                                elif 'occidente' in str(group).lower():
                                    occ_exp += rec.debit - rec.credit
                                elif 'baja sur' in str(group).lower():
                                    bcs_exp += rec.debit - rec.credit
                                elif 'chihuahua' in str(group).lower():
                                    chi_exp += rec.debit - rec.credit
                                else:
                                # elif 'false' in str(group).lower():
                                    ind_exp += rec.debit - rec.credit

            total_expense = sin_exp + tij_exp + mex_exp + son_exp + nor_exp + eu_exp + occ_exp + bcs_exp + chi_exp + ind_exp
            # Asignamos el valor a variables fuera del for para poder trabajar fuera de el
            sin_ex += sin_exp
            tij_ex += tij_exp
            mex_ex += mex_exp
            son_ex += son_exp
            nor_ex += nor_exp
            eu_ex += eu_exp
            occ_ex += occ_exp
            bcs_ex += bcs_exp
            chi_ex += chi_exp
            ind_ex += ind_exp
            total_exp += total_expense

            # expen.append((sin_exp,tij_exp,mex_exp,son_exp,nor_exp,eu_exp,occ_exp,bcs_exp,chi_exp,ind_exp,total_expense))
            expeneses_dict[account] = (sin_exp,tij_exp,mex_exp,son_exp,nor_exp,eu_exp,occ_exp,bcs_exp,chi_exp,ind_exp,total_expense)


        total_income = sin_inc + tij_inc + mex_inc + son_inc + nor_inc + eu_inc + occ_inc + bcs_inc + chi_inc + ind_inc
        total_discount = sin_des + tij_des + mex_des + son_des + nor_des + eu_des + occ_des + bcs_des + chi_des + ind_des
        total_other = sin_oth + tij_oth + mex_oth + son_oth + nor_oth + eu_oth + occ_oth + bcs_oth + chi_oth + ind_oth
        total_cos = sin_cos + tij_cos + mex_cos + son_cos + nor_cos + eu_cos + occ_cos + bcs_cos + chi_cos + ind_cos
        total_dep = sin_dep + tij_dep + mex_dep + son_dep + nor_dep + eu_dep + occ_dep + bcs_dep + chi_dep + ind_dep

        # TOTALES
        # La sumatoria de los ingresos se toma con el signo contrario para su correcto calculo
        sin_total = -sin_inc - sin_oth - sin_des - sin_cos - sin_ex - sin_dep
        tij_total = -tij_inc - tij_oth - tij_des - tij_cos - tij_ex - tij_dep
        mex_total = -mex_inc - mex_oth - mex_des - mex_cos - mex_ex - mex_dep
        son_total = -son_inc - son_oth - son_des - son_cos - son_ex - son_dep
        nor_total = -nor_inc - nor_oth - nor_des - nor_cos - nor_ex - nor_dep
        eu_total = -eu_inc - eu_oth - eu_des - eu_cos - eu_ex - eu_dep
        occ_total = -occ_inc - occ_oth - occ_des - occ_cos - occ_ex - occ_dep
        bcs_total = -bcs_inc - bcs_oth - bcs_des - bcs_cos - bcs_ex - bcs_dep
        chi_total = -chi_inc - chi_oth - chi_des - chi_cos - chi_ex - chi_dep
        ind_total = -ind_inc - ind_oth - ind_des - ind_cos - ind_ex - ind_dep
        total = -total_income - total_other - total_discount - total_cos - total_exp - total_dep


        moves['Incomes'] = (sin_inc,tij_inc,mex_inc,son_inc,nor_inc,eu_inc,occ_inc,bcs_inc,chi_inc,ind_inc,total_income)
        moves['Discounts'] = (sin_des,tij_des,mex_des,son_des,nor_des,eu_des,occ_des,bcs_des,chi_des,ind_des,total_discount)
        moves['Others'] = (sin_oth,tij_oth,mex_oth,son_oth,nor_oth,eu_oth,occ_oth,bcs_oth,chi_oth,ind_oth,total_other)
        moves['Costs'] = (sin_cos,tij_cos,mex_cos,son_cos,nor_cos,eu_cos,occ_cos,bcs_cos,chi_cos,ind_cos,total_cos)
        moves['Depreciations'] = (sin_dep,tij_dep,mex_dep,son_dep,nor_dep,eu_dep,occ_dep,bcs_dep,chi_dep,ind_dep,total_dep)
        moves['Expenses'] = expeneses_dict
        moves['Total'] = (sin_total,tij_total,mex_total,son_total,nor_total,eu_total,occ_total,bcs_total,chi_total,ind_total,total)

        return moves




