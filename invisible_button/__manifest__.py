# -*- coding: utf-8 -*-
{
    'name': "invisible_button",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Este moduo sirve para que el boton de promociones sea invisible cuando este en estado de 
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'sale_coupon'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views_button_invisible.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
