# -*- coding: utf-8 -*-
{
    'name': "add_fields_accounting",

    'summary': """
        Módulo creado para Contabilidad.""",

    'description': """
        Este desarrollo tiene como finalidad añadir dos campos nuevos territorio y sector asi como 
        tener la libertad de poner o quitar las columnas añadidas.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",
    'category': 'account_accountant',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant', 'import_casaley_order'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    'demo': [
    ],
}
