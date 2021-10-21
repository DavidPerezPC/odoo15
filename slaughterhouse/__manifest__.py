# -*- coding: utf-8 -*-
{
    'name': "Sacrificio",

    'summary': """
        Módulo de sacrificio
    """,

    'description': """
        Modulo de sacrificio
    """,

    'author': "Sistemas Grupo ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Sacrificio',

    'version': '14.0.1',

    'depends': ['base', 'contacts','stock'],

    'data': [
        'security/ir.model.access.csv',
        'views/slaughterhouse_view.xml',
        'views/slaughter_cattle_type_view.xml',
        'views/res_partner_view.xml',
        'views/stock_location_view.xml',
        'views/species_catalog_view.xml',
        'views/channels_classification.xml',
        'views/types_forfeiture_view.xml',
        'views/slaughter_line_view.xml',
        "views/slaughter_sub_product_type_view.xml",
        'views/slaughter_sub_product_identification_view.xml',
        'views/relationship_view.xml',
        'views/sacrifice_quotas_view.xml',
        'views/slaughter_ticket_scheduling_view.xml',
        'views/slaughter_source_sites.xml',
        'views/slaughter_passage_concepts_view.xml',
        'views/slaghter_source_sites_introducer.xml',
        'views/relationship_introducer_type_cattle_view.xml',
    ],

    'demo': [
    ],
    'installable': True,
    'application': True,
}
