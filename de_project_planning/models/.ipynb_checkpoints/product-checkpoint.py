# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date



class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    boq_type = fields.Selection([
        ('machinary', 'Machinery / Equipment'),
        ('worker', 'Worker / Resource'),
        ('cost', 'Work Cost Package'),
        ('subcontract', 'Subcontract'),
    ], string='BOQ Type', copy=False, )
    
    job_type_id = fields.Many2one('project.job.type', string='Job Type', change_default=True, ondelete='restrict') 