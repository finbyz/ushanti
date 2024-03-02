from __future__ import unicode_literals
from frappe.utils import flt
import frappe
from frappe.model.naming import make_autoname
from frappe.utils import flt,cint, get_url_to_form, nowdate
import frappe
from frappe import _
 
from frappe.contacts.doctype.address.address import get_company_address
from erpnext.accounts.utils import get_fiscal_year, getdate
import datetime
from email.utils import formataddr
from frappe.desk.notifications import get_filters_for
from frappe.model.mapper import get_mapped_doc
from frappe import _
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import make_purchase_invoice
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.accounts.party import get_party_account


@frappe.whitelist()
def cal_handling_loss(self,method):
	total_qty = 0.0
	for item in self.items:
		if item.item_group ==None or item.item_group =='':
			item.item_group=frappe.db.get_value("Item",item.item_name,"item_group")
		if item.item_group !="PACKING MATERIAL":
			total_qty += flt(item.qty)
	self.handling_loss=flt(total_qty) - flt(self.actual_qty)


def work_order_before_cancel(self, method):
	remove_consumption_reference(self)

def remove_consumption_reference(self):
	frappe.db.sql("SET SQL_SAFE_UPDATES = 0")
	frappe.db.sql("delete from `tabManufacturing Consumption Details` where work_order = '{}'".format(self.name))

def autoname(self):
	prefix = self.bank_account + "-" + self.from_date + "-" + self.to_date
	self.name = make_autoname(prefix + '-.##')
	if self.bank:
		mapper_name = self.bank + "-Statement-Settings"
		if not frappe.db.exists("Bank Statement Settings", mapper_name):
			self.create_settings(self.bank)
		self.bank_settings = mapper_name

@frappe.whitelist()
def sales_invoice_payment_remainder():
	if cint(frappe.db.get_value("Accounts Settings",None,"auto_send_payment_reminder_mails")):
		# mail on every sunday
		if getdate().weekday() == 6:
			frappe.enqueue(send_sales_invoice_mails, queue='long', timeout=5000, job_name='Payment Reminder Mails')
			# frappe.enqueue(send_proforma_invoice_mails, queue='long', timeout=5000, job_name='Payment Reminder Mails')
			return "Payment Reminder Mails Send"

@frappe.whitelist()
def send_sales_invoice_mails():
	from frappe.utils import fmt_money

	def header(customer):
		return """<strong>""" + customer + """</strong><br><br>Dear Sir,<br><br>
		Kind attention account department.<br>
		We wish to invite your kind immediate attention to our following bill/s which have remained unpaid till date and are overdue for payment.<br>
		<div align="center">
			<table border="1" cellspacing="0" cellpadding="0" width="100%">
				<thead>
					<tr>
						<th width="16%" valign="top">Bill No</th>
						<th width="12%" valign="top">Bill Date</th>
						<th width="21%" valign="top">Order No</th>
						<th width="15%" valign="top">Order Date</th>
						<th width="15%" valign="top">Net Total</th>
						<th width="16%" valign="top">Actual Amt</th>
						<th width="18%" valign="top">Rem. Amt</th>
					</tr></thead><tbody>"""
				
	def table_content(name, posting_date, po_no, po_date,net_total, grand_total, outstanding_amount):
		posting_date = posting_date.strftime("%d-%m-%Y") if bool(posting_date) else '-'
		po_date = po_date.strftime("%d-%m-%Y") if bool(po_date) else '-'
		print(grand_total)
		grand_total = fmt_money(grand_total, 2 , 'INR')
		outstanding_amount = fmt_money(outstanding_amount, 2 , 'INR')

		return """<tr>
				<td width="16%" valign="top"> {0} </td>
				<td width="12%" valign="top"> {1} </td>
				<td width="21%" valign="top"> {2} </td>
				<td width="15%" valign="top"> {3} </td>
				<td width="15%" valign="top"> {4} </td>
				<td width="16%" valign="top" align="right"> {5} </td>
				<td width="18%" valign="top" align="right"> {6} </td>
			</tr>""".format(name, posting_date, po_no or '-', po_date,net_total, grand_total, outstanding_amount)

	def footer(actual_amount, outstanding_amount):
		actual_amt = fmt_money(sum(actual_amount), 2, 'INR')
		outstanding_amt = fmt_money(sum(outstanding_amount), 2, 'INR')
		return """<tr>
					<td width="68%" colspan="4" valign="top" align="right">
						<strong>Net Receivable &nbsp; </strong>
					</td>
					<td align="right" width="13%" valign="top">
						<strong> {} </strong>
					</td>
					<td align="right" width="18%" valign="top">
						<strong> {} </strong>
					</td>
				</tr></tbody></table></div><br>
				We request you to look into the matter and release the payment/s without Further delay. <br><br>
				If you need any clarifications for any of above invoice/s, please reach out to our Accounts Receivable Team by sending email to test@gmail.com<br><br>
				We will appreciate your immediate response in this regard.<br><br>
				
				Thanking you in anticipation.<br><br>For,  Ushanti Colour Chem Ltd.
				""".format(actual_amt, outstanding_amt)

	non_customers = ()
	data = frappe.get_list("Sales Invoice", filters={
			'status': ['in', ('Overdue')],
			'outstanding_amount':(">", 5000),
			'currency': 'INR',
			'docstatus': 1,
			'customer': ['not in', non_customers],},
			order_by='posting_date',
			fields=["name", "customer", "posting_date", "po_no", "po_date", "rounded_total", "outstanding_amount", "contact_email", "naming_series" , "grand_total"])

	def get_customers():
		customers_list = list(set([d.customer for d in data if d.customer]))
		customers_list.sort()

		for customer in customers_list:
			yield customer

	def get_customer_si(customer):
		for d in data:
			if d.customer == customer:
				yield d

	customers = get_customers()

	sender = formataddr(("Ushanti Colour Chem Ltd.", "erp.ushanti@gmail.com"))
	for customer in customers:
		attachments, outstanding, actual_amount, recipients = [], [], [], []
		table = ''

		# customer_si = [d for d in data if d.customer == customer]
		customer_si = get_customer_si(customer)

		for si in customer_si:
			print(si)
			name = "Previous Year Outstanding"
			if si.naming_series != "PI-":
				name = si.name
				try:
					attachments.append(frappe.attach_print('Sales Invoice', si.name, print_format="Domestic Sales Invoice", print_letterhead=True))
				except:
					pass
			print(si.grand_total)
			table += table_content(name, si.posting_date, si.po_no, si.po_date,si.net_total,
						si.grand_total, si.outstanding_amount)

			outstanding.append(si.outstanding_amount)
			actual_amount.append(si.rounded_total or 0.0)

			if bool(si.contact_email) and si.contact_email not in recipients:
				recipients.append(si.contact_email)


		message = header(customer) + '' + table + '' + footer(actual_amount, outstanding)
		recipients = ["info.ushanti@gmail.com"]
		try:
			frappe.sendmail(
				recipients=recipients,
				cc = '',
				subject = 'Overdue Invoices: ' + customer,
				sender = sender,
				message = message,
				attachments = attachments
			)
		except:
			frappe.log_error("Mail Sending Issue", frappe.get_traceback())
			continue

