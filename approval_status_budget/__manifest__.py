# -*- coding: utf-8 -*-
{
    'name': "approval_status_budget",

    'summary': """
        Desarrollo creado para el módulo de compras.""",

    'description': """
        Este desarrollo tiene como finalidad mostrar al usuario cuando un presupuesto ya fue aprobado.""",

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",
    'category': 'purchase',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'purchase_order_pdf_customization'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
