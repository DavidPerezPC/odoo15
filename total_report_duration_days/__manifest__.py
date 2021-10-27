# -*- coding: utf-8 -*-
{
    'name': "total_report_duration_days",

    'summary': """
        Desarrollo creado para informe nivel de inventario en días.""",

    'description': """
        Este desarrollo tiene como finalidad agregar totaliadores de columnas en 
        informe nivel de inventario en días.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",
    'category': 'stock_duration_days',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock_duration_days', 'stock', 'mrp'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    'demo': [
    ],
}
