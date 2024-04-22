# -*- coding: utf-8 -*-
{
    'name': "Sale_order_report",

    'summary': """
        This module used to print sale order report based on project item wise""",

    'description': """
        
    """,

    'author': "Odoofusion",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizard/project_item_wizard.xml',
        'wizard/porject_items_sale.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
