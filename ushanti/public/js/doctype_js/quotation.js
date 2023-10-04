frappe.ui.form.on('Quotation', {
	refresh: function(frm) {
		frm.set_query("selling_price_list", function() {
            return {
                "filters": {
                    "company":frm.doc.company,
                    "selling":1
                }
            };
        });
	}
});