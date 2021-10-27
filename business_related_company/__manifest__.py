# -*- coding: utf-8 -*-
{
    'name': "business_related_company",

    'summary': """
       Desarrollo creado para el módulo de ventas.""",

    'description': """
        Módulo creado para especificar un usuario comercial relacionado con la empresa 
        en la que se esta llevando a cabo la transacción.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale_management',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'contacts', 'hr'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
