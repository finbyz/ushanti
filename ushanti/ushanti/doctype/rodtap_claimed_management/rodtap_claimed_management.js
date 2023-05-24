// Copyright (c) 2022, FinByz Tech Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rodtap Claimed Management', {
	get_rodtap_entries:function(frm){
		if (frm.doc.rodtap_details) {
            for (var j = frm.doc.rodtap_details.length - 1; j >= 0; j--) {
                cur_frm.get_field("rodtap_details").grid.grid_rows[j].remove();
            }
        }
		frappe.call({
			method : "ushanti.ushanti.doctype.rodtap_claimed_management.rodtap_claimed_management.journal_entry_list",
			args:{
				"start_date":frm.doc.start_date,
				"end_date":frm.doc.end_date
			},
			callback: function(r) {
				
				r.message.forEach(function(res) {
					var childTable = cur_frm.add_child("rodtap_details");
					childTable.je_no = res['je_no']
					childTable.shipping_bill_no = res['shipping_bill_no']
					childTable.account = res['account']
					childTable.debit_amount = res['debit_amount']
					childTable.cheque_date = res['cheque_date']
				})
				
				cur_frm.refresh();
					
				
			}
		});
		
	},
});