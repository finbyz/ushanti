from . import __version__ as app_version
from ushanti.api import autoname
from finbyzerp.finbyzerp.doctype.bank_statement_transaction_entry.bank_statement_transaction_entry import BankStatementTransactionEntry

BankStatementTransactionEntry.autoname =  autoname

app_name = "ushanti"
app_title = "ushanti"
app_publisher = "FinByz Tech Pvt. Ltd."
app_description = "Custom app for ushanti"
app_icon = "octicon octicon-file-directory"
app_color = "blue"
app_email = "info@finbyz.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ushanti/css/ushanti.css"
# app_include_js = "/assets/ushanti/js/ushanti.js"

# app_include_js = "/assets/js/ushanti.min.js"
app_include_js = [
	"ushanti.bundle.js"
]

# include js, css files in header of web template
# web_include_css = "/assets/ushanti/css/ushanti.css"
# web_include_js = "/assets/ushanti/js/ushanti.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ushanti/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}


override_doctype_class = {
	"Bank Clearance": "ushanti.bank_clearance_ovverride.CustomBankClearance"
}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

doctype_js = {
	"Quotation" : "public/js/doctype_js/quotation.js",
	"Sales Order" : "public/js/doctype_js/sales_order.js",
	"Delivery Note": "public/js/doctype_js/delivery_note.js",
	"Sales Invoice" : "public/js/doctype_js/sales_invoice.js",
	"Journal Entry" : "public/js/doctype_js/journal_entry.js",
	"Purchase Order" : "public/js/doctype_js/purchase_order.js",
	"Purchase Receipt" : "public/js/doctype_js/purchase_receipt.js",
	"Purchase Invoice" : "public/js/doctype_js/purchase_invoice.js"
	}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ushanti.install.before_install"
# after_install = "ushanti.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ushanti.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Ball Mill Data Sheet":{
		"before_save":'ushanti.api.cal_handling_loss'
		},
	"Work Order":{
		"before_cancel": "ushanti.api.work_order_before_cancel"
	},
	"Bank Statement Transaction Entry":{
		"validate":"ushanti.ushanti.doc_event.bank_statement_transaction_entry.validate",
		"on_submit":"ushanti.ushanti.doc_event.bank_statement_transaction_entry.on_submit"
	},
	"Salary Slip":{
		'validate':"ushanti.api.set_base_amount_in_ss",
		"on_submit":"ushanti.api.set_total_of_esic_diduction"
	},
	"Rodtap Claimed Management":{
		"on_submit":"ushanti.ushanti.doctype.rodtap_claimed_management.rodtap_claimed_management.create_jv_on_submit"
	},
	"Delivery Note":{
		"on_submit" : "ushanti.ushanti.doc_event.delivery_note.on_submit",
		"before_cancel":"ushanti.ushanti.doc_event.delivery_note.before_cancel"
	}
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
}

# Scheduled Tasks
# ---------------
override_whitelisted_methods = {
	"erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_purchase_invoice":"ushanti.api.make_purchase_invoice",
}


scheduler_events = {
# 	"all": [
# 		"ushanti.tasks.all"
# 	],
	"daily": [
		"ushanti.api.sales_invoice_payment_remainder"
	],
# 	"hourly": [
# 		"ushanti.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ushanti.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ushanti.tasks.monthly"
# 	]
}

# Testing
# -------

# before_tests = "ushanti.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ushanti.event.get_events"
# }
#
# override_whitelisted_methods = {
# 	"erpnext.selling.doctype.sales_order.sales_order.make_sales_invoice": "ushanti.ushanti.doc_event.sales_order.make_sales_invoice"
# }
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Inward Sample": "ushanti.ushanti.doc_event.inward_sample_dashboard"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ushanti.auth.validate"
# ]


from erpnext.accounts.report.tds_computation_summary import tds_computation_summary
from ushanti.ushanti.report.tds_computation_summary import execute as tds_computation_summary_execute
tds_computation_summary.execute = tds_computation_summary_execute

# from erpnext.accounts.report.tds_payable_monthly import tds_payable_monthly
# from ushanti.ushanti.report.tds_payable_monthly import execute as tds_payable_monthly_execute
# tds_payable_monthly.execute = tds_payable_monthly_execute

from india_compliance.gst_india.doctype.gstr_3b_report.gstr_3b_report import GSTR3BReport
from ushanti.ushanti.report.gstr_3b_report import GSTR3BReport as custom_GSTR3BReport
GSTR3BReport.validate = custom_GSTR3BReport.validate

from hrms.payroll.report.provident_fund_deductions import provident_fund_deductions
from ushanti.ushanti.report.provident_fund_deductions import execute as override_report_execute
provident_fund_deductions.execute = override_report_execute

from erpnext.selling.doctype.sales_order import sales_order
from ushanti.ushanti.doc_event.sales_order import make_sales_invoice
sales_order.make_sales_invoice = make_sales_invoice

from chemical.chemical.doc_events import stock_entry 
from ushanti.ushanti.doc_event.stock_entry import update_po_transfer_qty
stock_entry.update_po_transfer_qty = update_po_transfer_qty

from india_compliance.gst_india.report.gstr_1.gstr_1 import Gstr1Report
from ushanti.gstr_1 import get_row_data_for_invoice
Gstr1Report.get_row_data_for_invoice = get_row_data_for_invoice