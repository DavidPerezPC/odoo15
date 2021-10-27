# -*- coding: utf-8 -*-
{
    'name': "custom_account_change_date",

    'summary': """
        Cambio de fecha contable para evitar errores de timbrado.
    """,

    'description': """
        Cambiar la fecha contable para evitar errores en los timbrados.
    """,

    'author': "Sistemas Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Contabilidad',

    'version': '14.0.1',

    'depends': ['base','account_accountant','l10n_mx_edi'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/account_date.xml',
        'views/account_move.xml'
    ],

    'demo': [
    ],
}
