# -*- coding: utf-8 -*-
{
    'name': "custom_reconciliation_bank_view",

    'summary': """
         Módelo que permite ordenar por nombre en la conciliación bancaria.
    """,

    'description': """
        Módelo que permite ordenar por nombre en la conciliación bancaria.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",

    'category': 'Contabilidad',
    'version': '14.0.1',

    'depends': ['base','account_accountant','bank_accounts'],

     "assets": {
        "web.assets_backend": [
            "custom_reconciliation_bank_view/static/src/css/style.css",
        ]
    },

    'data': [
        # 'views/account_templates.xml',
    ],

    'qweb': [
        'static/src/xml/qweb_templates.xml',
    ],

    'demo': [
    ],
}
