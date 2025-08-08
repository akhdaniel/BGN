#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class mitra_sppg(models.Model):

    _name = "vit.mitra_sppg"
    _description = "vit.mitra_sppg"


    def action_reload_view(self):
        pass

    name = fields.Char( required=True, copy=False, string=_("Name"))
    id_mitra = fields.Char( string=_("Id Mitra"))
    code = fields.Char( string=_("Code"))
    jenis = fields.Char( string=_("Jenis"))
    alamat = fields.Text( string=_("Alamat"))
    status = fields.Char( string=_("Status"))
    mulai_opsnal = fields.Char( string=_("Mulai Opsnal"))
    ka_sppg = fields.Char( string=_("Ka Sppg"))
    hp_sppg = fields.Char( string=_("Hp Sppg"))
    mail_sppg = fields.Char( string=_("Mail Sppg"))
    yayasan = fields.Char( string=_("Yayasan"))


    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'name': self.name + ' (Copy)'
        })
        return super(mitra_sppg, self).copy(default)

    provinsi_id = fields.Many2one(comodel_name="vit.master_provinsi",  string=_("Provinsi"))
    kab_kota_id = fields.Many2one(comodel_name="vit.master_kab_kota",  string=_("Kab Kota"))
