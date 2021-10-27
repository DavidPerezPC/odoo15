# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime


class total_days(models.Model):
    _inherit = 'pos.autorizacion'

    remaining_days = fields.Char(string="Tiempo autorización", compute="calculed_days", help="Formato: DD HH/MM")
    x_remaining_days = fields.Char(string="Tiempo autorización", store=True, help="Formato: DD HH/MM")
    x_commercial_user_pos = fields.Many2one('res.users',related='partner_id.user_id',string="Comercial", store=True)

    @api.depends('create_date', 'fch_autorizacion')
    def calculed_days(self):
        for rec in self:
            create_date = rec.create_date
            authorization_date = rec.fch_autorizacion

            if authorization_date:
                subtract_days = authorization_date - create_date
                # Se convierte a string para separar DD/MM
                s_subtract_days = str(subtract_days)
                s_subtract_days = s_subtract_days.replace("day", ":")
                s_subtract_days = s_subtract_days.replace(",", "")
                s_subtract_days = s_subtract_days.split(sep=":")
                if len(s_subtract_days) == 3:
                    s_subtract_days.insert(0, '0')
                    minutes = s_subtract_days[2].split(sep=".")
                    if int(s_subtract_days[0]) > 2:
                        rec.remaining_days = s_subtract_days[0] + " " + "Días" + " " + s_subtract_days[1] + ":" + \
                                             minutes[0]
                        rec.x_remaining_days = s_subtract_days[0] + " " + "Días" + " " + s_subtract_days[1] + ":" + \
                                               minutes[0]
                    elif int(s_subtract_days[0]) == 0:
                        rec.remaining_days = s_subtract_days[0] + " " + "Días" + " " + s_subtract_days[1] + ":" + \
                                             minutes[0]
                        rec.x_remaining_days = s_subtract_days[0] + " " + "Días" + " " + s_subtract_days[1] + ":" + \
                                               minutes[0]
                    else:
                        rec.remaining_days = s_subtract_days[0] + " " + "Día" + " " + s_subtract_days[1] + ":" + \
                                             minutes[0]
                        rec.x_remaining_days = s_subtract_days[0] + " " + "Día" + " " + s_subtract_days[1] + ":" + \
                                               minutes[0]
                else:
                    # Asignación de dias y minutos.
                    minutes = s_subtract_days[2].split(sep=".")
                    horas = s_subtract_days[1].replace("s", "")
                    if int(s_subtract_days[0]) > 2:
                        rec.remaining_days = s_subtract_days[0] + " " + "Días" + " " + horas + ":" + minutes[0]
                        rec.x_remaining_days = s_subtract_days[0] + " " + "Días" + " " + horas + ":" + minutes[0]
                    elif int(s_subtract_days[0]) == 0:
                        rec.remaining_days = s_subtract_days[0] + " " + "Días" + " " + s_subtract_days[1] + ":" + \
                                             minutes[0]
                        rec.x_remaining_days = s_subtract_days[0] + " " + "Días" + " " + s_subtract_days[1] + ":" + \
                                               minutes[0]
                    else:
                        rec.remaining_days = s_subtract_days[0] + " " + "Día" + " " + horas + ":" + minutes[0]
                        rec.x_remaining_days = s_subtract_days[0] + " " + "Día" + " " + horas + ":" + minutes[0]
            else:
                rec.remaining_days = "Pendiente de autorizar"
                rec.x_remaining_days = "Pendiente de autorizar"