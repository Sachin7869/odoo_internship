from odoo import models, fields, api

class Order(models.Model):
    _name = 'online.shop.order'
    _description = 'Online Shop Order'
    _inherit = ['mail.thread']

    name = fields.Char(string='Order Reference', readonly=True)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    order_date = fields.Datetime(string='Order Date', default=fields.Datetime.now)
    order_lines = fields.One2many(
        'online.shop.order.line', 
        'order_id', 
        string='Order Lines'
    )
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')

    @api.depends('order_lines.subtotal')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(line.subtotal for line in order.order_lines)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('online.shop.order')
        return super(Order, self).create(vals)

class OrderLine(models.Model):
    _name = 'online.shop.order.line'
    _description = 'Online Shop Order Line'

    order_id = fields.Many2one('online.shop.order', string='Order')
    product_id = fields.Many2one('online.shop.product', string='Product', required=True)
    quantity = fields.Integer(string='Quantity', default=1)
    price = fields.Float(string='Unit Price', related='product_id.price')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price