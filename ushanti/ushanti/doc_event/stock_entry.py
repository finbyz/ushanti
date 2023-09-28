import frappe
from frappe.utils import flt

def update_po_transfer_qty(self, po):
	for d in po.required_items:
		se_items_date = frappe.db.sql('''select sum(quantity), valuation_rate
			from `tabStock Entry` entry, `tabStock Entry Detail` detail
			where
				entry.work_order = %s
				and entry.purpose = "Material Transfer for Manufacture"
				and entry.docstatus = 1
				and detail.parent = entry.name
				and detail.item_code = %s''', (po.name, d.item_code))[0]
				
		d.db_set('transferred_qty', flt(se_items_date[0]), update_modified = False)
		d.db_set('valuation_rate', flt(se_items_date[1]), update_modified = False)
