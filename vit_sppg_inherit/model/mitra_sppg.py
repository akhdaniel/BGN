#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class mitra_sppg(models.Model):
    _name = "vit.mitra_sppg"
    _inherit = "vit.mitra_sppg"
