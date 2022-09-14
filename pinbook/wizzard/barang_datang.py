from odoo import api, fields, models


class BarangDatang(models.TransientModel):
    _name = 'pinbook.barangdatang'


    buku_id = fields.Many2one(
        comodel_name='pinbook.buku',
        string='Nama Buku',
        required=True)

    jumlah = fields.Integer(
        string='Jumlah',
        required=False)

    def button_barang_datang(self):
        for rec in self:
            self.env['pinbook.buku'].search([('id', '=', rec.buku_id.id)]).write({'stok' : rec.buku_id.stok + rec.jumlah})