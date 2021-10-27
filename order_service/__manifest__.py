# -*- coding: utf-8 -*-
{
    'name': "order_service",

    'summary': """
        Módulo creado para sacar la cantidad de dias de fecha autorización.""",

    'description': """
         Módulo creado para sacar la cantidad de dias de fecha autorización,
         módulo punto de venta.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'point_of_sale',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale', 'pos_autorizacion'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/report_time_autorized.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
