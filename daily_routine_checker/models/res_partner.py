from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_users_doc_line = fields.One2many('res.users.doc.upload', 'partner_doc_id', string='User Document')