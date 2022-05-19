# -*- coding: utf-8 -*-
 
from odoo import models, fields, api


class RegisterPayWizard(models.TransientModel):
    _inherit = "register.pay.wizard"
    _description = 'Register Pay Wizard'
    fine_amount = fields.Float(string="Fine Amount")
    
    
