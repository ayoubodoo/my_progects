"""Inherited Res Partner Model."""
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
import re

class FleetVehicule(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    count_purchase_order = fields.Integer(string='Count Purchases', compute="compute_count_purchase_order")
    product_id = fields.Many2one('product.template', string='Article')
    qty = fields.Float(string='Quantité')
    price_unit = fields.Float(string='Prix unitaire')
    amount = fields.Monetary('Cost', compute='_compute_amount')
    purchaser_id = fields.Many2one('hr.employee', string="Driver", compute='_compute_purchaser_id', readonly=False,
                                   store=True)

    @api.depends('price_unit', 'qty')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.price_unit * rec.qty

    def compute_count_purchase_order(self):
        for rec in self:
            rec.count_purchase_order = len(self.env['purchase.order'].search([('service_id', '=', self.id)]))

    def create_purchase(self):
        for rec in self:
            if len(self.env['purchase.order'].search([('service_id', '=', self.id)])) > 0:
                raise UserError("Le bon de commande pour ce service est deja cree")
            if rec.product_id.id == False:
                raise UserError("Merci d'ajouter L'article dans le service avant de crée le bon de commande")
            po = self.env['purchase.order'].create({
                'partner_id': self.vendor_id.id,
                'service_id': self.id,
                'order_line': [
                    (0, 0, {
                        'product_id': rec.product_id.id,
                        'name': rec.product_id.name,
                        'date_planned': fields.Datetime.now(),
                        'product_qty': rec.qty,
                        'price_unit': rec.price_unit,
                        'product_uom': rec.product_id.uom_po_id.id,
                    })]
            })
            # for line in po.order_line:
            #     if line.price_unit != 0:
            #         line.product_qty = self.amount / line.price_unit
            # po.button_confirm()

    def action_view_commandes_achat(self):
        if len(self.env['purchase.order'].search([('service_id', '=', self.id)])) > 0:
            result = {
                'name': "Liste des commandes d'achat",
                'res_model': 'purchase.order',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', self.env['purchase.order'].search([('service_id', '=', self.id)]).ids)],
                'type': 'ir.actions.act_window',
                'target': 'current',
            }
            return result
        else:
            raise UserError(_("Aucune commande d'achat n'est encore disponible"))


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    service_id = fields.Many2one('fleet.vehicle.log.services', string='Service')
    count_req_purchase = fields.Integer(string='Count Req Purchases', compute="compute_count_req_purchase")
    remise_total = fields.Float(string='Remise Total')

    @api.depends('order_line.price_total', 'remise_total')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = tax = 0.0
            for line in order.order_line:
                line._compute_amount()
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                if amount_untaxed != 0:
                    tax = amount_tax / amount_untaxed
                else:
                    tax = 0
            amount_tax = amount_tax - order.remise_total * tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed) - order.remise_total,
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed - order.remise_total + amount_tax,
            })

    def action_view_invoice(self):
        '''
        This function returns an action that display existing vendor bills of given purchase order ids.
        When only one found, show the vendor bill immediately.
        '''
        action = self.env.ref('account.action_move_in_invoice_type')
        result = action.read()[0]
        create_bill = self.env.context.get('create_bill', False)
        # override the context to get rid of the default filtering
        result['context'] = {
            'default_type': 'in_invoice',
            'default_company_id': self.company_id.id,
            'default_purchase_id': self.id,
            'default_partner_id': self.partner_id.id,
            'default_remise_total': self.remise_total,
        }
        # Invoice_ids may be filtered depending on the user. To ensure we get all
        # invoices related to the purchase order, we read them in sudo to fill the
        # cache.
        self.sudo()._read(['invoice_ids'])
        # choose the view_mode accordingly
        if len(self.invoice_ids) > 1 and not create_bill:
            result['domain'] = "[('id', 'in', " + str(self.invoice_ids.ids) + ")]"
        else:
            res = self.env.ref('account.view_move_form', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                result['views'] = form_view
            # Do not set an invoice_id if we want to create a new bill.
            if not create_bill:
                result['res_id'] = self.invoice_ids.id or False
        result['context']['default_invoice_origin'] = self.name
        result['context']['default_ref'] = self.partner_ref
        return result

    def compute_count_req_purchase(self):
        for rec in self:
            req_purchase = []
            lignes_req_purchase = self.env['purchase.order.line'].search([('order_id', '=', rec.id)]).mapped('purchase_request_lines')
            for line in lignes_req_purchase:
                if line.request_id not in req_purchase:
                    req_purchase.append(line.request_id)
            rec.count_req_purchase = len(req_purchase)

    def action_view_demande_achat(self):
        self.compute_count_req_purchase()
        if self.count_req_purchase > 0:
            req_purchase_ids = []
            lignes_req_purchase = self.env['purchase.order.line'].search([('order_id', '=', self.id)]).mapped(
                'purchase_request_lines')
            for line in lignes_req_purchase:
                if line.request_id.id not in req_purchase_ids:
                    req_purchase_ids.append(line.request_id.id)
            result = {
                'name': "Liste des demandes d'achat",
                'res_model': 'purchase.request',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', req_purchase_ids)],
                'type': 'ir.actions.act_window',
                'target': 'current',
            }
            return result
        else:
            raise UserError(_("Aucune demande d'achat n'est encore disponible"))