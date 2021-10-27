# -*- coding: utf-8 -*-
{
    'name': "custom_addenda_fields",

    'summary': """
        Se hicieron obligatorios los campos de addenda en caso de que el cliente la tenga activa.
    """,

    'description': """
        Se hicieron obligatorios los campos de addenda en caso de que el cliente la tenga activa.
    """,

    'author': "Sistemas Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    'category': 'Contabilidad',

    'version': '14.0.1',

    'depends': ['base','partner_addenda'],

    'data': [
        'views/account_move.xml',
    ],
    'demo': [
    ],
}
