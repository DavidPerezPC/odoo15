# -*- coding: utf-8 -*-
{
    'name': "add_markwater_invoices_cancel",

    'summary': """
        Módulo creado para contabilidad.""",
    'description': """
        Este desarrollo tiene como finalidad agregar marca de agua en todas aquellas facturas que 
        tienen el estado de cancelado.
    """,
    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",
    'category': 'Contabilidad',
    'version': '14.0.1',
    'depends': ['base', 'account_accountant', 'l10n_mx_edi', 'invoice_pdf_customization'],
    'data': [
        'views/views.xml',
    ],
    'demo': [
    ],
}
