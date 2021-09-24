frappe.provide('erpnext')

erpnext.show_serial_batch_selector = function (frm, d, callback, on_close, show_dialog) {
	let warehouse, receiving_stock, existing_stock;
	if (frm.doc.is_return) {
		if (["Purchase Receipt", "Purchase Invoice"].includes(frm.doc.doctype)) {
			existing_stock = true;
			warehouse = d.warehouse;
		} else if (["Delivery Note", "Sales Invoice"].includes(frm.doc.doctype)) {
			receiving_stock = true;
		}
	} else {
		if (frm.doc.doctype == "Stock Entry") {
			if (frm.doc.purpose == "Material Receipt") {
				receiving_stock = true;
			} else {
				existing_stock = true;
				warehouse = d.s_warehouse;
			}
		} else {
			existing_stock = true;
			warehouse = d.warehouse;
		}
	}

	if (!warehouse) {
		if (receiving_stock) {
			warehouse = ["like", ""];
		} else if (existing_stock) {
			warehouse = ["!=", ""];
		}
	}

	frappe.require("/assets/ushanti/js/serial_no_batch_selector.js", function() {
		new erpnext.SerialNoBatchSelector({
			frm: frm,
			item: d,
			warehouse_details: {
				type: "Warehouse",
				name: warehouse
			},
			callback: callback,
			on_close: on_close
		}, show_dialog);
	});
}
