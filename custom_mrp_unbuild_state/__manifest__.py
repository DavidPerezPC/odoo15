# -*- coding: utf-8 -*-
{
    'name': "custom_mrp_unbuild_state",

    'summary': """
        Identificar ordenes descontruidas con un nuevo estado.
    """,

    'description': """
        Módulo que agrega un nuevo estado en ordenes de fabricación con la finalidad de identificar aquellas 
        ordenes que hayan sido desconstruidas.
    """,

    'author': "Soporte Grupo Ley",

    'website': "toodo.grupoley.com.mx",

    'category': 'Fabricación',

    'version': '14.0.1',

    'depends': ['base','mrp','mrp_account_enterprise','modify_cost_analysis'],

    'data': [
        'views/mrp_production.xml'
    ],

    'demo': [
    ],
}
