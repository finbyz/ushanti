frappe.ui.form.on('Sales Order', {
	onload:function(frm) {
		frm.set_query("selling_price_list", function() {
        return {
            "filters": {
                "company":frm.doc.company,
                "selling":1
            }
        };
    });
	}
})