from odoo.tests.common import TransactionCase
from odoo.addons.vit_sppg.tests.common import VitSppgCommon

from odoo.exceptions import UserError
from odoo.tests import tagged

import logging
_logger = logging.getLogger(__name__)

@tagged('post_install', '-at_install')
class MasterProvinsiTestCase(VitSppgCommon):

	def test_vit_master_provinsi_count(cls):
		_logger.info(' -------------------- test record count -----------------------------------------')
		cls.assertEqual(
		    4,
		    len(cls.master_provinsis)
		)