# -*- coding: utf-8 -*-
{
    'name': "contacts_visible_industry",

    'summary': """
        Módulo creado para contactos.""",

    'description': """
        Este módulo sirve para mostrar el sector en los usuarios de tipo de direccion de entrega.
    """,
    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'contacts',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
