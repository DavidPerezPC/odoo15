# -*- coding: utf-8 -*-
{
    'name': "modify_workorder",

    'summary': """
        Módulo creado para añadir columnas a vista tree de ordenes de trabajo.""",

    'description': """
        Módulo creado para añadir columnas (Producto,Orden de fabricación) a vista tree de ordenes de trabajo.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'mrp',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
