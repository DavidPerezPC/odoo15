# -*- coding: utf-8 -*-
{
    'name': "stock_delivery_note_acc",

    'summary': """
        Formatos de vale de entrega con contabilizacion y sin contabilizacion
    """,

    'description': """
         Formatos de vale de entrega con contabilizacion y sin contabilizacion
    """,

    'author': "",

    'website': "https://todoo.grupoley.com.mx",


    'category': 'Inventory',

    'version': '1.0.1',

    'depends': ['base','stock','stock_account','purchase_order_report'],
    'css':'static/src/css/invoice-style.css',

    # Actualización ODOO V15
     "assets": {
        "web.assets_backend": [
            "stock_delivery_note_acc/static/src/css/margin_form.css",
            "stock_delivery_note_acc/static/src/css/invoice-style.css",
        ],
        "web.report_assets_common": [
            "stock_delivery_note_acc/static/src/less/fonts.less",
        ]
    },

    'data': [
        # 'views/item_web.xml',
        'reports/delivery_note_report_acc.xml',
        'reports/delivery_note_report_view.xml',
        'views/styles_css.xml',

    ],

    'demo': [
    ],
}