#-*- coding: utf-8 -*-

{
	"name": "Data SPPG dan Dapodik",
	"version": "1.0",
	"depends": [
		"base"
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
		"security/groups.xml",
		"security/ir.model.access.csv",
		"view/menu.xml",
		"view/master_provinsi.xml",
		"report/master_provinsi.xml",
		"view/master_kab_kota.xml",
		"report/master_kab_kota.xml",
		"view/mitra_sppg.xml",
		"report/mitra_sppg.xml",
		"view/master_dapodik.xml",
		"report/master_dapodik.xml"
	],
	"installable": True,
	"auto_install": False,
	"application": True,
	"odooVersion": 16
}