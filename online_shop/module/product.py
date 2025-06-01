from odoo import models, fields

class Product(models.Model):
    _name = 'online.shop.product'
    _description = 'Online Shop Product'

    name = fields.Char(string='Product Name', required=True)
    description = fields.Text(string='Description')
    price = fields.Float(string='Price', required=True)
    quantity = fields.Integer(string='Available Quantity', default=1)
    image = fields.Binary(string='Product Image')
    active = fields.Boolean(string='Active', default=True)