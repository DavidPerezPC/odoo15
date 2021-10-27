# -*- coding: utf-8 -*-
{
    'name': "add_territory_data",

    'summary': """
        Módulo creado para agregar territorio.""",

    'description': """
        Módulo creado para agregar territorio en el módulo de ventas en los diferentes tipos de ventas.
        Se agregó el sector y el almacén junto con el territorio.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale_management',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'contacts', 'import_casaley_order', 'stock', 'point_of_sale'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
