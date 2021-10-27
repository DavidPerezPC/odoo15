# -*- coding: utf-8 -*-
{
    'name': "modify_cost_analysis",

    'summary': """
        Este módulo sirve para editar el pdf de Análisis de costos""",

    'description': """
         Este módulo sirve para editar el pdf de Análisis de costos
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'mrp',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'mrp_account_enterprise'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
