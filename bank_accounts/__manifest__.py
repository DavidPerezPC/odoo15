# -*- coding: utf-8 -*-
{
    'name': "bank_accounts",

    'summary': """
        Módulo creado para agregar el campo de sucursal en cuenta bancarias""",

    'description': """
        Módulo creado para agregar el campo de sucursal en cuenta bancarias
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'account_accountant',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant', 'contacts'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
