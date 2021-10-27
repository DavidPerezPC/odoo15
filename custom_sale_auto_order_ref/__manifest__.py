# -*- coding: utf-8 -*-
{
    'name': "custom_sale_auto_order_ref",

    'summary': """
        Agrega a la vista de pedidos de venta el folio y la fecha de orden de compra.
    """,

    'description': """
        Agrega a la vista de pedidos de venta el folio y la fecha de orden de compra.
    """,

    'author': "Sistemas Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Ventas',

    'version': '14.0.1',

    'depends': ['base','sale_management','import_casaley_order'],

    'data': [
        'views/sale_order.xml',
    ],

    'demo': [
    ],
}