def set_base_amount_in_ss(self , method):
	base = frappe.db.get_value("Salary Structure Assignment",{'salary_structure':self.salary_structure},'base')
	self.base = base

def set_total_of_esic_diduction(self,method):
	if self.earnings:
		esic_amount = 0
		for row in self.earnings:
			if row.salary_component not in ["Washing Allowance", "Conveyance Allowance"]:
				esic_amount += row.amount
		self.esic_deduction = esic_amount

@frappe.whitelist()
def make_purchase_invoice_from_purchase_order(source_name, target_doc=None):
	return get_mapped_purchase_invoice(source_name, target_doc)

def set_missing_values_from_purchase_order_to_purchase_invoice(source, target):
	target.run_method("set_missing_values")
	target.run_method("calculate_taxes_and_totals")

def get_mapped_purchase_invoice(source_name, target_doc=None, ignore_permissions=False):
	def postprocess(source, target):
		target.flags.ignore_permissions = ignore_permissions
		set_missing_values_from_purchase_order_to_purchase_invoice(source, target)
		# Get the advance paid Journal Entries in Purchase Invoice Advance
		if target.get("allocate_advances_automatically"):
			target.set_advances()

		target.set_payment_schedule()
		target.credit_to = get_party_account("Supplier", source.supplier, source.company)

	def update_item(obj, target, source_parent):
		target.amount = flt(obj.amount) - flt(obj.billed_amt)
		target.base_amount = target.amount * flt(source_parent.conversion_rate)
		target.qty = (
			target.amount / flt(obj.rate) if (flt(obj.rate) and flt(obj.billed_amt)) else flt(obj.qty)
		)

		item = get_item_defaults(target.item_code, source_parent.company)
		item_group = get_item_group_defaults(target.item_code, source_parent.company)
		target.cost_center = (
			obj.cost_center
			or frappe.db.get_value("Project", obj.project, "cost_center")
			or item.get("buying_cost_center")
			or item_group.get("buying_cost_center")
		)

	fields = {
		"Purchase Order": {
			"doctype": "Purchase Invoice",
			"field_map": {
				"party_account_currency": "party_account_currency",
				"supplier_warehouse": "supplier_warehouse",
				"payment_terms_template": "payment_terms_template"
			},
			"field_no_map": ["payment_terms_template"],
			"validation": {
				"docstatus": ["=", 1],
			},
		},
		"Purchase Order Item": {
			"doctype": "Purchase Invoice Item",
			"field_map": {
				"name": "po_detail",
				"parent": "purchase_order",
			},
			"postprocess": update_item,
			"condition": lambda doc: (doc.base_amount == 0 or abs(doc.billed_amt) < abs(doc.amount)),
		},
		"Purchase Taxes and Charges": {"doctype": "Purchase Taxes and Charges", "add_if_empty": True},
	}

	doc = get_mapped_doc(
		"Purchase Order",
		source_name,
		fields,
		target_doc,
		postprocess,
		ignore_permissions=ignore_permissions,
	)
	doc.set_onload("ignore_price_list", True)

	return doc


