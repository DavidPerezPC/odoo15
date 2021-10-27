# -*- coding: utf-8 -*-
{
    'name': "custom_print_account_move",

    'summary': """
        Imprimir Asientos contables (Poliza contable)
    """,

    'description': """
        Impresión de asientos contables creados manualmente.
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Contabilidad',

    'version': '14.0.1',

    'depends': ['base','account_accountant','stock'],

    'data': [
        'reports/account_move_report.xml'
    ],

    'demo': [
    ],
}
