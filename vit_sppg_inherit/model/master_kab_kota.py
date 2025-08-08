#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class master_kab_kota(models.Model):
    _name = "vit.master_kab_kota"
    _inherit = "vit.master_kab_kota"
