from odoo import api, fields, models

class Buku(models.Model):
    _name = 'pinbook.buku'
    _description = 'New Description'

    name = fields.Char(string='Judul')
    harga_beli = fields.Integer(string='Harga Modal', required=True)
    harga_jual = fields.Integer(string='Harga Jual', required=True)
    kategoribuku_id = fields.Many2one(comodel_name='pinbook.kategoribuku',
                                        string='Kategori Buku',
                                        ondelete ='cascade')

    supplier_id = fields.Many2many(comodel_name='pinbook.supplier', string='Supplier')
    stok = fields.Integer(string='Stok')


