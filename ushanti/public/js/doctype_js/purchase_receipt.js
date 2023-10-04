frappe.ui.form.on('Purchase Receipt', {
	refresh: function(frm) {
        frm.set_query("buying_price_list", function() {
            return {
                "filters": {
                    "company": frm.doc.company,
                    "buying": 1
                }
            };
        });
	}
});