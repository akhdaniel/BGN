from odoo.tests.common import TransactionCase
from odoo.addons.vit_sppg_summary.tests.common import VitSppgSummaryCommon

from odoo.exceptions import UserError
from odoo.tests import tagged

import logging
_logger = logging.getLogger(__name__)

@tagged('post_install', '-at_install')
class RekapPotensiMbgTestCase(VitSppgSummaryCommon):

	def test_vit_rekap_potensi_mbg_count(cls):
		_logger.info(' -------------------- test record count -----------------------------------------')
		cls.assertEqual(
		    4,
		    len(cls.rekap_potensi_mbgs)
		)