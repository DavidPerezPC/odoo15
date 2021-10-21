from odoo import models
import pandas as pd
import datetime
import dateutil.relativedelta


class ExportXLSX(models.AbstractModel):
    _name = 'report.stock_duration_days.export_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        format1 = workbook.add_format(
            {'font_size': 12, 'bold': True, 'font_color': '#ba8328', 'border': 1, 'num_format': '#,##0.00'})
        format2 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'bold': True, 'font_color': '#ba8328', 'border': 1})
        format3 = workbook.add_format({'font_size': 14, 'align': 'center', 'bold': True, 'border': 1})
        format4 = workbook.add_format({'font_size': 10, 'bold': True})
        format5 = workbook.add_format(
            {'font_size': 12, 'bold': True, 'font_color': '#ba8328'})
        format6 = workbook.add_format({'font_size': 12, 'bold': True, 'font_color': '#ba8328', 'border': 1})

        sheet = workbook.add_worksheet('Reporte Duración días')
        sheet.set_column('A:A', 10)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 25)
        sheet.set_column('H:H', 20)
        sheet.set_column('I:I', 20)
        sheet.set_column('J:J', 20)
        # sheet.set_row(1, 40)
        sheet.write('A8', 'Referencia', format1)
        sheet.write('B8', 'Producto', format1)
        sheet.write('C8', 'Unidad de medida', format1)
        sheet.write('D8', 'Categoria', format1)
        sheet.write('E8', 'Pendiente de surtir', format1)
        sheet.write('F8', 'Inventario actual', format1)
        sheet.write('G8', 'Consumo promedio diario', format1)
        sheet.write('H8', 'Cantidad de productos', format1)
        sheet.write('I8', 'Duracion en dias', format1)
        sheet.write('J8', 'Ubicación', format1)
        row = 8
        col = 0
        list_code = list()
        list_product = list()
        list_product_uom = list()
        list_category = list()
        list_pendding = list()
        list_inventory = list()
        list_average = list()
        list_qty_product = list()
        list_days = list()
        list_location = list()
        list_filter_location = list()
        list_filter_category = list()
        list_filter_product = list()
        variable = ''
        date = ''
        mes = 0
        for rec in lines:
            for fl in lines.location_id:
                list_filter_location.append(fl.name)
            for fc in lines.category:
                list_filter_category.append(fc.name)
            for fp in lines.product_ids:
                list_filter_product.append(fp.name)
            if lines.out_of_stock:
                variable = 'Incluye artículos sin existencia en inventario'
            else:
                variable = 'Articulos con existencia en inventario'
            if lines.consumption_in_months:
                mes = lines.months
                date_ends = datetime.datetime.strptime(str(lines.end_date), '%Y-%m-%d')
                date_date = str(date_ends - dateutil.relativedelta.relativedelta(months=mes))
                date_date_2 = date_date.split(sep=' ')
                date = date_date_2[0]
            if rec.inventory_lines:
                for i in rec.inventory_lines:
                    list_code.append(str(i.default_code))
                    list_product.append(i.product_id)
                    list_product_uom.append(i.product_uom)
                    list_category.append(i.category)
                    list_pendding.append(i.qty_per_supply)
                    list_inventory.append(i.qty_on_hand)
                    list_average.append(i.daily_consumption_average)
                    list_qty_product.append(i.qty_product)
                    list_days.append(i.duration_days)
                    list_location.append(i.location_id.name)

        df = pd.DataFrame(
            list(zip(list_code, list_product, list_product_uom, list_category, list_pendding, list_inventory,
                     list_average, list_qty_product, list_days, list_location)),
            columns=['Referencia', 'Producto', 'Unidad de medida', 'Categoria', 'Pendiente de surtir',
                     'Inventario actual', 'Consumo promedio diario', 'Cantidad de productos', 'Duracion en dias',
                     'Ubicación'])
        order_df = df.sort_values('Ubicación')

        set_location_3 = ', '.join(map(str, list_filter_location))
        set_category_3 = ', '.join(map(str, list_filter_category))
        set_products_3 = ', '.join(map(str, list_filter_product))

        list_code_new = order_df['Referencia'].to_list()
        list_product_new = order_df['Producto'].to_list()
        list_product_uom_new = order_df['Unidad de medida'].to_list()
        list_category_new = order_df['Categoria'].to_list()
        list_pendding_new = order_df['Pendiente de surtir'].to_list()
        list_inventory_new = order_df['Inventario actual'].to_list()
        list_average_new = order_df['Consumo promedio diario'].to_list()
        list_qty_product_new = order_df['Cantidad de productos'].to_list()
        list_days_new = order_df['Duracion en dias'].to_list()
        list_location_new = order_df['Ubicación'].to_list()
        len_df = len(order_df)
        for h in range(len_df):
            sheet.write(row, col, list_code_new[h])
            sheet.write(row, col + 1, list_product_new[h])
            sheet.write(row, col + 2, list_product_uom_new[h])
            sheet.write(row, col + 3, list_category_new[h])
            sheet.write(row, col + 4, list_pendding_new[h])
            sheet.write(row, col + 5, list_inventory_new[h])
            sheet.write(row, col + 6, list_average_new[h])
            sheet.write(row, col + 7, list_qty_product_new[h])
            sheet.write(row, col + 8, list_days_new[h])
            sheet.write(row, col + 9, list_location_new[h])
            row += 1

        sheet.merge_range('A1:J1', 'Reporte de ordenes de clientes con nivel de inventario y duración en días', format3)
        sheet.merge_range(f'A{len_df + 9}:D{len_df + 9}', 'Totales', format2)
        sheet.merge_range('A2:B2', 'Fechas', format5)
        sheet.merge_range('A3:B3', 'A la fecha: ' + str(lines.end_date), format4)
        sheet.merge_range('A4:B4', 'Calculo de consumo', format5)
        sheet.merge_range('A5:C5', variable, format4)
        sheet.merge_range('E2:F2', 'Producto', format5)
        sheet.merge_range('A6:D6', 'El Consumo Promedio Diario se calcula de las fechas: ' + str(date) + ' al: ' + str(
            lines.end_date) + " " + f"({mes} Meses)", format4)
        
        if list_filter_location:
            sheet.merge_range('E3:J3', 'Ubicaciónes: ' + str(set_location_3), format4)
        else:
            sheet.merge_range('E3:J3', 'Ubicaciónes: ' + "TODAS", format4)
        if list_filter_category:
            sheet.merge_range('E4:J4', 'Categoria: ' + str(set_category_3), format4)
        else:
            sheet.merge_range('E4:J4', 'Categoria: ' + 'TODAS', format4)
        if list_filter_product:
            sheet.merge_range('E5:J5', 'Productos: ' + str(set_products_3), format4)
        else:
            sheet.merge_range('E5:J5', 'Productos: ' + 'TODOS', format4)

        sheet.write(len_df + 8, 4, lines.x_sum_qty_pendding_supply, format1)
        sheet.write(len_df + 8, 5, lines.x_sum_qty_on_hand, format1)
        sheet.write(len_df + 8, 6, lines.x_sum_daily_consumption_average, format1)
        sheet.write(len_df + 8, 7, lines.x_sum_qty_product, format1)

        if sum(list_average_new) == 0:
            sheet.write(len_df + 8, 8, int(0), format1)
        else:
            sheet.write(len_df + 8, 8, round(sum(list_qty_product_new) / sum(list_average_new)), format6)
