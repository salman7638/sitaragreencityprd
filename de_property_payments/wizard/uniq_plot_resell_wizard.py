
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class UniqPlotResellWizard(models.TransientModel):
    _name = "uniq.plot.resell.wizard"
    _description = "Uniq Plot Resell wizard"
    

    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    reseller_id = fields.Many2one('res.partner', string='Reseller')
    is_process_fee = fields.Boolean(string='Processing Fee')
    resell_date = fields.Date(string='Reselling Date',  required=True, default=fields.date.today())
    product_ids = fields.Many2many('product.product', string='Products')

    def action_confirm(self):
        payment_list=[]
        for line in self.product_ids:
            resell_vals={
                'partner_id': self.reseller_id.id,
                'customer_id': self.partner_id.id,
                'date': self.resell_date,
                'product_id': line.product_tmpl_id.id,
                'amount_paid': line.amount_paid,
                'amount_residual': line.amount_residual,
            }
            reseller = self.env['uniq.reseller.line'].create(resell_vals)
            line.update({
                'partner_id': self.partner_id.id,
            }) 
            for booking_line  in  line.booking_id.order_line:
                if booking_line.product_id.id==line.id:
                   booking_line.unlink() 
          
        for prd_line in self.product_ids:            
            if prd_line.booking_id.installment_created==True:
                percent_amt = round((prd_line.list_price/prd_line.booking_id.amount_total),2)
                for installment_line in prd_line.booking_id.installment_line_ids:
                   installment_line.update({
                       'total_amount':  installment_line.total_amount - (installment_line.total_amount/100)*percent_amt,
                       'total_actual_amount': installment_line.total_actual_amount -(installment_line.total_actual_amount/100)*percent_amt,
                       'amount_paid': installment_line.amount_paid -(installment_line.amount_paid/100)*percent_amt,
                       'amount_residual': installment_line.amount_residual-(installment_line.amount_residual/100)*percent_amt,
                   })     
            booking_vals = {
              'partner_id': self.partner_id.id,
              'date_order': self.resell_date,
            }
            booking = self.env['sale.order'].create(booking_vals)
            if self.is_process_fee==True:
                booking.update({
                      'processing_fee_submit':False,
                      'membership_fee_submit':True,    
                    })
            elif self.is_process_fee==False:
                booking.update({
                    'processing_fee_submit':True,
                    'membership_fee_submit':True,  
                })      
            line_vals = {
                'order_id': booking.id,
                'product_id': prd_line.id,
                'price_unit':  prd_line.list_price,
            }
            booking_line = self.env['sale.order.line'].create(line_vals)   
            batch_payments = self.env['account.batch.payment'].search([('order_id','=',prd_line.booking_id.id)])
            for batch in batch_payments:
                final_payment_list = []
                payments = self.env['account.payment'].search([('batch_payment_id','=',batch.id),('plot_id','=',prd_line.id),('order_id','=',prd_line.booking_id.id),('state','=','posted')])
                total_b_pay = 0
                for pay in payments:
                    final_payment_list.append(pay.id)
                    total_b_pay += pay.amount
                    pay.action_draft()
                    pay.update({
                        'partner_id': self.partner_id.id,
                        'order_id': booking.id,
                    })
                    pay.action_post()
                    
                batch_vals = {
                    'batch_type': 'inbound',
                    'journal_id': batch.journal_id.id,
                    'partner_id':  self.partner_id.id,
                    'check_number':  batch.check_number ,
                    'narration':  ' Customer Payments '+ str(total_b_pay) +' - '+ str(self.partner_id.name),  
                    'order_id': booking.id,
                    'date': fields.date.today(),
                    'state': 'reconciled',
                } 
                batch=self.env['account.batch.payment'].create(batch_vals)
                batch.update({
                    'state': 'reconciled',
                })
                batch.payment_ids=final_payment_list
                batch.update({
                   'state': 'reconciled',
                })
                
                
            prd_line.update({
                    'booking_id': booking.id,
                })

       
            