# -*- coding: utf-8 -*-

from odoo import models, fields, api


class informacion(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'Tipos de datos basicos'

    name = fields.Char(string="Titulo", required=True, size=20)
    description = fields.Text(string="Esta es la descripcion")
    autorizado = fields.Boolean(string="Esta autorizado", default=False)
    sexo_traducido = fields.Selection([('Hombre', 'Home'), ('Mujer', 'Muller'),
                                       ('Otros', 'Outros')], string="Sexo")
    alto_en_centimetros = fields.Integer(string="Altura(cms)")
    longo_en_centimetros = fields.Integer(string="Longo(cms)")
    ancho_en_centimetros = fields.Integer(string="Ancho(cms)")
    volume = fields.Float(compute="_volume", store=True)
    peso = fields.Float(string="Peso", default=2.7, digits=(6, 2))
    densidade = fields.Float(compute="_densidade", store=True)
    foto = fields.Binary(string='Foto')
    adxunto_nome = fields.Char(string="Nome adxunto")
    adxunto = fields.Binary(string='Arquivo adxunto')

    @api.depends('alto_en_centimetros', 'longo_en_centimetros',
                 'ancho_en_centimetros')
    def _volume (self):
        for rexistro in self:
            rexistro.volume = float(rexistro.alto_en_centimetros) * float(rexistro.ancho_en_centimetros) * float(rexistro.longo_en_centimetros)

    @api.depends('volume', 'peso')
    def _densidade(self):
        for rexistro in self:
            if rexistro.volume != 0:
                rexistro.densidade = (float(rexistro.peso) / float(rexistro.volume))*100
            else:
                rexistro.densidade = 0
#    value = fields.Integer()
#    value2 = fields.Float(compute="_value_pc", store=True)
#   description = fields.Text()

#    @api.depends('value')
#    def _value_pc(self):
#        for record in self:
#            record.value2 = float(record.value) / 100
