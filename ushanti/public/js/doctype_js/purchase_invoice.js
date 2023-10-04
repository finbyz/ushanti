frappe.ui.form.on('Purchase Invoice', {
	refresh: function(frm) {
		setTimeout(() => {
			frm.set_query("buying_price_list", function() {
				return {
					"filters": {
						"company": frm.doc.company,
						"buying": 1
					}
				};
			});
		}, 10);
	}
});