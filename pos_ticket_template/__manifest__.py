# -*- coding: utf-8 -*-

{
    'name': 'Point of Sale Ticket Template ',
    'version': '1.0.1',
    'category': 'Sales/Point of Sale',
    'sequence': 10,
    'summary': 'Inherit ticket POS ',
     'author': "DataWorks",
    'description': "",
    'depends': ['base','point_of_sale', 'pos_autorizacion','pos_precio_lista_precio','pos_impresion_ticket'],
    
    # Modificación ODOO V15
     "assets": {
        "point_of_sale.assets": [
            "pos_ticket_template/static/src/js/models.js",
        ]
    },

    'data': [
        # 'views/templates.xml',

    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'qweb': [
        #'static/src/xml/Screens/ReceiptScreen/WrappedProductNameLines.xml',
        'static/src/xml/OrderReceipt.xml',
        #'static/src/xml/Screens/ReceiptScreen/ReceiptScreen.xml',

    ],
    'website': '',
}
