# -*- coding: utf-8 -*-
import pytz as pytz
import locale
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
    moeda_id = fields.Many2one('res.currency', domain="[('position','=','after')]")
    gasto = fields.Monetary("Gasto", 'moeda_id')
    moeda_en_texto = fields.Char(related="moeda_id.currency_unit_label",
                                 string="Moeda en formato texto", store=True)

    moeda_euro_id = fields.Many2one('res.currency', default=lambda self: self.env['res.currency']
                                    .search([('name', '=', "EUR")], limit=1))
    gasto_en_euros = fields.Monetary("Gasto en Euros", 'moeda_euro_id')
    creador_da_moeda = fields.Char(related="moeda_id.create_uid.login",
                                   string="Usuario creador da moeda", store=True)

    data = fields.Date(string="Data", default=lambda self: fields.Date.today())
    data_hora = fields.Datetime(string="Data e Hora", default=lambda self: fields.Datetime.now())
    mes_castelan = fields.Char(compute="_mes_castelan", size=15, string="Mes en castelán", store=True)
    mes_galego = fields.Char(compute="_mes_galego", size=15, string="Mes en galego", store=True)
    hora_utc = fields.Char(compute="_hora_utc", string="Hora UTC", size=15, store=True)
    hora_timezone_usuario = fields.Char(compute="_hora_timezone_usuario", string="Hora Timezone do Usuario", size=15,
                                        store=True)
    hora_actual = fields.Char(compute="_hora_actual", string="Hora Actual", size=15, store=True)

    @api.depends('alto_en_centimetros', 'longo_en_centimetros', 'ancho_en_centimetros')
    def _volume(self):
        for rexistro in self:
            rexistro.volume = float(rexistro.alto_en_centimetros) * float(rexistro.ancho_en_centimetros) * float(
                rexistro.longo_en_centimetros)

    @api.depends('volume', 'peso')
    def _densidade(self):
        for rexistro in self:
            if rexistro.volume != 0:
                rexistro.densidade = (float(rexistro.peso) / float(rexistro.volume)) * 100
            else:
                rexistro.densidade = 0

    def _cambia_campo_sexo(self, rexistro):
        rexistro.sexo_traducido = "Hombre"

    def ver_contexto(self):
        for rexistro in self:
            raise Warning(
                'Contexto: %s' % rexistro.env.context)
        return True

    @api.depends('data')
    def _mes_castelan(self):
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8')  # Para GNU/Linux
        # locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Para Windows
        for rexistro in self:
            rexistro.mes_castelan = rexistro.data.strftime("%B")  # strftime https://strftime.org/

    @api.depends('data')
    def _mes_galego(self):
        locale.setlocale(locale.LC_TIME, 'gl_ES.utf8')  # Para GNU/Linux
        # locale.setlocale(locale.LC_TIME, 'Galician_Spain.1252')  # Para Windows
        for rexistro in self:
            rexistro.mes_galego = rexistro.data.strftime("%B")
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8')  # Para GNU/Linux
        # locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Para Windows

    @api.depends('data_hora')
    def _hora_utc(self):
        for rexistro in self:
            rexistro.hora_utc = rexistro.data_hora.strftime("%H:%M:%S")

    def actualiza_hora_actual_UTC(
            self):
        for rexistro in self:
            rexistro.hora_actual = fields.Datetime.now().strftime("%H:%M:%S")

    @api.depends('data_hora')
    def _hora_actual(self):
        for rexistro in self:
            rexistro.actualiza_hora_actual_UTC()

    def convirte_data_hora_de_utc_a_timezone_do_usuario(self, data_hora_utc_object):
        usuario_timezone = pytz.timezone(
            self.env.user.tz or 'UTC')
        return pytz.UTC.localize(data_hora_utc_object).astimezone(usuario_timezone)

    def actualiza_hora_timezone_usuario(self, obxeto_rexistro):
        obxeto_rexistro.hora_timezone_usuario = self.convirte_data_hora_de_utc_a_timezone_do_usuario(
            obxeto_rexistro.data_hora).strftime("%H:%M:%S")

    def actualiza_hora_timezone_usuario_dende_boton_e_apidepends(self):
        self.actualiza_hora_timezone_usuario(self)

    @api.depends('data_hora')
    def _hora_timezone_usuario(self):
        for rexistro in self:
            rexistro.actualiza_hora_timezone_usuario_dende_boton_e_apidepends()

    def envio_email(self):
        meu_usuario = self.env.user
        mail_reply_to = meu_usuario.partner_id.email
        mail_para = 'santiago191098@gmail.com'
        mail_valores = {
            'subject': 'Aquí iría o asunto do email ',
            'author_id': meu_usuario.id,
            'email_from': mail_reply_to,
            'email_to': mail_para,
            'message_type': 'email',
            'body_html': 'Aquí iría o corpo do email cos datos por exemplo de "%s" ' % self.descripcion,
        }
        mail_id = self.env['mail.mail'].create(mail_valores)
        mail_id.sudo().send()
        return True
