# -*- coding: utf-8 -*-
{
    'name': "action_quality_check",

    'summary': """
        Módulo creado para Control de calidad.""",

    'description': """
        Este desarrollo tiene como finalidad marcar como aprobado todos aquellos registro 
        que el tipo de prueba sea: 	Register Consumed Materials.
    """,

    'author': "Soporte Grupo Ley",
    'website': "todoo.grupoley.com.mx",
    'category': 'Calidad',
    'version': '14.0.1',
    'depends': ['base', 'quality_control'],
    'data': [
        'views/views.xml',
    ],
    'demo': [
    ],
}
