# -*- coding: utf-8 -*-
{
    'name': "promotions_board",

    'summary': """
        Módulo creado para tablero de promociones activas""",

    'description': """
        Módulo creado para tablero de promociones activas, dicho módulo le permitira al usuario,
        ver de manera más concreta lo campos.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale_management',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management','additional_discount_promotion','custom_promotions'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
