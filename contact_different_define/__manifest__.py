# -*- coding: utf-8 -*-
{
    'name': "contact_different_define",

    'summary': """
        Módulo creado para módulo de usuarios.""",

    'description': """
        Módulo creado para validar que un cliente de 'Contado' no puede tener forma de pago 'Por definir'.
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
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
