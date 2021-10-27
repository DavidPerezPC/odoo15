# -*- coding: utf-8 -*-
{
    'name': "add_territory_to_accounting",

    'summary': """
        Módulo creado para contabilidad.""",

    'description': """
        Este desarrollo tiene como finalidad agregar el territorio del cliente en Contabilidad/Facturas
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",
    'category': 'account_accountant',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant', 'sale_management', 'contacts', 'import_casaley_order', 'stock', 'point_of_sale'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
