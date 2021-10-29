# © 2016 ADHOC SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Account Payment CHECK Report",
    "version": "1.0.0",
    "category": "Accounting",
    "website": "",
    "author": "",
    "license": "AGPL-3",
    "application": False,
    'installable': True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": ['base', 'account_accountant',
        "account",
    ],

    # Modificación ODOO V15
     "assets": {
        "web.report_assets_common": [
            "account_payment_check_report/static/src/less/custom_check_ms_gothic.less",
            "account_payment_check_report/static/src/less/custom_check_utilities.less",
        ]
    },

    "data": [
        'report/report_payment_check.xml',
        'report/report_payment_check_santander.xml',
        'report/report_payment_check_banorte.xml',
        'report/report_payment_check_citibanamex.xml',
        'report/report_payment_check_banamexgpi.xml',
        'views/views.xml',
        # 'report/custom_assets_report_font.xml',
    ],
}
