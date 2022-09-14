from odoo import api, fields, models


class Kasir(models.Model):
    _name = 'pinbook.kasir'
    _description = 'Kasir'
    
    id_kasir = fields.Char(string='ID Kasir')
    name = fields.Char(string='Nama')
    alamat = fields.Char(string='Alamat')
    tgl_lahir = fields.Datetime(string='Tanggal Lahir')
