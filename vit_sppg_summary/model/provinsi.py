#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class provinsi(models.Model):

    _name = "vit.master_provinsi"
    _description = "vit.master_provinsi"


    def action_reload_view(self):
        pass


    _inherit = "vit.master_provinsi"


