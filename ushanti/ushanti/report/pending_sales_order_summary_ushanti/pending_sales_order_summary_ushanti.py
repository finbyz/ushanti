# Copyright (c) 2023, FinByz Tech Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _



def execute(filters=None):
	columns, data = [], []

	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data

def get_columns(filters):
	return [
		{
			"label": _("Sales Order"),
			"fieldname": "sales_order",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 150,
		},
		{
			"label": _("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 100,
		},
		{
			"label": _("Date"),
			"fieldname": "transaction_date",
			"fieldtype": "Date",
			"width": 100,
		},
		{
			"label": _("Order No"),
			"fieldname": "order_no",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Link",
			"options": "Item",
			"width": 100,
		},
		{
			"label": _("Qty"),
			"fieldname": "qty",
			"fieldtype": "Float",
			"width": 80,
		},
		{
			"label": _("Pending Qty"),
			"fieldname": "pending_qty",
			"fieldtype": "Float",
			"width": 80,
		},
		{
			"label": _("PSS"),
			"fieldname": "pss",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Standard"),
			"fieldname": "standard",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Standard Percentage"),
			"fieldname": "standard_percentage",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Parameters"),
			"fieldname": "parameters",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Tone Sales"),
			"fieldname": "tone_sales",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Customer Quality"),
			"fieldname": "customer_quality",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Special Remarks"),
			"fieldname": "special_remarks",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Special Method"),
			"fieldname": "special_method",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Packaging Material"),
			"fieldname": "packaging_material",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Packing Size"),
			"fieldname": "packing_size",
			"fieldtype": "Float",
			"width": 80,
		},
		{
			"label": _("KP Remarks"),
			"fieldname": "kp_remarks",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Last Dispatch"),
			"fieldname": "last_dispatch",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Batch No"),
			"fieldname": "batch_no",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Party Code"),
			"fieldname": "party_code",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Dispatch Date"),
			"fieldname": "dispatch_date",
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 80,
		},
	]

def get_data(filters):
	data = frappe.db.sql(f"""
		select 
			`tabSales Order`.`name` as sales_order,
			`tabSales Order`.`company`,
			`tabSales Order`.`transaction_date`,
			`tabSales Order`.`order_no`,
			`tabSales Order`.`customer`,
			`tabSales Order Item`.item_name ,
			`tabSales Order Item`.qty,
			(`tabSales Order Item`.qty - ifnull(`tabSales Order Item`.delivered_qty, 0)) as pending_qty,
			`tabSales Order Item`.pss,
			`tabSales Order Item`.standard ,
			`tabSales Order Item`.standard_percentage,
			`tabSales Order Item`.parameters,
			`tabSales Order Item`.tone_ as tone_sales,
			`tabSales Order Item`.party_code as customer_quality,
			`tabSales Order Item`.special_remarks,
			`tabSales Order Item`.special_method,
			`tabSales Order Item`.packaging_material,
			`tabSales Order Item`.packing_size,
			`tabSales Order Item`.kp_remarks,
			`tabSales Order Item`.last_dispatch,
			`tabSales Order Item`.batch_no,
			`tabSales Order Item`.party as party_code,
			`tabSales Order Item`.dispatch_date,
			`tabSales Order`.status
			
			from
			`tabSales Order` JOIN `tabSales Order Item` join `tabItem` JOIN `tabCustomer Group`

			where
			`tabSales Order Item`.`parent` = `tabSales Order`.`name`
			and `tabSales Order`.docstatus < 2
			and `tabCustomer Group`.`customer_group_name` = `tabSales Order`.`customer_group`
			and `tabItem`.name = `tabSales Order Item`.item_code
			and `tabSales Order`.status not in ("Stopped", "Closed")
			and ifnull(`tabSales Order Item`.delivered_qty,0) < ifnull(`tabSales Order Item`.qty,0)
			and  `tabSales Order`.company = '{filters.get('company')}'
			
			ORDER BY  `tabSales Order`.`name` DESC 
	""", as_dict = 1)
	return data