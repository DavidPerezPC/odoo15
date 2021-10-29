# -*- coding: utf-8 -*-
{
    'name': "PDV Precio según Lista de Precios",
    'version': '1.0',
    'depends': [
        'point_of_sale',
    ],
    'author': "DataWorks",
    'category': 'Custom',
    'description': "PDV Precio según Lista de Precios",
    'summary': "PDV Precio según Lista de Precios",

    # Modificación ODOO V15
     "assets": {
        "point_of_sale.assets": [
            "pos_precio_lista_precio/static/src/js/models.js",
        ]
    },

    'data': [
        #'views/pos_assets_common.xml',
    ],

    'qweb': [

    ],
}
