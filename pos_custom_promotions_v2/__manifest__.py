# -*- coding: utf-8 -*-
{
    'name': "POS Promotions v2",
    'version': '1.0',
    'depends': [
        'point_of_sale',
        'custom_promotions',
        'pos_multi_product_uom',
    ],
    'author': "DataWorks",
    'category': 'Point of Sale',
    'description': "Personalizacion para manejo de promociones y descuentos POS V.2",
    'summary': "Personalizacion para manejo de promociones y descuentos POS V.2",

    # Modificación ODOO V15
     "assets": {
        "point_of_sale.assets": [
            "pos_custom_promotions_v2/static/src/js/models.js",
            "pos_custom_promotions_v2/static/src/js/Screens/ProductScreen/ControlButtons/PromocionesButtonLey.js",
        ]
    },

    'data': [
        # 'views/templates.xml',
        'views/pos_order_views.xml',
    ],

    'qweb': [
        'static/src/xml/Screens/ProductScreen/ControlButtons/PromocionesButton.xml',
    ],
}
