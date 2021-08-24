# -*- coding: utf-8 -*-
from odoo import api, exceptions, fields, models, _


class AccountPayment(models.Model):
    _inherit = "account.payment"

    pago_origen_id = fields.Many2one('recibo.pago',string="Pago caplin")
    # empleado_id = fields.Many2one('hr.employee','Empleado')
    pago_liquidacion_ids = fields.One2many('recibo.pago','pago_id',string="Pagos")

    @api.onchange('pago_liquidacion_ids')
    def onchange_caplin_pagos(self):
        total = 0
        if self.pago_liquidacion_ids:
            for caplin_pago in self.pago_liquidacion_ids:
                if caplin_pago.linea_pago_ids:
                    for linea in caplin_pago.linea_pago_ids:
                        total += linea.pago
        self.amount = total

    # @api.multi
    def post(self):
        res = super(AccountPayment, self).post()
        for rec in self:
            if rec.pago_liquidacion_ids:
                for caplin_pago in rec.pago_liquidacion_ids:
                    caplin_pago.write({'pago_origen_id': rec.id})
        return True
