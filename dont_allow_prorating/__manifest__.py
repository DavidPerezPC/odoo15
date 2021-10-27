# -*- coding: utf-8 -*-
{
    'name': "dont_allow_prorating",

    'summary': """
        Módulo creado para el módulo de contabilidad/etiquetas analíticas prorrateable.""",

    'description': """
        Módulo creado para no permitir prorratear si la suma de los porcentajes es diferente de 100.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'account_accountant',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant'],

    # always loaded
    'data': [
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
