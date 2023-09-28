import frappe
from frappe.utils import flt, formatdate, getdate


def get_row_data_for_invoice(self, invoice, invoice_details, tax_rate, items):
    row = []
    for fieldname in self.invoice_fields:
        if (
            self.filters.get("type_of_business") in ("CDNR-REG", "CDNR-UNREG")
            and fieldname == "invoice_value"
        ):
            row.append(
                abs(invoice_details.base_rounded_total)
                or abs(invoice_details.base_grand_total)
            )
        elif fieldname == "invoice_value":
            if invoice_details.get("export_type"):
                invoice_value = (invoice_details.base_rounded_total * tax_rate) / 100
                invoice_value_with_tax  = invoice_details.base_rounded_total + invoice_value 
                row.append(
                    invoice_value_with_tax
                    or invoice_details.base_grand_total
                )
            else:
                row.append(
                    invoice_details.base_rounded_total
                    or invoice_details.base_grand_total
                )
        elif fieldname in ("posting_date", "shipping_bill_date"):
            row.append(formatdate(invoice_details.get(fieldname), "dd-MMM-YY"))
        elif fieldname == "export_type":
            export_type = "WPAY" if invoice_details.get(fieldname) else "WOPAY"
            row.append(export_type)
        else:
            row.append(invoice_details.get(fieldname))
    taxable_value = 0

    for item_code, net_amount in self.invoice_items.get(invoice).items():
        if item_code in items:
            taxable_value += abs(net_amount)

    row += [tax_rate or 0, taxable_value]

    for column in self.other_columns:
        if column.get("fieldname") == "cess_amount":
            row.append(flt(self.invoice_cess.get(invoice), 2))

    return row, taxable_value
