# -*- coding: utf-8 -*-
{
    'name': "custom_account_bank_statement_validation",

    'summary': """
        Validación e importe de extractos bancarios con formato csv. 
    """,

    'description': """
        Validación e importe de extractos bancarios con formato csv. 
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Contabilidad',
    'version': '14.0.1',

    'depends': ['base','account_accountant','bank_accounts'],

    'data': [
        'security/ir.model.access.csv',
        'views/validate_csv_view.xml',
        'views/account_journal_dashboard_view.xml'
    ],

    'demo': [
    ],
}
