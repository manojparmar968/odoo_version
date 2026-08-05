from pytz import timezone
from datetime import datetime, timedelta
from odoo import models, fields, api, _

doc=[
    ('aadhaar_front', 'Aadhaar Front'), 
    ('aadhaar_back', 'Aadhaar Back'),
    ('pan', 'Pan Card'), 
    ('dl', 'Driving Licence'), 
    ('gstin', 'GSTIN'),
    ('voter_id', 'Voter Card'), 
    ('bank_detail', 'Bank Detail'),
    ('user_agreement', 'User Agreement'),
    ('other', 'Other')
]

class UsersImagePdfUpload(models.Model):
    _name = 'res.users.doc.upload'
    _description = "User Document Upload"

    partner_doc_id = fields.Many2one('res.partner', string='Customer Name', required=True, ondelete='cascade', index=True, copy=False)
    doc_image_1920 = fields.Image(string='Document Image')
    doc_type = fields.Selection(doc, string='Document Type')
    date = fields.Datetime(string='DateTime',
        default=datetime.now(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S"))
    file_type = fields.Selection(selection=[
        ('image', 'Image'),
        ('pdf', 'PDF')], string='File Type', help='''Based on selection, the image or pdf will upload.'''
    )
    img_download = fields.Binary(string="IMG Download",related='doc_image_1920')
    file = fields.Binary('Document PDF')
    file_name = fields.Char('PDF File Name')
    pdf_download = fields.Binary(string="PDF Download",related='file')
