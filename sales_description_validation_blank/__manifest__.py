# -*- coding: utf-8 -*-
{
    'name': "sales_description_validation_blank",

    'summary': """
        Módulo creado para Ventas.""",

    'description': """
        Módulo creado para Validar que no permita guardar un pedido o presupuesto con descripción de 
        linea de producto en blanco.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale_management',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'pos_multi_product_uom'],

    # always loaded
    'data': [
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
