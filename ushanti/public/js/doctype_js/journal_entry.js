frappe.ui.form.on('Journal Entry', {
    onload: function(frm){
        frm.set_query('party_address', function(){
            return {
                query: 'frappe.contacts.doctype.address.address.address_query',
                filters: {
                    link_doctype: frm.doc.party_type,
                    link_name: frm.doc.party,
                }
            }
        });
        frm.set_query('party_type', function(){
            return {
                filters: {
                    'name': ['in', 'Customer, Supplier']
                }
            }
        });
		frm.set_query("contact_person", function() {
			if (frm.doc.party) {
				return {
					query: 'frappe.contacts.doctype.contact.contact.contact_query',
					filters: {
						link_doctype: frm.doc.party_type,
						link_name: frm.doc.party
					}
				};
			}
		});
    },
    party_type: function(frm){
        frm.set_value('party',null)
        frm.trigger('clear_fields');
    },
    party : function(frm){
        frm.trigger('clear_fields');
        if(frm.doc.party && frm.doc.party){
            frappe.call({
                method:"erpnext.accounts.party.get_party_details",
                args:{
                    party_type: frm.doc.party_type,
                    party: frm.doc.party,
                },
                callback: function(r){
                    if(r.message){
                        frm.set_value('party_address', r.message[frappe.scrub(frm.doc.party_type) + "_address"])
                        frm.set_value('address_display', r.message.address_display)
                        frm.set_value('contact_person', r.message.contact_person)
                        frm.set_value('contact_email', r.message.contact_email)
                        frm.set_value('contact_mobile', r.message.contact_mobile)
                        frm.set_value('contact_display', r.message.contact_dispaly)
                    }
                }
            });
            frappe.db.get_value(frm.doc.party_type,frm.doc.party,"pan", function(p){
                if (p.pan){
                    frm.set_value('pan',p.pan)
                }
            })
        }
    },
    party_address: function(frm) {
        erpnext.utils.get_address_display(frm);
    },
	contact_person: function(frm) {
		erpnext.utils.get_contact_details(frm);
	},
    clear_fields: function(frm){
        frm.set_value('pan',null)
        frm.set_value('party_address', null)
        frm.set_value('address_display', null)
        frm.set_value('contact_person', null)
        frm.set_value('contact_email', null)
        frm.set_value('contact_mobile', null)
        frm.set_value('contact_display', null)
    }
})