# -*- coding: utf-8 -*-
{
    'name': "Caseta",

    'summary': """
        Módulo de caseta""",

    'description': """
        Módulo de caseta""",

    'author': "Sistemas Grupo ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Caseta',

    'version': '14.0.1',

    'depends': ['base', 'contacts', 'stock', 'slaughterhouse', 'fleet', 'sale_management', 'hr'],

    'data': [
        'security/ir.model.access.csv',
        'views/stall_main_view.xml',
        'views/stall_cattle_entry_view.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
