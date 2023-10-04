frappe.ui.form.on('Delivery Note', {
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