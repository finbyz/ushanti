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
		grand_total = fmt_money(grand_total,  'INR')
		outstanding_amount = fmt_money(outstanding_amount, 'INR')

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
			fields=["name", "customer", "posting_date", "po_no", "po_date", "rounded_total", "outstanding_amount", "contact_email", "naming_series"])

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