from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    invoice_count = fields.Integer(string="Invoice Count", compute='_get_invoiced')
    invoice_ids = fields.Many2many(
        comodel_name='account.move',
        string="Invoices",
        # compute='_get_invoiced',
        # search='_search_invoice_ids',
        copy=False)
    
    def _get_invoiced(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    @api.readonly
    def action_view_invoice(self, invoices=False):
        if not invoices:
            invoices = self.mapped('invoice_ids')
        action = self.env['ir.actions.actions']._for_xml_id('account.action_move_out_invoice_type')
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        
        context = {
            'default_move_type': 'out_invoice',
        }
        action['context'] = context
        return action

    def action_property_sold(self):
        res = super(EstateProperty, self).action_property_sold()
        Move = self.env['account.move']
        for property in self:
            commission_amount = property.selling_price * 0.06
            move_vals = {
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',  # Customer Invoice
                'line_ids': [],
                'invoice_line_ids': [(0,0, {
                    'name': property.name,
                    'quantity': 1,
                    'price_unit': commission_amount,
                }),
                (0,0, {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00,
                })
                ]
            }
            move = Move.create(move_vals)
            property.invoice_ids = [(4, move.id)]
        return res