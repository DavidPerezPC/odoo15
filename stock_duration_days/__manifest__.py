# -*- coding: utf-8 -*-
{
    'name': "Inventario en dias",

    'summary': """
        Módulo que nos permite obtener el nivel de inventario.
    """,

    'description': """
        Módulo que nos permite obtener el nivel de inventario en días.
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Inventory',

    'version': '14.0.1',

    'depends': ['base', 'stock', 'mrp', 'report_xlsx'],

    'data': [
        'security/ir.model.access.csv',
        'wizards/stock_generate_report.xml',
        'report/report_stock_duration_days.xml',
        'views/stock_duration_days_view.xml',
    ],

    'demo': [

    ],
}
