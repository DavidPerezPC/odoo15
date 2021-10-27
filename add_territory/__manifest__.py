# -*- coding: utf-8 -*-
{
    'name': "add_territory",

    'summary': """
        Desarrollo creado para módulo de contabilodad.""",

    'description': """
        La fianlidad de este desarollo es agregar el territorio de dirección de entrega a apuntes contables.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",
    'category': 'Contabilidad',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'import_casaley_order', 'account_accountant'],
    'data': [
        'views/views.xml',
    ],
    'demo': [
    ],
}
