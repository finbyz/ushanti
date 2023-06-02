from frappe.utils import flt, cstr, nowdate, nowtime, cint
import frappe

def validate(self,method):
    validate_total_of_allocated_amount(self)

def on_submit(self,method):
    if self.total_amount and self.total_allocated_amount:
           if flt(self.total_allocated_amount) != flt(self.total_amount):
            frappe.throw("Total Amount of New Transaction and Total Allocated Amount are Match '<br>' Total Amount = {0} '<br>' Total Allocated Amount = {1}".format(frappe.bold(self.total_amount),frappe.bold(self.total_allocated_amount)))

def validate_total_of_allocated_amount(self):
    total_allocated_amount = 0
    if self.payment_invoice_items:
        for row in self.payment_invoice_items:
            total_allocated_amount += flt(row.allocated_amount)
        self.total_allocated_amount = flt(total_allocated_amount)

