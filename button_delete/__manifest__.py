# -*- coding: utf-8 -*-
{
    'name': "button_delete",

     'summary': """
        Módulo creado para contabilidad y ventas.""",

    'description': """
        La finalidad de este desarrollo es: Agregar un botón que permita borrar todas las partidas si asi lo decide el usuario.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",
    'category': 'account_accountant',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'account', 'stock', 'account_accountant'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
