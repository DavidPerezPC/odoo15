# -*- coding: utf-8 -*-
{
    'name': "custom_mrp_replenish",

    'summary': """
        Módulo que agrega funcionalidad al Programa Maestro de Producción.
    """,

    'description': """
        Módulo que agrega funcionalidad al Programa Maestro de Producción agregando un nuevo boton para
        separar las ordenes de produccción.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    'category': 'MRP',

    'version': '14.0.1',

    'depends': ['base','mrp','mrp_mps'],

    'qweb': [
        "static/src/xml/qweb_templates.xml",
    ],

    'data': [
        'views/templates.xml',
    ],

    'demo': [
    ],
}
