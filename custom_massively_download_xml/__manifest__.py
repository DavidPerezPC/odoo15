# -*- coding: utf-8 -*-
{
    'name': "custom_massively_download_xml",

    'summary': """
       Módulo creado para Contabilidad.""",

    'description': """
        Desarrollo creado para generar archivo comprimdo con XML seleccionados por el usuario. 
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
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
