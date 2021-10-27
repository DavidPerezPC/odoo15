odoo.define("pos_client_ref_screen.models", function(require) {
    "use strict";

    var rpc = require('web.rpc');
    var models = require('point_of_sale.models');

    var field_utils = require('web.field_utils');
    models.load_fields('res.partner', ['ref','company_id','parent_id','property_product_pricelist','pos_order_count','total_invoiced','customer_rank', 'l10n_mx_edi_colony','l10n_mx_edi_locality_id', 'property_payment_term_id']);
    var super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({

        initialize: function (session, attributes) {
            var partner_model = _.find(this.models, function (model){
                model.order = [{name: "name"}];
                return model.model === 'res.partner';
            });
            partner_model.fields.push('ref','company_id','parent_id','property_product_pricelist','pos_order_count','total_invoiced','customer_rank', 'l10n_mx_edi_colony','l10n_mx_edi_locality_id', 'property_payment_term_id');
            return super_posmodel.initialize.call(this, session, attributes);
        },
    });
/*
       models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var partner_model = _.find(this.models, function(model){
                return model.model === 'res.partner';
            });
            partner_model.domain.push(['company_id','=',self.config.company_id[0]]);
            return _super_posmodel.initialize.call(this, session, attributes);
        },
    });*/


});