#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class rekap_potensi_mbg(models.Model):
    _name = "vit.rekap_potensi_mbg"
    _inherit = "vit.rekap_potensi_mbg"

    @api.depends("potensi_penerima_siswa","potensi_penerima_bumil","potensi_penerima_busui","potensi_penerima_balita")
    def _get_total(self, ):
        """
        {
        "@api.depends":["potensi_penerima_siswa","potensi_penerima_bumil","potensi_penerima_busui","potensi_penerima_balita"]
        }
        """
        for rec in self:
            rec.potensi_penerima_total = (rec.potensi_penerima_siswa +
                rec.potensi_penerima_bumil + rec.potensi_penerima_busui + 
                rec.potensi_penerima_balita)
            if rec.total_penerima_mbg >0:
                rec.prosentase_penerima_mbg = 100.0*(rec.potensi_penerima_total / rec.total_penerima_mbg)
            else:
                rec.prosentase_penerima_mbg = 0


    @api.depends("rencana_dapur_mbg","jumlah_sppg_aktif")
    def _get_prosentase_dapur(self, ):
        """
        {
        "@api.depends":["rencana_dapur_mbg","jumlah_sppg_aktif"]
        }
        """
        for rec in self:
            if rec.rencana_dapur_mbg > 0:
                rec.prosentase_dapur_mbg = 100.0 * (rec.jumlah_sppg_aktif / rec.rencana_dapur_mbg)
            else:
                rec.prosentase_dapur_mbg = 0

