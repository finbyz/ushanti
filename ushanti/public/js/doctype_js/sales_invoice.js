frappe.ui.form.on('Sales Invoice', {
	onload: function(frm){
	    frm.ignore_doctypes_on_cancel_all = ["Delivery Note"]
		console.log("ushanti loaded")
	},
	refresh:function(frm){
	    frm.ignore_doctypes_on_cancel_all = ["Delivery Note"]
	},
})
frappe.ui.form.on('Sales Invoice Item', {
	pallet_size_packages: function (frm, cdt, cdn) {
		console.log("cal")
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
