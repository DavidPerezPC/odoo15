# -*- coding: utf-8 -*-
{
    'name': "amount_to_consume_vs_consumed",

    'summary': """
        Módulo creado para vista pivot inventario(Movimientos de stock)""",

    'description': """
        Este módulo es creado para que el usuario pueda ver la cantidad a consumir vs cantidad consumida por producción
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
