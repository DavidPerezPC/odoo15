# -*- coding: utf-8 -*-
{
    'name': "invoice_entry_validation",

    'summary': """
        Módulo creado para contabilidad.""",

    'description': """
        Este desarrollo tiene como finalidad, restringir al usuario para que no cree dos facturas con el mismo 
        folio y para la misma cadena.
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'account_accountant',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant'],

    # always loaded
    'data': [
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
