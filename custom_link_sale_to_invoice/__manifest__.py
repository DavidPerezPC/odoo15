# -*- coding: utf-8 -*-
{
    'name': "custom_link_sale_to_invoice",

    'summary': """
        Módulo para enlazar facturas directas con un pedido de ventas.
    """,
    
    'description': """
        Módulo para enlazar facturas directas con un pedido de ventas.
    """,

    'author': "Sistemas Grupo Ley",

    'website': "todoo.grupoley.com",

    'category': 'Ventas',

    'version': '14.0.1',

    'depends': ['base','account_accountant','sale_management','point_of_sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/sale_order.xml',
        'views/pos_order.xml'
    ],

    'demo': [
    ],
}
