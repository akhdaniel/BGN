#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class rekap_potensi_mbg(models.Model):

    _name = "vit.rekap_potensi_mbg"
    _description = "vit.rekap_potensi_mbg"


    @api.depends("potensi_penerima_siswa","potensi_penerima_bumil","potensi_penerima_busui","potensi_penerima_balita")
    def _get_total(self, ):
        """
        {
        "@api.depends":["potensi_penerima_siswa","potensi_penerima_bumil","potensi_penerima_busui","potensi_penerima_balita"]
        }
        """
        pass


    @api.depends("rencana_dapur_mbg","jumlah_sppg_aktif")
    def _get_prosentase_dapur(self, ):
        """
        {
        "@api.depends":["rencana_dapur_mbg","jumlah_sppg_aktif"]
        }
        """
        pass


    def action_reload_view(self):
        pass

    potensi_penerima_siswa = fields.Integer( string=_("Potensi Penerima Siswa"))
    potensi_penerima_bumil = fields.Integer( string=_("Potensi Penerima Bumil"))
    potensi_penerima_busui = fields.Integer( string=_("Potensi Penerima Busui"))
    potensi_penerima_balita = fields.Integer( string=_("Potensi Penerima Balita"))
    potensi_penerima_total = fields.Integer(compute="_get_total", store=True,  string=_("Potensi Penerima Total"))
    total_penerima_mbg = fields.Integer( string=_("Total Penerima Mbg"))
    prosentase_penerima_mbg = fields.Float(compute="_get_total", store=True,  string=_("Prosentase Penerima Mbg"))
    rencana_dapur_mbg = fields.Integer( string=_("Rencana Dapur Mbg"))
    jumlah_sppg_aktif = fields.Integer( string=_("Jumlah Sppg Aktif"))
    prosentase_dapur_mbg = fields.Float(compute="_get_prosentase_dapur", store=True,  string=_("Prosentase Dapur Mbg"))


    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'name': self.name + ' (Copy)'
        })
        return super(rekap_potensi_mbg, self).copy(default)

    name = fields.Many2one(comodel_name="vit.master_provinsi",  required=True, copy=False, string=_("Name"))
