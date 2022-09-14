from odoo import api, fields, models

class Supplier(models.Model):
    _name = 'pinbook.supplier'
    _description = 'Supplier'

    name = fields.Char(string='Nama Perusahaan')
    alamat = fields.Char(string='Alamat')
    no_telp = fields.Char(string='No. Telepon')
    buku_id = fields.Many2many(comodel_name='pinbook.buku', string='Buku')