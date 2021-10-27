# -*- coding: utf-8 -*-
{
    'name': "Pos order log",

    'summary': """
        Módulo que agrega a los pedidos del punto de venta el log.
    """,

    'description': """
        Módulo que agrega a los pedidos del punto de venta el log para agaregar docuementos y enviar correos.
    """,

    'author': "Soporte Grupo Ley",

    'website': "toodo.grupoley.com.mx",

    'category': 'POS',
    'version': '14.0.1',

    'depends': ['base', 'point_of_sale'],

    'data': [
        'views/pos_order.xml',
    ],

    'demo': [
    ],
}
