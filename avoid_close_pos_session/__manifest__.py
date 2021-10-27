# -*- coding: utf-8 -*-
{
    'name': "Avoid close POS session",

    'summary': """
        Este módulo evita el cierre de la caja en el punto de venta
    """,

    'description': """
        Este módulo evita el cierre de la caja en el punto de venta dependiendo si un pedido no está facturado y está
        configurado como restringido.
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'POS',

    'version': '14.0.1',

    'depends': ['base','point_of_sale'],

    'data': [
        'views/pos_config.xml',
    ],
    'demo': [
    ],
}
