# -*- coding: utf-8 -*-
{
    'name': "print_scrap_orders",

    'summary': """
        Creación de informe de operaciones de desecho en el modulo de inventario.
    """,

    'description': """
        Creación de informe de operaciones de desecho en el modulo de inventario.
    """,

    'author': "Sistemas Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Inventario',

    'version': '14.0.1',

    'depends': ['base','stock'],

    'data': [
        'reports/scrap_order_report.xml',
        'reports/scrap_orders.xml',
    ],

    'demo': [
    ],
}
