# -*- coding: utf-8 -*-
{
    'name': "Plot Fine",

    'summary': """
        Plot Fine Details
        """,

    'description': """
        Plot Fine Details
    """,

    'author': "dynexel",
    'website': "http://www.dynexel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','de_property','product','sale','de_property_payments'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/cron.xml',
        'wizard/fine_wizard.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
