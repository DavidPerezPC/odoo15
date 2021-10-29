# -*- coding: utf-8 -*-
{
    'name': "PDV Metodo pago por cliente",
    'version': '1.0',
    'depends': [
        'point_of_sale',
        'account',
        'res_partner_cfdi',
    ],
    'author': "DataWorks",
    'category': 'Custom',
    'description': "Personalizacion para limitar Metodo pago por cliente por cliente en el PDV",
    'summary': "Personalizacion para limitar Metodo pago por cliente por cliente en el PDV",

    # Modificación ODOO V15
     "assets": {
        "point_of_sale.assets": [
            "pos_metodo_pago_cliente/static/src/js/models.js",
            "pos_metodo_pago_cliente/static/src/js/Screens/PaymentScreen/PaymentScreen.js",
        ]
    },

    'data': [
       # 'views/templates.xml',
        'views/pos_config_check_payment_method.xml',
    ],

    'qweb': [
       'static/src/xml/Screens/PaymentScreen/PaymentScreen.xml',
    ],
}
