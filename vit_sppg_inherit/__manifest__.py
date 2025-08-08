#-*- coding: utf-8 -*-

{
	"name": "Data SPPG dan Dapodik Inherited",
	"version": "1.0",
	"depends": [
		"base",
		"vit_sppg"
	],
	"author": "Akhmad Daniel Sembiring",
	"category": "Utility",
	"website": "http://vitraining.com",
	"images": [
		"static/description/images/main_screenshot.jpg"
	],
	"price": "100",
	"license": "OPL-1",
	"currency": "USD",
	"summary": "",
	"description": "",
	"data": [
		"wizard/import_sppg_wizard.xml",
		"wizard/import_dapodik_wizard.xml",
		"security/ir.model.access.csv",
		"view/import_menu.xml",
		#"view/mitra_sppg.xml",
		#"view/master_dapodik.xml"
	],
	"installable": True,
	"auto_install": False,
	"application": True,
	"odooVersion": 16
}