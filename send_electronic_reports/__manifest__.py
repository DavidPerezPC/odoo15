# -*- coding: utf-8 -*-
{
    'name': "Send Electronic Reports",

    'summary': """
        Módulo para el envio de reportes con documentos no timbrados.
    """,

    'description': """
        Módulo para el envio de reportes con documentos no timbrados en formato pdf.
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Mail',

    'version': '14.0.1',

    'depends': ['base','mail','account_accountant'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'reports/unstamped_invoice_report.xml',
        'data/ir_cron.xml'
    ],

    'demo': [
    ],
}
