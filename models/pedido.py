# -*- coding: utf-8 -*-

from odoo import models, fields, api


class pedido(models.Model):
    _name = 'odoo_basico.pedido'
    _description = 'Pedidos'

    name = fields.Char(string="Titulo", required=True, size=20)
    lineapedido_ids = fields.One2many("odoo_basico.lineapedido", 'pedido_id')

    def actualizadorSexo(self):
        informacion_ids = self.env['odoo_basico.informacion'].search([('autorizado', '=', False)])
        for rexistro in informacion_ids:
            self.env['odoo_basico.informacion']._cambia_campo_sexo(rexistro)