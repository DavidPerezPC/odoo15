# -*- coding: utf-8 -*-
{
    'name': "NSS_and_INFONAVIT",

    'summary': """
        Módulo creado para requerir al usuario No.Seguro Social y No.INFONAVIT.""",

    'description': """
        Módulo creado para requerir al usuario No.Seguro Social y No.INFONAVIT.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'hr',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
