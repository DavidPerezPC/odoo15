# -*- coding: utf-8 -*-
{
    'name': "custom_sale_invoice_status",

    'summary': """
        Modulo que añade un nuevo estado de factura al modulod de ventas
    """,

    'description': """
        Módulo que añade un nuevo estado de factura al módulo de ventas lo cual nos permite identificar 
        aquellos pedidos que hayan tenido entregas parciales con "facturado parcialmente" y aquello que
        haya entregado con menos cantidad de la solicitada, asignarle el estado de "facturado".
    """,

    'author': "Soporte Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Ventas',

    'version': '14.0.1',

    'depends': ['base','sale_management','account_accountant'],

    'data': [
        'views/sale_order.xml',
    ],

    'demo': [
    ],
}
