# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from xml.dom import minidom
import pymssql
import base64

class ProcesoRecibeXML(models.Model):
    _inherit = 'hr.expense'

    x_partner_id = fields.Many2one('res.partner', string='Proveedor',store=True)

    def server_connection(self):
        servidor = str(self.env.company.x_server_address).strip()
        db = str(self.env.company.x_database).strip()
        user = 'sa'
        passwo = 'syssql'
        try:
            connection = pymssql.connect(server=servidor, user=user, password=passwo, database=db)
            return connection
        except Exception as e:
            raise UserError(e)

    def search_xml(self):
        try:
            supplier = str(self.x_partner_id.vat).strip()
            reference = str(self.reference).strip()
            connection = self.server_connection()
            with connection.cursor() as cursor:
                cursor.execute(str("""SELECT xml FROM Fl_ContaElec_FacturasRecibidas(NOLOCK)
                                  WHERE XML IS NOT NULL AND RFC='{}' 
                                  AND FolioFacturaProveedor='{}'""").format(supplier,reference))
                batchs = cursor.fetchall()
                if batchs:
                    for batch in batchs:
                        root = minidom.parseString(str(batch[0]))
                        xml_pretty = root.toprettyxml(indent='\t',encoding='UTF-8')
                        name = 'Comprobante factura {}'.format(self.reference)
                        return self.env['ir.attachment'].create({
                            'name': name + '.xml',
                            'type': 'binary',
                            'datas': base64.encodebytes(xml_pretty),
                            'store_fname': name,
                            'res_model': 'hr.expense',
                            'res_id':self.id,
                            'mimetype': 'application/xml'
                        })
                else:
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'type': 'warning',
                            'message': _('No se encontro un XML relacionado'),
                            'next': {'type': 'ir.actions.act_window_close'},
                        }
                    }
        except Exception as e:
            raise UserError(e)





