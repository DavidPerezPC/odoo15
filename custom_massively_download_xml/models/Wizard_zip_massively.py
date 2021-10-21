# -*- coding: utf-8 -*-

from odoo import api, fields, models


class download_ZIP(models.TransientModel):
    _name = 'download.zip'
    _description = 'Módulo creado para el Wizard de descarga masiva XML'

    binary_zip = fields.Binary(string="Archivo ZIP", store=True)
    field_name_binary = fields.Char(string="Nombre", default="Archivo ZIP", readonly=True)



