# -*- coding: utf-8 -*-
{
    'name': "PDV Stock",
    'version': '1.0',
    'depends': [
        'point_of_sale',
        'account',
        'l10n_mx_edi',
    ],
    'author': "DataWorks",
    'category': 'Custom',
    'description': "Personalizacion para agregar Stock en el PDV",
    'summary': "Personalizacion para agregar Stock en el PDV",

    # Modificación ODOO V15
     "assets": {
        "point_of_sale.assets": [
            "pos_cantidad_stock/static/src/css/pos.css",
            "pos_cantidad_stock/static/src/js/Screens/ProductScreen/ProductItem.js",
            "pos_cantidad_stock/static/src/js/Screens/ProductScreen/ProductsWidgetControlPanel.js",
            "pos_cantidad_stock/static/src/js/Screens/ProductScreen/ProductsWidget.js",
            "pos_cantidad_stock/static/src/js/Chrome.js",
            "pos_cantidad_stock/static/src/js/db.js",
            "pos_cantidad_stock/static/src/js/models.js",
        ]
    },

    'data': [
        # 'views/pos_assets_common.xml',
        'views/pos_config_views.xml',
    ],

    'qweb': [
        'static/src/xml/Screens/ProductScreen/ProductItem.xml',
        'static/src/xml/Screens/ProductScreen/ProductsWidgetControlPanel.xml',
    ],
}
