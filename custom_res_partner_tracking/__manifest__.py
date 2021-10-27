# -*- coding: utf-8 -*-
{
    'name': "custom_res_partner_tracking",

    'summary': """
        Módulo para tener un rastreo del cambio en etiquetas de contactos.
    """,

    'description': """
        Módulo para tener un rastreo del cambio en las etiquetas de contactos en tipo de campo many2many.
    """,

    'author': "Sistemas Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Contactos',

    'version': '14.0.1',

    'depends': ['base','mail','contacts'],

    'data': [
        'views/res_partner.xml'
    ],

    'demo': [
    ],
}
