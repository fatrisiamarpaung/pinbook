from email.policy import default
from odoo.exceptions import ValidationError
from odoo import api, fields, models

class Penjualan(models.Model):
    _name = 'pinbook.penjualan'
    _description = 'Penjualan'

    name = fields.Char(string='No. Nota')
    nama_pembeli = fields.Many2one(
        comodel_name='res.partner', 
        string='Nama Pembeli')
    tgl_penjualan = fields.Datetime(
        string='Tanggal Transaksi', 
        default=fields.Datetime.now())
    total_bayar=fields.Integer(
        string='Total Pembayaran', 
        compute='_compute_totalbayar')
    detail_penjualan_ids=fields.One2many(
        comodel_name='pinbook.detailpenjualan',
        inverse_name='penjualan_id',
        string='Penjualan')
    state = fields.Selection(
        string='Status',
        selection=[('draft', 'Draft'),
                   ('confirm', 'Confirm'),
                   ('done', 'Done'),
                   ('cancelled', 'Cancelled'),
                   ],
        required=True, readonly=True, default='draft')

    def action_confirm(self):
        self.write({'state': 'confirm'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'})

    @api.depends('detail_penjualan_ids')
    def _compute_totalbayar(self):
        for rec in self:
            result= sum(self.env['pinbook.detailpenjualan'].search(
                [('penjualan_id', '=', rec.id)]).mapped('subtotal'))
            rec.total_bayar = result

    def unlink(self):
        if self.filtered(lambda line: line.state != 'draft'):
            raise ValidationError("Tidak dapat menghapus jika status bukan DRAFT")
        else:
            if self.detail_penjualan_ids:
                penjualan = []
                for rec in self:
                    penjualan = self.env['pinbook.detailpenjualan'].search(
                        [('penjualan_id', '=', rec.id)])
                    print(penjualan)

                for ob in penjualan:
                    print(ob.buku_id.name + ' ' + str(ob.qty))
                    ob.buku_id.stok += ob.qty

        rec = super(Penjualan, self).unlink()

    def write(self,vals):
        for rec in self:
            a = self.env['pinbook.detailpenjualan'].search([('penjualan_id','=',rec.id)])
            print(a)
            for data in a:
                print(str(data.buku_id.name)+' '+str(data.qty)+' '+str(data.buku_id.stok))
                data.buku_id.stok += data.qty
        record = super(Penjualan,self).write(vals)

        for rec in self:
            b = self.env['pinbook.detailpenjualan'].search([('penjualan_id','=',rec.id)])
            for new_data in b:
                if new_data in a:
                    print(str(new_data.buku_id.name)+' '+str(new_data.qty)+' '+str(new_data.buku_id.stok))
                    new_data.buku_id.stok -= new_data.qty
                else:
                    pass
        return record

    _sql_constraints = [
        ('no_nota_unik','unique (name)','Nomor Nota tidak boleh sama !!!')
    ]


class DetailPenjualan(models.Model):
    _name = 'pinbook.detailpenjualan'
    _description = 'Detail'

    name = fields.Char(string='Nama')
    penjualan_id = fields.Many2one(
        comodel_name='pinbook.penjualan',
        string='Detail Penjualan')
    buku_id = fields.Many2one(
        comodel_name='pinbook.buku',
        string='List Buku')
    harga_satuan = fields.Integer(
        string='Harga Satuan',
        onchange='_onchange_barang_id')
    qty=fields.Integer(string='Quantity')
    subtotal=fields.Integer(
        compute='_compute_subtotal', 
        string='Subtotal')

    api.depends('harga_satuan', 'qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.harga_satuan

    @api.onchange('buku_id')
    def _onchange_buku_id(self):
        if self.buku_id.harga_jual:
            self.harga_satuan = self.buku_id.harga_jual

    @api.model
    def create(self, vals):
        rec = super(DetailPenjualan, self).create(vals)
        if rec.qty:
            # Mendapatkan data berdasarkan ID pada buku_id
            self.env['pinbook.buku'].search(
                [('id', '=', rec.buku_id.id)]
            ).write({'stok': rec.buku_id.stok - rec.qty})
        
        return rec
        
    @api.constrains('qty')
    def check_quantity(self):
        for rec in self:
            if rec.qty < 1:
                raise ValidationError('Quantity error'.format(rec.buku_id.name))
            elif (rec.buku_id.stok < rec.qty):
                raise ValidationError('Stok {} tidak mencukupi, hanya tersedia {}'.format(rec.buku_id.name,rec.buku_id.stok))