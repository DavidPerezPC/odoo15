# -*- coding: utf-8 -*-
{
    'name': "add_source_document",

    'summary': """
       Desarrollo creado para módulo de inventarios.""",

    'description': """
        La finalidad de este desarrollo es añadir la columna de documento origen en módulo de
        inventarios - movimientos de stock.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",
    'category': 'Inventarios',
    'version': '14.0.1',
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
