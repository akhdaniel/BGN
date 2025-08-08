from odoo.tests.common import TransactionCase
from odoo.addons.vit_sppg.tests.common import VitSppgCommon

from odoo.exceptions import UserError
from odoo.tests import tagged

import logging
_logger = logging.getLogger(__name__)

@tagged('post_install', '-at_install')
class MitraSppgTestCase(VitSppgCommon):

	def test_vit_mitra_sppg_count(cls):
		_logger.info(' -------------------- test record count -----------------------------------------')
		cls.assertEqual(
		    4,
		    len(cls.mitra_sppgs)
		)