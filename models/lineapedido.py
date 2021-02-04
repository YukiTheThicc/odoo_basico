# -*- coding: utf-8 -*-

from odoo import models, fields, api


class lineapedido(models.Model):
    _name = 'odoo_basico.lineapedido'
    _description = 'Linespedidosasdasdadasdf,gkbgr'

    descripcion_da_lineapedido = fields.Text(string="La descripcion")
    pedido_id = fields.Many2one('odoo_basico.pedido',
                                ondelete="cascade", required=True)
