#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class master_dapodik(models.Model):

    _name = "vit.master_dapodik"
    _description = "vit.master_dapodik"


    def action_reload_view(self):
        pass

    name = fields.Char( required=True, copy=False, string=_("Name"))
    npsn = fields.Char( string=_("Npsn"))
    status_kepemilikan = fields.Char( string=_("Status Kepemilikan"))
    bentuk_pendidikan = fields.Char( string=_("Bentuk Pendidikan"))
    status_sekolah = fields.Char( string=_("Status Sekolah"))
    alamat = fields.Text( string=_("Alamat"))
    lintang = fields.Float( string=_("Lintang"))
    bujur = fields.Float( string=_("Bujur"))
    jumlah_pd = fields.Integer( string=_("Jumlah Pd"))
    jumlah_guru = fields.Integer( string=_("Jumlah Guru"))
    jumlah_tendik = fields.Integer( string=_("Jumlah Tendik"))
    update_jumlah_pd = fields.Integer( string=_("Update Jumlah Pd"))
    update_jumlah_tendik = fields.Integer( string=_("Update Jumlah Tendik"))


    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'name': self.name + ' (Copy)'
        })
        return super(master_dapodik, self).copy(default)

    provinsi_id = fields.Many2one(comodel_name="vit.master_provinsi",  string=_("Provinsi"))
    kab_kota_id = fields.Many2one(comodel_name="vit.master_kab_kota",  string=_("Kab Kota"))
