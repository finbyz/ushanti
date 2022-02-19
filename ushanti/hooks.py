from . import __version__ as app_version

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

app_include_js = "/assets/js/ushanti.min.js"

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

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

doctype_js = {
	"Sales Invoice" : "public/js/doctype_js/sales_invoice.js",
	"Journal Entry" : "public/js/doctype_js/journal_entry.js"
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
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ushanti.tasks.all"
# 	],
# 	"daily": [
# 		"ushanti.tasks.daily"
# 	],
# 	"hourly": [
# 		"ushanti.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ushanti.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ushanti.tasks.monthly"
# 	]
# }

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
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ushanti.task.get_dashboard_data"
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

from erpnext.accounts.report.tds_payable_monthly import tds_payable_monthly
from ushanti.ushanti.report.tds_payable_monthly import execute as tds_payable_monthly_execute
tds_payable_monthly.execute = tds_payable_monthly_execute

from erpnext.regional.doctype.gstr_3b_report.gstr_3b_report import GSTR3BReport
from ushanti.ushanti.report.gstr_3b_report import GSTR3BReport as custom_GSTR3BReport
GSTR3BReport.validate = custom_GSTR3BReport.validate