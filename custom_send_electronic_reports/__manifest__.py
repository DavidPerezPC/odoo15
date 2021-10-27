# -*- coding: utf-8 -*-
{
    'name': "custom_send_electronic_reports",

    'summary': """
        Módulo que agrega el envio de informes de ventas a facturar.
    """,

    'description': """
        Módulo que agrega en el envio de informes el reporte de ventas que esten pendientes de facturar
        y que se hayan facturado más productos de los que se entregaron, ya que en ocasiones se realizan
        devoluciones y es necesario crear una nota de crédito.
    """,

    'author': "Sistemas Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Ventas',

    'version': '14.0.1',

    'depends': ['base','send_electronic_reports','sale_management'],

    'data': [
        'reports/sale_report.xml',
    ],

    'demo': [
    ],
}
