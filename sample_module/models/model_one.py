from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError

class ModelOne(models.Model):
    _name = 'model.one'
    _description = 'Model One'

    seq = fields.Char(string="Sequence")
    name = fields.Char(string="Name", help='A normal name field', required=True, copy=False)
    age = fields.Integer(string="Age", default=18)
    email = fields.Char(string="Email")
    joining_date = fields.Date(string="Joining Date", required=True)
    date = fields.Date(string='Date')
    dob = fields.Date(string="Date of Birth")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], 
                            string="Gender", required=True, copy=False)
    active = fields.Boolean("Active", default=True)
    description = fields.Text("Description", default="Test Description")
    partner_ids = fields.Many2many('res.partner', string="Partner")
    sale_ids = fields.Many2many('sale.order', 'model_one_sale_rel', 'model_one_id', 'sale_id', string="Sale")
    product_ids = fields.Many2many('product.template', 'model_one_prduct_rel', 'model_one_id', 'product_id', string="Products")
    model_one_line_ids = fields.One2many('model.one.lines', 'model_one_id', string="Product")
    sale_id = fields.Many2one('sale.order', string="Sales")
    
    partner_count = fields.Integer(string="Partner Count", compute="get_partner_count")
    is_special = fields.Boolean('Is Special')
    employee_id = fields.Many2one('my.employee', string="Employee")
    sale_count = fields.Integer(string="Sale Count", compute="get_sale_count")

    def write_values(self):
        """
        Method to demonstrate various write operations on many2many and one2many fields
        """
        # Example operations for many2many fields
        products = self.env['product.template'].search([('list_price', '>', 200)], limit=1).id
        order = self.env['sale.order'].search([('id', '=', 26)], limit=1).id
        
        # self.write({'product_ids': [[6, 0, products]]})     # replace values
        # self.write({'product_ids': [[5]]})                  # unlink all records
        # self.write({'product_ids': [[4, products]]})        # link to existing record
        # self.write({'product_ids': [[3, products]]})        # unlink a record (don't delete)
        # self.write({'sale_ids': [[2, order]]})             # unlinks and deletes the record 

        # Operations for one2many fields
        # self.write({'model_one_line_ids': [[0, 0, {'name': 'Test 1', 'product_id': products, 'price': 250}]]})    
        # line = self.model_one_line_ids.filtered(lambda l: l.price == 300).id
        # existing_line = self.env['model.one.lines'].search([('price', '=', 300)], limit=1).id
        ex_line = self.env['model.one.lines'].search([('model_one_id', '=', False)], limit=1).id
        # self.write({'model_one_line_ids': [[1, line, {'price': 350}]]}) 
        # self.write({'model_one_line_ids': [[2, line]]})  
        # self.write({'model_one_line_ids': [[3, line]]})  
        # self.write({'model_one_line_ids': [[4, existing_line]]})  
        # self.write({'model_one_line_ids': [[4, ex_line]]})
        self.write({'model_one_line_ids': [[6, 0, ex_line]]})    

    def helloworld(self):
        """Simple test method"""
        print("Hello World")

    # display a wizard through button action
    def show_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'My Sample Wizard',
            'res_model': 'sample.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sample_module.view_form_sample_wizard').id,
            'target': 'new',
            'context': {
                'default_name': 'Naga',
                'default_dob': self.dob if hasattr(self, 'dob') else False
            }
        }

    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            if rec.dob:
                today = date.today()
                rec.age = today.year - rec.dob.year - ((today.month, today.day) < (rec.dob.month, rec.dob.day))
            else:
                rec.age = 0

    #@api method decorators
    #1. @api.model : model level operations, don't need recordsets
    @api.model
    def create(self, vals):
        """Override create method to set sequence"""
        vals['seq'] = self.env['ir.sequence'].next_by_code('sequence.model.one')
        res = super(ModelOne, self).create(vals)
        return res

    #2. @api.depends : define dependencies between models and fields
    @api.depends('partner_ids')
    def get_partner_count(self):
        for record in self:
            if record.partner_ids:
                record.partner_count = len(record.partner_ids)
            else:
                record.partner_count = 0

    @api.depends('sale_ids')
    def get_sale_count(self):
        for record in self:
            if record.sale_ids:
                record.sale_count = len(record.sale_ids)
            else:
                record.sale_count = 0
    
    #3. @api.onchange : execute your logic when there is a change in a field
    @api.onchange('gender')
    def onchange_gender(self):
        for record in self:
            if record.gender == 'other':
                record.is_special = True
            else:
                record.is_special = False

    def increase_age(self):
        records = self.search([]) # fetch all records
        for record in records:
            print("age before :", record.age)
            record.age += 1
            print("age after :", record.age)    
    
    @api.constrains('email')
    def check_email(self):
        for record in self:
            if record.email:  
                if not isinstance(record.email, str):
                    raise ValidationError("Email must be a text value")
                if not record.email.endswith('@gmail.com'):
                    raise ValidationError("This email doesn't end with @gmail.com. Please enter a valid email address.")
                    
    #4. _sql_constraints : to set database related constraints like unique, etc.
    _sql_constraints = [
        ('unique_email_user', 'unique(email)', 'This email already exists. Email must be unique'),
    ]

    def change_description(self):
        for record in self:
            record.description = "Description added through server action"

    def send_my_email(self):
        template = self.env.ref('sample_module.my_sample_email_template')
        for record in self:
            values = {'subject': 'My Custom Subject via Method'}
            template.send_mail(record.id, force_send=True, email_values=values)
    
    def show_sale(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('id', 'in', self.sale_ids.ids)]
        }


class ModelOneLines(models.Model):
    _name = "model.one.lines"
    _description = "Model One lines"

    name = fields.Char(string="Name", help='A normal name field')
    price = fields.Float(string="Standard Price")
    product_id = fields.Many2one('product.template', string="Product")
    model_one_id = fields.Many2one('model.one', string="Model One", 
                                 domain="['|',('gender', '=', 'female'),('age','>',18)]")