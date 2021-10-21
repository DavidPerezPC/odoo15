# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import base64
import os
from os.path import basename
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from datetime import date


class download_xml_massive(models.Model):
    _inherit = 'account.move'

    def comprido_massive(self, list_xml):
        zip_file = self.env['ir.attachment'].search([('name', '=', 'XML Masivos.zip')], limit=1)
        if zip_file:
            zip_file.sudo().unlink()
        # function to convert binary data
        def isBase64_decodestring(s):
            try:
                decode_archive = base64.decodebytes(s)
                return decode_archive
            except Exception as e:
                raise ValidationError('Error:', + str(e))

        tempdirXML = TemporaryDirectory()
        location_tempdir = tempdirXML.name
        # creating dynamic path to create zip file
        date_act = date.today()
        file_name = 'DescargaMasiva(Fecha de descarga' + " - " + str(date_act) + ")"
        file_name_zip = file_name + ".zip"
        zipfilepath = os.path.join(location_tempdir, file_name_zip)
        path_files = os.path.join(location_tempdir)

        # creating zip file in above mentioned path
        for xml_file in list_xml:
            object_name = xml_file.name
            ruta_ob = object_name
            ru = os.path.join(location_tempdir, ruta_ob)
            object_handle = open(os.path.join(location_tempdir, ruta_ob), "wb")
            object_handle.write(isBase64_decodestring(xml_file.datas))
            object_handle.close()

        with ZipFile(zipfilepath, 'w') as zip_obj:
            for file in os.listdir(path_files):
                file_path = os.path.join(path_files, file)
                if file_path != zipfilepath:
                    zip_obj.write(file_path, basename(file_path))

        bytes_content = None
        with open(zipfilepath, 'rb') as file_data:
            bytes_content = file_data.read()
            encoded = base64.b64encode(bytes_content)

        data = {
            'name': 'XML Masivos.zip',
            'type': 'binary',
            'datas': encoded,
            'company_id': self.env.company.id
        }
        attachment = self.env['ir.attachment'].create(data)
        return self.download(file_name_zip, attachment.id)

        # code snipet for downloading zip file

    def download(self, filename, id_file):
        path = "/web/binary/download_document?"
        model = "ir.attachment"

        url = path + "model={}&id={}&filename={}".format(
            model, id_file, filename)

        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }

    def dowlowad_massive_xml(self):
        for i in self.attachment_ids:
            name = i.name
            if name:
                lista = name.split('.')
                if lista[-1] == "xml":
                    return i
