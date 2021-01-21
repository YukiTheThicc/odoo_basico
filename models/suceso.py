# -*- coding: utf-8 -*-

from odoo import models, fields, api


class suceso(models.Model):
    _name = 'odoo_basico.suceso'
    _description = 'Prueba de vistatree en modo edicion'

    name = fields.Char(string="Suceso", required=True, size=20)
    description = fields.Text(string="Esta es la descripcion del suceso")
    nivel = fields.Selection([('Alto', 'Alto'), ('Medio', 'Medio'), ('Bajo', 'Bajo')], string="Nivel")
    data_hora = fields.Datetime(string="Fecha y hora")
