# -*- coding: utf-8 -*-
{
    'name': "send_auto_invoice_email",

    'summary': """
        Envio automático de correo electrónico al timbrar una factura.
    """,

    'description': """
        Envio automático de correo electrónico al timbrar una factura y si el cliente tiene configurado
        la opción.
    """,

    'author': "Sistemas Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Contabilidad',

    'version': '14.0.1',

    'depends': ['base','contacts','l10n_mx_edi'],

    'data': [
        'views/res_partner.xml',
    ],

    'demo': [
    ],
}
