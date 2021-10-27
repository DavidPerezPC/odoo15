# -*- coding: utf-8 -*-
{
    'name': "total_percentage",

    'summary': """
        Módulo creado para totalizador de porcentajes.""",

    'description': """
        Este módulo sirve para generar un totalizador de porcentajes
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'accounting',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}