# -*- coding: utf-8 -*-
{
    'name': "PDV Addenda",
    'version': '1.0',
    'depends': [
        'point_of_sale',
        'account',
        'l10n_mx_edi',
        'partner_addenda',
        'res_partner_cfdi',
    ],
    'author': "DataWorks",
    'category': 'Custom',
    'description': "Personalizacion para agregar Addenda en el PDV",
    'summary': "Personalizacion para agregar Addenda en el PDV",
    
    # Actualización ODOO V15
     "assets": {
        "point_of_sale.assets": [
            "pos_addenda_custom/static/src/js/Screens/PaymentScreen.js",
            "pos_addenda_custom/static/src/js/Popups/AdendaPopup.js",
            "pos_addenda_custom/static/src/js/adenda.js",
        ]
    },

    'data': [
        # 'views/templates.xml',
    ],

    'qweb': [
        'static/src/xml/Screens/PaymentScreen/PaymentScreen.xml',
        'static/src/xml/Popups/AdendaPopup.xml'
    ],
}