# -*- coding: utf-8 -*-
{
    'name': "invoice_pdf_customization",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly ,'l10n_mx_edi'
    'depends': ['base','account','l10n_mx_edi','l10n_mx_edi_extended','custom_promotions','bank_accounts'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/account_move_views.xml',
    ],
}
