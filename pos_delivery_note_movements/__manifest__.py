# -*- coding: utf-8 -*-
{
    'name': "pos_delivery_note_movements",

    'summary': """
        Módulo creado para PoS.""",

    'description': """
        Módulo creado para Validar que no permita cerrar sesión en PoS si hay movimientos de albaran pendientes de cerrar.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'point_of_sale',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
