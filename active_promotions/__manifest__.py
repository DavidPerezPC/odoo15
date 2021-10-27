# -*- coding: utf-8 -*-
{
    'name': "active_promotions",

    'summary': """
        Módulo creado para tablero de promociones.""",

    'description': """
        Este modulo sirve para crear un tablero de promociones, por ruta/cliente/producto
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale_management',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management','custom_promotions','additional_discount_promotion'],

    # always loaded
    'data': [
        'views/views.xml',
        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
