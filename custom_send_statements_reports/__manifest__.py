# -*- coding: utf-8 -*-
{
    'name': "custom_send_statements_reports",

    'summary': """
        Agregar reporte de extractos bancarios no timbrados.
    """,

    'description': """
        Agregar reporte de extractos bancarios no timbrados.
    """,

    'author': "Sistemas Grupo Ley",

    'website': "todoo.grupoley.com.mx",

    'category': 'Contabilidad',
    'version': '14.0.1',

    'depends': ['base','send_electronic_reports'],

    'data': [
        'reports/statements_report.xml'
    ],

    'demo': [
    ],
}
