frappe.ui.form.on("Lead", {
	refresh: function (frm) {
	  frm.set_query("ref_id", "samples_details", function (doc, cdt, cdn) {
		let row = locals[cdt][cdn];
		return {
		  "filters": {
			"product_name": row.product_id
		  },
		};
	  });
	},
  });