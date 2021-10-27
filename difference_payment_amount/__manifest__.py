# -*- coding: utf-8 -*-
{
    'name': "Difference payment and credit note",

    'summary': """
        Módelo que agrega 2 campos para diferenciar el monto rectificado y el monto pagado en una factura.
    """,

    'description': """
        Módelo que agrega 2 campos para diferenciar el monto rectificado y el monto pagado en una factura.
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Accounting',

    'version': '14.0.1',

    'depends': ['base','sale_management','account'],

    'data': [
        'views/account_move.xml',
    ],

    'demo': [
    ],
}
