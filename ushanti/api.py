from frappe.utils import flt
import frappe

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
