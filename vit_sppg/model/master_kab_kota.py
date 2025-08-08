#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class master_kab_kota(models.Model):

    _name = "vit.master_kab_kota"
    _description = "vit.master_kab_kota"


    def action_reload_view(self):
        pass

    name = fields.Char( required=True, copy=False, string=_("Name"))
    code = fields.Char( string=_("Code"))


    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'name': self.name + ' (Copy)'
        })
        return super(master_kab_kota, self).copy(default)

    provinsi_id = fields.Many2one(comodel_name="vit.master_provinsi",  string=_("Provinsi"))
