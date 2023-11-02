# encoding: utf-8

import base64
import pandas as pd
import tempfile
from odoo import models, api, fields, _
from odoo.exceptions import UserError, ValidationError


class AccountUpdateWizard(models.TransientModel):
    _name = 'account.update.wizard'
    _description = 'account update wizard'

    file = fields.Binary('File', help="File to check and import, csv format")
    filename = fields.Char(string="Filename")

    def update_accounts(self):

        if not self.file:
            raise ValidationError(_('Please select a valid file'))
        file_path = tempfile.gettempdir() + '/file.csv'
        data = self.file
        f = open(file_path, 'wb')
        f.write(base64.decodebytes(data))
        f.close()

        d = pd.read_csv(file_path)
        liste = d.to_numpy()
        account_obj = self.env['account.account']
        record = account_obj.search([('internal_type', '!=', 'view'), ('company_id', '=', self.env.company.id)])
        # nombre_initial = len(d['code'].unique())

        nombre_initial = 0
        total = 0
        updated = 0
        created = 0
        ignored = 0
        for e in liste:
            #UPDATE , e[1] it's the name, but must a account code, so we use e[0] instead at if and write, look to the search
            # we serach accounts by their code
            if str(e[0]) != 'nan':
                total = total + 1
                n = account_obj.search([('code', '=', str(int(e[0]))),
                    ('company_id', '=', self.env.company.id)])
                if len(n) != 0:
                    if e[1] != 'nan':
                        #UPDATE , e[0] it's the code, but must the account name, so we use e[1] at if and write
                        n.write({'name': e[1]})
                        updated = updated + 1
                        print(str(total) + ' un compte modifie')
                else:
                    t = 0
                    i = len(str(int(e[0]))) - 1
                    while i > 0:
                        for c in record:
                            if len(str(c.code)) >= i:
                                if str(int(e[0]))[0:i] == str(c.code)[0:i]:
                                    t = 1
                                    reconcile = False
                                    if c.user_type_id.type in ('receivable', 'payable'):
                                        reconcile = True
                                    print(e)
                                    account_obj.create({'code': str(int(e[0])), 'name': str(e[1]),
                                                        'user_type_id': c.user_type_id.id,
                                                        'reconcile': reconcile,
                                                        'company_id': self.env.company.id})
                                    created = created + 1
                                    print(str(total) + ' un compte cree')
                                    break
                        i = i - 1
                        if t:
                            break
                    if t == 0:
                        ignored = ignored + 1
                        print(str(total) + ' un compte ignore')

        print('Nombre initial : ' + str(nombre_initial))
        print('Total : ' + str(total))
        print('Updated : ' + str(updated))
        print('Created : ' + str(created))
        print('Ignored : ' + str(ignored))
        print('Somme : ' + str(updated + created + ignored))
