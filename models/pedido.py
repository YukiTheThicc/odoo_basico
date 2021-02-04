# -*- coding: utf-8 -*-

from odoo import models, fields, api


class pedido(models.Model):
    _name = 'odoo_basico.pedido'
    _description = 'Pedidos'

    name = fields.Char(string="Titulo", required=True, size=20)
    lineapedido_ids = fields.One2many("odoo_basico.lineapedido", 'pedido_id')