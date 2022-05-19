# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from json import dumps

import ast
import json
import re
import warnings


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    account_move_id = fields.Many2one('account.move', string='Journal Entry', copy=False, readonly=True)
    invoiced_flag = fields.Boolean(string="Invoiced")
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
                'price_unit': ((adv.price_subtotal-((adv.price_subtotal/100)*self.disc))-adv.co_amount) if adv.discount==0 and self.disc > 0  else adv.price_subtotal - adv.co_amount,
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
            'invoice_payment_term_id': self.payment_term_id.id,
            'partner_bank_id': self.company_id.partner_id.bank_ids[:1].id,
            'invoice_user_id': self.user_id.id,
            'dealer_id':self.dealer_id.id or False,
            'invoice_line_ids':lines_data,
        })
        self.account_move_id._post()
        self.invoiced_flag = True
        return invoice
    
    
class AccountAccount(models.Model):
    _inherit = "account.account"
    
    
    process =  fields.Boolean(string='Process')
    membership =  fields.Boolean(string='Membership')
    
    
    
# class AcountMove(models.Model):
#     _inherit = "account.move"
    
    
    
#     def _compute_payments_widget_to_reconcile_info(self):
#         for move in self:
#             move.invoice_outstanding_credits_debits_widget = json.dumps(False)
#             move.invoice_has_outstanding = False

#             if move.state != 'posted' \
#                     or move.payment_state not in ('not_paid', 'partial') \
#                     or not move.is_invoice(include_receipts=True):
#                 continue

#             pay_term_lines = move.line_ids\
#                 .filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))

#             domain = [
#                 ('account_id', 'in', pay_term_lines.account_id.ids),
#                 ('parent_state', '=', 'posted'),
#                 ('partner_id', '=', move.commercial_partner_id.id),
#                 ('reconciled', '=', False),
#                 ('invoice_origin','=', self.env['account.payment'].search([('order_id', '=', 'move.invoice_origin')])),
#                 '|', ('amount_residual', '!=', 0.0), ('amount_residual_currency', '!=', 0.0),
#             ]

#             payments_widget_vals = {'outstanding': True, 'content': [], 'move_id': move.id}

#             if move.is_inbound():
#                 domain.append(('balance', '<', 0.0))
#                 payments_widget_vals['title'] = _('Outstanding credits')
#             else:
#                 domain.append(('balance', '>', 0.0))
#                 payments_widget_vals['title'] = _('Outstanding debits')

#             for line in self.env['account.move.line'].search(domain):

#                 if line.currency_id == move.currency_id:
#                     # Same foreign currency.
#                     amount = abs(line.amount_residual_currency)
#                 else:
#                     # Different foreign currencies.
#                     amount = move.company_currency_id._convert(
#                         abs(line.amount_residual),
#                         move.currency_id,
#                         move.company_id,
#                         line.date,
#                     )

#                 if move.currency_id.is_zero(amount):
#                     continue

#                 payments_widget_vals['content'].append({
#                     'journal_name': line.ref or line.move_id.name,
#                     'amount': amount,
#                     'currency': move.currency_id.symbol,
#                     'id': line.id,
#                     'move_id': line.move_id.id,
#                     'position': move.currency_id.position,
#                     'digits': [69, move.currency_id.decimal_places],
#                     'date': fields.Date.to_string(line.date),
#                     'account_payment_id': line.payment_id.id,
#                 })

#             if not payments_widget_vals['content']:
#                 continue

#             move.invoice_outstanding_credits_debits_widget = json.dumps(payments_widget_vals)
#             move.invoice_has_outstanding = True