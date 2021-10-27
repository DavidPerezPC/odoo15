# -*- coding: utf-8 -*-
{
    'name': "custom_profit_and_loss_report",

    'summary': """
        Estado de resultados por zonas.
    """,

    'description': """
        Reporte de estado de resultados por zonas
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Contabilidad',

    'version': '14.0.1',

    'depends': ['base','account_accountant','l10n_mx','report_xlsx'],

    'data': [
        'security/ir.model.access.csv',
        'views/custom_profit_loss.xml',
        'views/account_account.xml',
        'views/account_move_line.xml',
        'reports/profit_and_loss.xml',
    ],

    'demo': [
    ],
}
