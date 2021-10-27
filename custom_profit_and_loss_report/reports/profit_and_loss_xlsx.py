from odoo import api, fields, models


class ProffitAndLossXLSX(models.AbstractModel):
    _name = 'report.custom_profit_and_loss_report.prof_and_loss_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Reporte de ganancias y perdidas en XLSX'
    
    def generate_xlsx_report(self, workbook, data, lines):
        # Formato de celdas
        header_format = workbook.add_format({'font_size': 13, 'align': 'center', 'font_color': '#ba8328', 'border': 1})
        header_date_format = workbook.add_format({'font_size': 11, 'align': 'center', 'font_color': '#595959'})
        header_columns_format = workbook.add_format(
            {'font_size': 9, 'align': 'center', 'font_color': '#ba8328', 'border': 1})
        header_account_type_format = workbook.add_format(
            {'font_size': 9, 'align': 'left', 'font_color': '#595959', 'bold': True})
        concept_body_format = workbook.add_format({'font_size': 10, 'align': 'left', 'font_color': '#595959'})
        values_body_format = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'font_color': '#595959', 'num_format': '#,##0.00'})
        # Creación de nuestra hoja de excel
        sheet = workbook.add_worksheet('Reporte')

        # Anchura de columnas
        sheet.set_column(0, 0, 2)
        sheet.set_column(1, 1, 50)
        sheet.set_column(2, 2, 12)
        sheet.set_column(2, 12, 12)

        # Titulo principal
        sheet.merge_range('B2:M2', self.get_main_header(lines), header_format)
        # Titulo con rango de fecha
        date_header = 'Correspondiente ' + str(lines.get_date())
        sheet.merge_range('B3:M3', date_header, header_date_format)
        # Titulo de columnas
        sheet.write('B4', 'CONCEPTO', header_columns_format)
        sheet.write('C4', 'SINALOA', header_columns_format)
        sheet.write('D4', 'BCN TIJUANA', header_columns_format)
        sheet.write('E4', 'BCN MEXICALI', header_columns_format)
        sheet.write('F4', 'SONORA', header_columns_format)
        sheet.write('G4', 'NORESTE', header_columns_format)
        sheet.write('H4', 'E.U', header_columns_format)
        sheet.write('I4', 'OCCIDENTE', header_columns_format)
        sheet.write('J4', 'BCS', header_columns_format)
        sheet.write('K4', 'CHIHUAHUA', header_columns_format)
        sheet.write('L4', 'INDEFINIDO', header_columns_format)
        sheet.write('M4', 'TOTAL', header_columns_format)

        # Llenar campos
        sheet.merge_range('B5:M5', 'INGRESOS', header_account_type_format)
        sheet.merge_range('B9:M9', 'COSTOS', header_account_type_format)
        sheet.merge_range('B11:M11', 'OTROS INGRESOS', header_account_type_format)
        sheet.merge_range('B13:M13', 'AMORTIZACIÓN', header_account_type_format)
        sheet.merge_range('B15:M15', 'GASTOS', header_account_type_format)

        values = lines.get_move_values()

        # Variables
        sin_inc, tij_inc, mex_inc, son_inc, nor_inc, eu_inc, occ_inc, bcs_inc, chi_inc, ind_inc = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        sin_des, tij_des, mex_des, son_des, nor_des, eu_des, occ_des, bcs_des, chi_des, ind_des = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        sin_oth, tij_oth, mex_oth, son_oth, nor_oth, eu_oth, occ_oth, bcs_oth, chi_oth, ind_oth = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        sin_cos, tij_cos, mex_cos, son_cos, nor_cos, eu_cos, occ_cos, bcs_cos, chi_cos, ind_cos = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        sin_dep, tij_dep, mex_dep, son_dep, nor_dep, eu_dep, occ_dep, bcs_dep, chi_dep, ind_dep = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        sin_ex, tij_ex, mex_ex, son_ex, nor_ex, eu_ex, occ_ex, bcs_ex, chi_ex, ind_ex = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        expenses = list()
        exp = list()
        territories = ['sinaloa', 'tijuana', 'mexicali', 'sonora', 'noreste', 'estados unidos', 'occidente', 'baja sur',
                       'chihuahua']

        for rec in values:
            group = rec.analytic_account_id.group_id.name
            type_account = rec.account_id.user_type_id.id
            is_disc = rec.account_id.x_is_discount_account
            # Ventas
            if 'sinaloa' in str(group).lower() and type_account == 13 and is_disc == False:
                sin_inc += rec.debit - rec.credit
            elif 'tijuana' in str(group).lower() and type_account == 13 and is_disc == False:
                tij_inc += rec.debit - rec.credit
            elif 'mexicali' in str(group).lower() and type_account == 13 and is_disc == False:
                mex_inc += rec.debit - rec.credit
            elif 'sonora' in str(group).lower() and type_account == 13 and is_disc == False:
                son_inc += rec.debit - rec.credit
            elif 'noreste' in str(group).lower() and type_account == 13 and is_disc == False:
                nor_inc += rec.debit - rec.credit
            elif 'estados unidos' in str(group).lower() and type_account == 13 and is_disc == False:
                eu_inc += rec.debit - rec.credit
            elif 'occidente' in str(group).lower() and type_account == 13 and is_disc == False:
                occ_inc += rec.debit - rec.credit
            elif 'baja sur' in str(group).lower() and type_account == 13 and is_disc == False:
                bcs_inc += rec.debit - rec.credit
            elif 'chihuahua' in str(group).lower() and type_account == 13 and is_disc == False:
                chi_inc += rec.debit - rec.credit
            elif str(group).lower() not in territories and type_account == 13 and is_disc == False:
                ind_inc += rec.debit - rec.credit
            # Descuentos
            elif 'sinaloa' in str(group).lower() and type_account == 13 and is_disc == True:
                sin_des += rec.debit - rec.credit
            elif 'tijuana' in str(group).lower() and type_account == 13 and is_disc == True:
                tij_des += rec.debit - rec.credit
            elif 'mexicali' in str(group).lower() and type_account == 13 and is_disc == True:
                mex_des += rec.debit - rec.credit
            elif 'sonora' in str(group).lower() and type_account == 13 and is_disc == True:
                son_des += rec.debit - rec.credit
            elif 'noreste' in str(group).lower() and type_account == 13 and is_disc == True:
                nor_des += rec.debit - rec.credit
            elif 'estados unidos' in str(group).lower() and type_account == 13 and is_disc == True:
                eu_des += rec.debit - rec.credit
            elif 'occidente' in str(group).lower() and type_account == 13 and is_disc == True:
                occ_des += rec.debit - rec.credit
            elif 'baja sur' in str(group).lower() and type_account == 13 and is_disc == True:
                bcs_des += rec.debit - rec.credit
            elif 'chihuahua' in str(group).lower() and type_account == 13 and is_disc == True:
                chi_des += rec.debit - rec.credit
            elif str(group).lower() not in territories and type_account == 13 and is_disc == True:
                ind_des += rec.debit - rec.credit
            # OTROS INGRESOS
            elif 'sinaloa' in str(group).lower() and type_account == 14:
                sin_oth += rec.debit - rec.credit
            elif 'tijuana' in str(group).lower() and type_account == 14:
                tij_oth += rec.debit - rec.credit
            elif 'mexicali' in str(group).lower() and type_account == 14:
                mex_oth += rec.debit - rec.credit
            elif 'sonora' in str(group).lower() and type_account == 14:
                son_oth += rec.debit - rec.credit
            elif 'noreste' in str(group).lower() and type_account == 14:
                nor_oth += rec.debit - rec.credit
            elif 'estados unidos' in str(group).lower() and type_account == 14:
                eu_oth += rec.debit - rec.credit
            elif 'occidente' in str(group).lower() and type_account == 14:
                occ_oth += rec.debit - rec.credit
            elif 'baja sur' in str(group).lower() and type_account == 14:
                bcs_oth += rec.debit - rec.credit
            elif 'chihuahua' in str(group).lower() and type_account == 14:
                chi_oth += rec.debit - rec.credit
            elif str(group).lower() not in territories and type_account == 14:
                ind_oth += rec.debit - rec.credit
            # Costo de ventas
            elif 'sinaloa' in str(group).lower() and type_account == 17:
                sin_cos += rec.debit - rec.credit
            elif 'tijuana' in str(group).lower() and type_account == 17:
                tij_cos += rec.debit - rec.credit
            elif 'mexicali' in str(group).lower() and type_account == 17:
                mex_cos += rec.debit - rec.credit
            elif 'sonora' in str(group).lower() and type_account == 17:
                son_cos += rec.debit - rec.credit
            elif 'noreste' in str(group).lower() and type_account == 17:
                nor_cos += rec.debit - rec.credit
            elif 'estados unidos' in str(group).lower() and type_account == 17:
                eu_cos += rec.debit - rec.credit
            elif 'occidente' in str(group).lower() and type_account == 17:
                occ_cos += rec.debit - rec.credit
            elif 'baja sur' in str(group).lower() and type_account == 17:
                bcs_cos += rec.debit - rec.credit
            elif 'chihuahua' in str(group).lower() and type_account == 17:
                chi_cos += rec.debit - rec.credit
            elif str(group).lower() not in territories and type_account == 17:
                ind_cos += rec.debit - rec.credit
            # Amortización
            elif 'sinaloa' in str(group).lower() and type_account == 16:
                sin_dep += rec.debit - rec.credit
            elif 'tijuana' in str(group).lower() and type_account == 16:
                tij_dep += rec.debit - rec.credit
            elif 'mexicali' in str(group).lower() and type_account == 16:
                mex_dep += rec.debit - rec.credit
            elif 'sonora' in str(group).lower() and type_account == 16:
                son_dep += rec.debit - rec.credit
            elif 'noreste' in str(group).lower() and type_account == 16:
                nor_dep += rec.debit - rec.credit
            elif 'estados unidos' in str(group).lower() and type_account == 16:
                eu_dep += rec.debit - rec.credit
            elif 'occidente' in str(group).lower() and type_account == 16:
                occ_dep += rec.debit - rec.credit
            elif 'baja sur' in str(group).lower() and type_account == 16:
                bcs_dep += rec.debit - rec.credit
            elif 'chihuahua' in str(group).lower() and type_account == 16:
                chi_dep += rec.debit - rec.credit
            elif str(group).lower() not in territories and type_account == 16:
                ind_dep += rec.debit - rec.credit
            # Creamos una lista con solo gastos
            elif type_account == 15:
                exp.append(rec)
                account_name = str(rec.account_id.code) + ' ' + str(rec.account_id.name)
                if account_name not in expenses:
                    expenses.append(account_name)

        # Obtención de totales
        total_income = sin_inc + tij_inc + mex_inc + son_inc + nor_inc + eu_inc + occ_inc + bcs_inc + chi_inc + ind_inc
        total_discount = sin_des + tij_des + mex_des + son_des + nor_des + eu_des + occ_des + bcs_des + chi_des + ind_des
        total_other = sin_oth + tij_oth + mex_oth + son_oth + nor_oth + eu_oth + occ_oth + bcs_oth + chi_oth + ind_oth
        total_cos = sin_cos + tij_cos + mex_cos + son_cos + nor_cos + eu_cos + occ_cos + bcs_cos + chi_cos + ind_cos
        total_dep = sin_dep + tij_dep + mex_dep + son_dep + nor_dep + eu_dep + occ_dep + bcs_dep + chi_dep + ind_dep

        # Impresión de ventas en el xlsx
        sheet.write('B6', 'Ventas Totales', concept_body_format)
        sheet.write('C6', abs(sin_inc) + abs(sin_des), values_body_format)
        sheet.write('D6', abs(tij_inc) + abs(tij_des), values_body_format)
        sheet.write('E6', abs(mex_inc) + abs(mex_des), values_body_format)
        sheet.write('F6', abs(son_inc) + abs(son_des), values_body_format)
        sheet.write('G6', abs(nor_inc) + abs(nor_des), values_body_format)
        sheet.write('H6', abs(eu_inc) + abs(eu_des), values_body_format)
        sheet.write('I6', abs(occ_inc) + abs(occ_des), values_body_format)
        sheet.write('J6', abs(bcs_inc) + abs(bcs_des), values_body_format)
        sheet.write('K6', abs(chi_inc) + abs(chi_des), values_body_format)
        sheet.write('L6', abs(ind_inc) + abs(ind_des), values_body_format)
        sheet.write('M6', abs(total_income) + abs(total_discount), values_body_format)
        # Impresión de descuentos en el xlsx
        sheet.write('B7', 'Desc.Y/o Dev', concept_body_format)
        sheet.write('C7', -sin_des, values_body_format)
        sheet.write('D7', -tij_des, values_body_format)
        sheet.write('E7', -mex_des, values_body_format)
        sheet.write('F7', -son_des, values_body_format)
        sheet.write('G7', -nor_des, values_body_format)
        sheet.write('H7', -eu_des, values_body_format)
        sheet.write('I7', -occ_des, values_body_format)
        sheet.write('J7', -bcs_des, values_body_format)
        sheet.write('K7', -chi_des, values_body_format)
        sheet.write('L7', -ind_des, values_body_format)
        sheet.write('M7', -total_discount, values_body_format)
        # Impresión de ventas en el xlsx
        sheet.write('B8', 'Ventas Netas', concept_body_format)
        sheet.write('C8', -sin_inc, values_body_format)
        sheet.write('D8', -tij_inc, values_body_format)
        sheet.write('E8', -mex_inc, values_body_format)
        sheet.write('F8', -son_inc, values_body_format)
        sheet.write('G8', -nor_inc, values_body_format)
        sheet.write('H8', -eu_inc, values_body_format)
        sheet.write('I8', -occ_inc, values_body_format)
        sheet.write('J8', -bcs_inc, values_body_format)
        sheet.write('K8', -chi_inc, values_body_format)
        sheet.write('L8', -ind_inc, values_body_format)
        sheet.write('M8', -total_income, values_body_format)
        # Impresión de costos en el xlsx
        sheet.write('B10', 'Costo de venta', concept_body_format)
        sheet.write('C10', sin_cos, values_body_format)
        sheet.write('D10', tij_cos, values_body_format)
        sheet.write('E10', mex_cos, values_body_format)
        sheet.write('F10', son_cos, values_body_format)
        sheet.write('G10', nor_cos, values_body_format)
        sheet.write('H10', eu_cos, values_body_format)
        sheet.write('I10', occ_cos, values_body_format)
        sheet.write('J10', bcs_cos, values_body_format)
        sheet.write('K10', chi_cos, values_body_format)
        sheet.write('L10', ind_cos, values_body_format)
        sheet.write('M10', total_cos, values_body_format)
        # Impresión de otros ingresos en el xlsx
        sheet.write('B12', 'Otros ingresos', concept_body_format)
        sheet.write('C12', -sin_oth, values_body_format)
        sheet.write('D12', -tij_oth, values_body_format)
        sheet.write('E12', -mex_oth, values_body_format)
        sheet.write('F12', -son_oth, values_body_format)
        sheet.write('G12', -nor_oth, values_body_format)
        sheet.write('H12', -eu_oth, values_body_format)
        sheet.write('I12', -occ_oth, values_body_format)
        sheet.write('J12', -bcs_oth, values_body_format)
        sheet.write('K12', -chi_oth, values_body_format)
        sheet.write('L12', -ind_oth, values_body_format)
        sheet.write('M12', -total_other, values_body_format)
        # Impresión de amortización en el xlsx
        sheet.write('B14', 'Depreciación', concept_body_format)
        sheet.write('C14', sin_dep, values_body_format)
        sheet.write('D14', tij_dep, values_body_format)
        sheet.write('E14', mex_dep, values_body_format)
        sheet.write('F14', son_dep, values_body_format)
        sheet.write('G14', nor_dep, values_body_format)
        sheet.write('H14', eu_dep, values_body_format)
        sheet.write('I14', occ_dep, values_body_format)
        sheet.write('J14', bcs_dep, values_body_format)
        sheet.write('K14', chi_dep, values_body_format)
        sheet.write('L14', ind_dep, values_body_format)
        sheet.write('M14', total_dep, values_body_format)

        # Calculo de gastos
        # Indicamos el renglón y la columna para los gastos
        row = 15
        col = 2
        # ordenamos la lista para acomodarla por código
        expenses.sort()
        # Variable en donde se guardara el total de gastos
        total_exp = 0
        for account in expenses:
            sin_exp, tij_exp, mex_exp, son_exp, nor_exp, eu_exp, occ_exp, bcs_exp, chi_exp, ind_exp = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            # Imprimimos el nombre de la cuenta
            sheet.write(row, 1, account, concept_body_format)
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
                        elif str(group).lower() not in territories:
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
                                    elif str(group).lower() not in territories:
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
                                    elif str(group).lower() not in territories:
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
                                elif str(group).lower() not in territories:
                                    ind_exp += rec.debit - rec.credit

            # Obtenemos el total de los gastos
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

            # Impresión de Gastos en el xlsx
            sheet.write(row, col, sin_exp, values_body_format)
            sheet.write(row, col + 1, tij_exp, values_body_format)
            sheet.write(row, col + 2, mex_exp, values_body_format)
            sheet.write(row, col + 3, son_exp, values_body_format)
            sheet.write(row, col + 4, nor_exp, values_body_format)
            sheet.write(row, col + 5, eu_exp, values_body_format)
            sheet.write(row, col + 6, occ_exp, values_body_format)
            sheet.write(row, col + 7, bcs_exp, values_body_format)
            sheet.write(row, col + 8, chi_exp, values_body_format)
            sheet.write(row, col + 9, ind_exp, values_body_format)
            sheet.write(row, col + 10, total_expense, values_body_format)
            row += 1

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

        # Impresión de beneficio por zona
        sheet.write(row + 1, col - 1, 'Beneficio', header_account_type_format)
        sheet.write(row + 1, col, sin_total, values_body_format)
        sheet.write(row + 1, col + 1, tij_total, values_body_format)
        sheet.write(row + 1, col + 2, mex_total, values_body_format)
        sheet.write(row + 1, col + 3, son_total, values_body_format)
        sheet.write(row + 1, col + 4, nor_total, values_body_format)
        sheet.write(row + 1, col + 5, eu_total, values_body_format)
        sheet.write(row + 1, col + 6, occ_total, values_body_format)
        sheet.write(row + 1, col + 7, bcs_total, values_body_format)
        sheet.write(row + 1, col + 8, chi_total, values_body_format)
        sheet.write(row + 1, col + 9, ind_total, values_body_format)
        sheet.write(row + 1, col + 10, total, values_body_format)

    # Obtener titulo principal
    def get_main_header(self, lines):
        for line in lines:
            header = 'RESULTADO '
            if line.account_period == 'current_month':
                header += 'MENSUAL '
            elif line.account_period == 'current_trimester':
                header += 'TRIMESTRAL '
            elif line.account_period == 'current_year':
                header += 'ANUAL '
            elif line.account_period == 'last_month':
                header += 'DEL ÚLTIMO MES '
            elif line.account_period == 'last_quarter':
                header += 'DEL ÚLTIMO CUARTO '
            elif line.account_period == 'last_year':
                header += 'DEL ÚLTIMO AÑO '
            if line.zone_filter == 'zone':
                header += 'DE ZONAS CONSOLIDADO '
            else:
                header += 'CONSOLIDADO '
            if line.get_account_tags():
                header += line.get_account_tags() + ' '
            header += line.get_move_state()

            return header