@frappe.whitelist()
def make_purchase_invoice(source_name, target_doc=None):
	from erpnext.accounts.party import get_payment_terms_template

	doc = frappe.get_doc("Purchase Receipt", source_name)
	returned_qty_map = get_returned_qty_map(source_name)
	invoiced_qty_map = get_invoiced_qty_map(source_name)

	def set_missing_values(source, target):
		if len(target.get("items")) == 0:
			frappe.throw(_("All items have already been Invoiced/Returned"))

		doc = frappe.get_doc(target)
		doc.payment_terms_template = get_payment_terms_template(
			source.supplier, "Supplier", source.company
		)
		doc.run_method("onload")
		doc.run_method("set_missing_values")
		doc.run_method("calculate_taxes_and_totals")
		doc.set_payment_schedule()

	def update_item(source_doc, target_doc, source_parent):
		target_doc.qty, returned_qty = get_pending_qty(source_doc)
		if frappe.db.get_single_value(
			"Buying Settings", "bill_for_rejected_quantity_in_purchase_invoice"
		):
			target_doc.rejected_qty = 0
		target_doc.stock_qty = flt(target_doc.qty) * flt(
			target_doc.conversion_factor, target_doc.precision("conversion_factor")
		)
		returned_qty_map[source_doc.name] = returned_qty

	def get_pending_qty(item_row):
		qty = item_row.qty
		if frappe.db.get_single_value(
			"Buying Settings", "bill_for_rejected_quantity_in_purchase_invoice"
		):
			qty = item_row.received_qty
		pending_qty = qty - invoiced_qty_map.get(item_row.name, 0)
		returned_qty = flt(returned_qty_map.get(item_row.name, 0))
		if returned_qty:
			if returned_qty >= pending_qty:
				pending_qty = 0
				returned_qty -= pending_qty
			else:
				pending_qty -= returned_qty
				returned_qty = 0
		return pending_qty, returned_qty

	doclist = get_mapped_doc(
		"Purchase Receipt",
		source_name,
		{
			"Purchase Receipt": {
				"doctype": "Purchase Invoice",
				"field_map": {
					"supplier_warehouse": "supplier_warehouse",
					"is_return": "is_return",
					"bill_date": "bill_date",
					"posting_date":"posting_date",
					"posting_time":"posting_time",
				},
				"validation": {
					"docstatus": ["=", 1],
				},
			},
			"Purchase Receipt Item": {
				"doctype": "Purchase Invoice Item",
				"field_map": {
					"name": "pr_detail",
					"parent": "purchase_receipt",
					"purchase_order_item": "po_detail",
					"purchase_order": "purchase_order",
					"is_fixed_asset": "is_fixed_asset",
					"asset_location": "asset_location",
					"asset_category": "asset_category",
				},
				"postprocess": update_item,
				"filter": lambda d: get_pending_qty(d)[0] <= 0
				if not doc.get("is_return")
				else get_pending_qty(d)[0] > 0,
			},
			"Purchase Taxes and Charges": {"doctype": "Purchase Taxes and Charges", "add_if_empty": True},
		},
		target_doc,
		set_missing_values,
	)

	doclist.set_onload("ignore_price_list", True)
	return doclist

def get_invoiced_qty_map(purchase_receipt):
	"""returns a map: {pr_detail: invoiced_qty}"""
	invoiced_qty_map = {}

	for pr_detail, qty in frappe.db.sql(
		"""select pr_detail, qty from `tabPurchase Invoice Item`
		where purchase_receipt=%s and docstatus=1""",
		purchase_receipt,
	):
		if not invoiced_qty_map.get(pr_detail):
			invoiced_qty_map[pr_detail] = 0
		invoiced_qty_map[pr_detail] += qty

	return invoiced_qty_map

def get_returned_qty_map(purchase_receipt):
	"""returns a map: {so_detail: returned_qty}"""
	returned_qty_map = frappe._dict(
		frappe.db.sql(
			"""select pr_item.purchase_receipt_item, abs(pr_item.qty) as qty
		from `tabPurchase Receipt Item` pr_item, `tabPurchase Receipt` pr
		where pr.name = pr_item.parent
			and pr.docstatus = 1
			and pr.is_return = 1
			and pr.return_against = %s
	""",
			purchase_receipt,
		)
	)

	return returned_qty_map