#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class master_dapodik(models.Model):
    _name = "vit.master_dapodik"
    _inherit = "vit.master_dapodik"

    lintang = fields.Float( string=_("Lintang"), digits=(16, 12))
    bujur = fields.Float( string=_("Bujur"), digits=(16, 12))
