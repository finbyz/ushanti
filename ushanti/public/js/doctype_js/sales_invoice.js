frappe.ui.form.on('Sales Invoice', {
	onload: function(frm){
	    frm.ignore_doctypes_on_cancel_all = ["Delivery Note"]
	},
	refresh:function(frm){
	    frm.ignore_doctypes_on_cancel_all = ["Delivery Note"]
	}
})