# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import os
import pandas as pd
import io
import csv
import base64
import tempfile
from datetime import *

class CustomAccountBankStatement(models.TransientModel):
    _name = 'custom.account.bank.statement.validate'
    _description = 'Importación de extractos bancarios mediante csv'

    @api.model
    def _default_journal(self):
        journal_type = self.env.context.get('journal_type', False)
        company_id = self.env.company.id
        if journal_type:
            journals = self.env['account.journal'].search(
                [('type', '=', journal_type), ('company_id', '=', company_id)])
            if journals:
                return journals[0]
        return self.env['account.journal']

    file_data = fields.Binary(string='Archivo', required=True)
    file_name = fields.Char(string='Nombre')
    date = fields.Date(string='Fecha', default=datetime.today())
    company_id = fields.Many2one('res.company', string='Compañía', default=lambda self: self.env.company.id)
    journal_id = fields.Many2one('account.journal', string='Diario', required=True, default=_default_journal, check_company=True)


    def validate_import(self):
        bank_statement_obj = self.env['account.bank.statement']
        bank_statement_line_obj = self.env['account.bank.statement.line']
        file_path_csv = tempfile.gettempdir() + '/bank_statement.csv'

        #VALIDAR FORMATO DE CSV
        if not self.txt_validator(self.file_name):
            raise UserError(_("El archivo debe ser de extension .csv"))

        #DECODIFICA EL ARCHIVO BINARIO
        data_decode = base64.b64decode(self.file_data)
        data_decode = data_decode.decode('latin-1')

        #LECTURA DE ARCHIVO Y CONVERSIÓN A DATAFRAME
        data_csv = pd.read_csv(io.StringIO(data_decode),thousands=',',sep=',')
        #RECONSTRUCCIÓN DE CSV PARA SU LECTURA
        data_csv.to_csv(file_path_csv)
        #CREACIÓN DE DICCIONARIO DESDE EL CSV
        data_dict = csv.DictReader(open(file_path_csv,encoding='utf-8'))

        data_lines = []
        for i in data_dict:
            data_lines.append(i)
        if data_lines:
            data = {
                'date': self.date,
                'journal_id': self.journal_id.id
            }
            statement = bank_statement_obj.create(data)
            statement._set_next_sequence()

            for line in data_lines:
                account = line.get('CUENTA') or line.get('Cuenta')
                if "'" in account:
                    account = account.replace("'", '')

                if account not in self.journal_id.name:
                    raise UserError(_("El extracto pertenece a otro banco"))

                if line.get('FECHA DE OPERACIÓN'):
                    date = line.get('FECHA DE OPERACIÓN')
                    date = datetime.strptime(date, '%d/%m/%Y')
                else:
                    date = str(line.get('Fecha')).replace("'",'')
                    date = datetime.strptime(date, '%d%m%Y')
                ref = line.get('REFERENCIA') or line.get('Referencia')
                payment_ref = line.get('DESCRIPCIÓN') or line.get('Descripción')

                #OBTENER EL IMPORTE
                amount = 0
                if line.get('DEPÓSITOS') or line.get('RETIROS'):

                    if line.get('DEPÓSITOS') == '-':
                        amount = str(line.get('RETIROS')).replace('$', '')
                        amount = amount.replace(',', '')
                        amount = -float(amount)
                    else:
                        amount = str(line.get('DEPÓSITOS')).replace('$', '')
                        amount = amount.replace(',', '')
                        amount = float(amount)
                else:
                    if line.get('Cargo/Abono') == '-':
                        amount = -float(line.get('Importe'))
                    else:
                        amount = float(line.get('Importe'))

                data = {
                    'statement_id': statement.id,
                    'date': date,
                    'payment_ref': payment_ref,
                    'ref': ref,
                    'amount': amount,
                    'account_number': account
                }
                bank_statement_line_obj.create(data)

    #VALIDCACIÓN DE EXTENSIÓN DEL ARCHIVO
    @api.model
    def txt_validator(self, file_name):
        name, extension = os.path.splitext(file_name)
        return True if extension == '.csv' else False