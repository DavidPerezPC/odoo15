odoo.define("pos_ticket_template.models", function(require) {
    "use strict";

    var rpc = require('web.rpc');
    var models = require('point_of_sale.models');
    // models.load_fields('res.company',['street_name','street_number','country_id','zip','city','state_id']);
    models.load_fields('res.company',['street_name','street_number','street_number2','street','street2', 'country_id','l10n_mx_edi_colony','l10n_mx_edi_locality_id','zip','city','state_id','parent_id']);
    var super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var res_company_model = _.find(this.models, function (model){
                return model.model === 'res.company';
            });
            res_company_model.fields.push('street_name','street_number','street_number2','street','street2', 'country_id','l10n_mx_edi_colony','l10n_mx_edi_locality_id','zip','city','state_id');
             //res_company_model.fields.push('street_name','street_number','street','street2', 'country_id','zip','city','state_id');
             var amount_in_words;
              var pos_date_due;
              var total_discount_tarifa;
              var discountpromo;
              var invoice_number;
              var onchange_promotions= this.onchange_promotions || 0;

            return super_posmodel.initialize.call(this, session, attributes);
        },
    });
    var _super_ordermodel = models.Order.prototype;
    models.Order = models.Order.extend({
      initialize: function(attr, options) {
            _super_ordermodel.initialize.call(this,attr,options);
            this.to_invoice = true; //para imprimir factura automaticamente al validar pos_order
             this.onchange_promotions= this.onchange_promotions || 0;
        },
        init_from_JSON: function(json) {
            _super_ordermodel.init_from_JSON.apply(this, arguments);
             if (json.to_invoice) {
                this.to_invoice = json.to_invoice;
                console.log(this)
            }
             this.onchange_promotions= this.onchange_promotions

        },

    export_for_printing: function(){
        var receipt = _super_ordermodel.export_for_printing.apply(this, arguments);

        receipt.amount_in_words = this.amount_in_words;
        receipt.pos_date_due=this.pos_date_due;
        receipt.total_discount_tarifa=this.total_discount_tarifa;
        receipt.discountpromo = this.discountpromo;
        receipt.price_discount= this.price_discount;
        console.log(this.onchange_promotions)
         if(this.invoice_number){
             receipt.invoice_number=this.invoice_number;
              $(this.el).find('.pos-receipt-container').html(receipt);

           }
        return receipt;
       },
   });
});