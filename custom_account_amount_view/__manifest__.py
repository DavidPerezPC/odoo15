# -*- coding: utf-8 -*-
{
    'name': "custom_account_amount_view",

    'summary': """
        Cambio de ubicación en los campos de importe y fecha de pago
    """,

    'description': """
        Cambio de ubicación en los campos de importe y fecha de pago
    """,

    'author': "Sistemas Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Contabilidad',

    'version': '14.0.1',

    'depends': ['base','account','l10n_mx_edi'],

    'data': [
        'views/account_payment_register.xml',
    ],
    'demo': [
    ],
}
