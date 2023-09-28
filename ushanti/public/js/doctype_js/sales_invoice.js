frappe.ui.form.on('Sales Invoice', {
	onload: function(frm){
	    frm.ignore_doctypes_on_cancel_all = ["Delivery Note"]
	},
	refresh:function(frm){
	    frm.ignore_doctypes_on_cancel_all = ["Delivery Note"]
	},
    weighbridge_address_: function (frm) {
        if(frm.doc.weighbridge_address_){
            return frappe.call({
                method: "frappe.contacts.doctype.address.address.get_address_display",
                args: {
                    "address_dict": frm.doc.weighbridge_address_
                },
                callback: function (r) {
                    if (r.message)
                        frm.set_value("weighbridge_address_display", r.message);
                }
            });
        }
    }
})
frappe.ui.form.on('Sales Invoice Item', {
	pallet_size_packages: function (frm, cdt, cdn) {
        frappe.run_serially([
            () => {
                let d = locals[cdt][cdn]; 
				frappe.model.set_value(cdt, cdn, "total_pallets",Math.round(d.no_of_packages/  d.pallet_size_packages));
                // frappe.model.set_value(cdt, cdn, "total_pallets", Math.round(d.qty / d.pallet_size));
            },
            () => {
                frm.events.pallet_cal(frm);
            }
        ]);
    },
})
