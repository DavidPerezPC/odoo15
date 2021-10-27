# -*- coding: utf-8 -*-
{
    'name': "update_duplicate_sale_prices",

    'summary': """
        Módulo creado para Ventas.""",

    'description': """
        Este desarrollo tiene como finalidad que al modificar el costo del producto no  sea copiable al duplicar una venta
        y tome el precio actualizado.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",
    'category': 'sale_management',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management'],

    # always loaded
    'data': [
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
