from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit='res.partner'
    _description='Res Partner'

    is_konsumen = fields.Boolean(string='Is Konsumen')
