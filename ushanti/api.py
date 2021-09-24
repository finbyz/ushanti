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
