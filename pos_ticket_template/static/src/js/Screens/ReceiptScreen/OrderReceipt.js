odoo.define('pos_ticket_template.OrderReceipt', function(require) {
    'use strict';

    const OrderReceipt = require('point_of_sale.OrderReceipt');
    const Registries = require('point_of_sale.Registries');

    var models = require('point_of_sale.models');
    models.load_fields('res.company',['street','street2', 'country_id','zip','city','state_id']);

    const InheritOrderReceipt = (OrderReceipt) => class extends OrderReceipt {
        constructor() {
            super(...arguments);
            this.res_company = this.env.pos.res_company;
            this._receiptEnv = this.props.order.getOrderReceiptEnv();
        }
    };
    Registries.Component.extend(OrderReceipt, InheritOrderReceipt);
    return OrderReceipt;
});