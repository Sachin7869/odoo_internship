# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2025 ZestyBeanz Technologies(<http://www.zbeanztech.com>)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'sample_module',
    'version': '18.0.0.0',
    'summary': 'madre mia',
    'description': """ This Module  is for training purposes.
    """,
    'category':'Training',
    'author': 'Sachin T',
    'website': 'www.zbeanztech.com',
    "license": "LGPL-3",
    'depends': ['base','sale','sale_management','account','contacts','product'],
    'data': [
				'security/ir.model.access.csv',
                'security/security.xml',
                'data/sequence.xml',
                'views/car_rental_view.xml',
                'views/food_view.xml',
                'views/model_one_view.xml',
                'views/model_one_lines.xml',
                'views/menu.xml',
				
        ],
    'test': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
