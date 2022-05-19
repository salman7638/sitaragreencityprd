# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    account_move_id = fields.Many2one('account.move', string='Journal Entry', copy=False, readonly=True)
    
    def action_create_plot_invoice(self):
        if not self.partner_id.id:
            raise UserError(_("The partner must be set"))
        res = self._create_bill()
    def _create_bill(self):
        invoice = self.env['account.move']
        lines_data = []
        
        process_fee_sum =0
        membership_fee_sum = 0
        commission_amo_sum = 0
        for adv in self.order_line:
            process_fee_sum += adv.processing_fee
            membership_fee_sum += adv.membership_fee
            commission_amo_sum += adv.co_amount
            lines_data.append([0,0,{
                'product_id':adv.product_id.id,
                'name': str(adv.name),
                'price_unit': self.amount_paid - adv.co_amount - adv.processing_fee - adv.membership_fee or 0.0,
                'quantity': 1,
                
            }])
    
        if process_fee_sum > 0: 
#             paccount = 0
#             if lines_data.name == 'Proceessing Fee':
            paccount = self.env['account.account'].sudo().search([('process', '=', True)]).id
            lines_data.append([0,0,{
            'name': 'Proceessing Fee',
            'price_unit': process_fee_sum,
            'account_id': paccount,
            'quantity': 1,
            }]) 
            
        if membership_fee_sum > 0:
            maccount = self.env['account.account'].sudo().search([('membership', '=', True)]).id
            lines_data.append([0,0,{
                'name': 'Membership Fee',
                'price_unit': membership_fee_sum,
                'account_id': maccount,
                'quantity': 1,
            }])  
            
        if commission_amo_sum > 0:   
            lines_data.append([0,0,{
                'name': 'Total Commission',
                'price_unit': commission_amo_sum,
                'quantity': 1,
            }])
            
        self.account_move_id = invoice.create({
            'move_type': 'out_invoice',
            'invoice_date': fields.Datetime.now(),
            'partner_id': self.partner_id.id,
            'currency_id': self.currency_id.id,
            'invoice_origin': self.name,
            'narration': self.name,
            'payment_reference': self.reference,
            'partner_bank_id': self.company_id.partner_id.bank_ids[:1].id,
            'invoice_user_id': self.user_id.id,
            'dealer_id':self.dealer_id.id or False,
            'invoice_line_ids':lines_data,
        })
        self.account_move_id._post()
        return invoice
    
    
class AccountAccount(models.Model):
    _inherit = "account.account"
    
    
    process =  fields.Boolean(string='Process')
    membership =  fields.Boolean(string='Membership')