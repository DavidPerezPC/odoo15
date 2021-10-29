# -*- coding: utf-8 -*-
{
    'name': "PDV Restriccion de clientes por almacen",
    'version': '1.0',
    'depends': [
        'point_of_sale',
        'sale_stock',
    ],
    'author': "DataWorks",
    'category': 'Custom',
    'description': "Personalizacion para Restriccion de clientes por almacen en el PDV",
    'summary': "Personalizacion para Restriccion de clientes por almacen en el PDV",

    # Modificación ODOO V15
     "assets": {
        "point_of_sale.assets": [
            "pos_cliente_almacen/static/src/js/Screens/ClientListScreen/ClientListScreen.js",
        ]
    },

    'data': [
        # 'views/template.xml',
        'views/pos_config_check_all_picking_type_view_form.xml',
    ],

    'qweb': [

    ],
}
