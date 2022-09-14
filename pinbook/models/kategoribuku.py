from odoo import api, fields, models


class KategoriBuku(models.Model):
    _name = 'pinbook.kategoribuku'
    _description = 'New Description'

    name = fields.Selection([
        ('self improvement', 'Self Improvement'),
        ('romance', 'Romance'),
        ('psychology', 'Psychology'),
        ('history', 'History'),
        ('children', 'Children'),
        ('technology', 'Technology')
    ], string='Nama Kategori')
  
    kode_kategori = fields.Char(string='Kode Kategori')

    kode_rak = fields.Selection([
      ('kiri01', 'Kiri01'),
      ('kiri02', 'Kiri02'),
      ('kiri03', 'Kiri03'),
      ('kanan01', 'Kanan01'),
      ('kanan02', 'Kanan02'),
      ('kanan03', 'Kanan03')
    ], string='Kode Rak')    

    @api.onchange('name')
    def _onchange_kode_kategori(self):
      if self.name == 'self improvement':
        self.kode_kategori = 'SIB'
      elif self.name == 'romance':
        self.kode_kategori = 'RB' 
      elif self.name == 'psychology':
        self.kode_kategori = 'PSYB'
      elif self.name == 'history':
        self.kode_kategori = 'HB'
      elif self.name == 'children':
        self.kode_kategori = 'CDB'
      elif self.name == 'technology':
        self.kode_kategori = 'TECHB'
    
  
    buku_ids = fields.One2many(comodel_name='pinbook.buku',
                                inverse_name='kategoribuku_id',
                                string='Daftar Buku')

    jml_item = fields.Char(compute='_compute_jml_item', string='Jml Item')

    def _compute_jml_item(self):
      for record in self:
        a = self.env['pinbook.buku'].search([('kategoribuku_id', '=', record.id)]).mapped('name')
        b = len(a)
        record.jml_item = b
        record.daftar = a

    daftar = fields.Char(string='Daftar isi')