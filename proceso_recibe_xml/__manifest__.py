# -*- coding: utf-8 -*-
{
    'name': "proceso_recibe_xml",

    'summary': """
        Módulo que permite encontrar los XML relacionados a un proveedor y su folio de factura
    """,

    'description': """
        Módulo que permite encontrar los XML relacionados a un proveedor y su folio de factura
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Expenses',
    'version': '14.0.1',

    'depends': ['base','hr_expense','account_accountant'],

    'data': [
        'views/hr_expense.xml',
        'views/res_company.xml',
        'views/account_move.xml'
    ],

    'demo': [
    ],
}
