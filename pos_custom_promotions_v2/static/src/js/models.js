odoo.define("pos_custom_promotions_v2.PosModel", function(require) {
    "use strict";

    var models = require('point_of_sale.models');

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        initialize: function(attr, options) {
            _super_orderline.initialize.call(this,attr,options);
            this.is_reward_line = this.is_reward_line || false;
            this.discount_promotions = this.discount_promotions || 0;
            this.price_unit_pdf = this.price_unit_pdf || 0;
            this.descuento_pdf = this.descuento_pdf || 0;
            this.price_so = this.price_so || 0;
            this.new_price = this.new_price || 0;
        },
        init_from_JSON: function(json) {
            _super_orderline.init_from_JSON.apply(this, arguments);
            this.is_reward_line = json.is_reward_line;
            this.discount_promotions = json.discount_promotions;
            this.price_unit_pdf = json.price_unit_pdf;
            this.descuento_pdf = json.descuento_pdf;
            this.price_so = json.price_so;
        },
        export_as_JSON: function() {
            var json = _super_orderline.export_as_JSON.apply(this);
            json.is_reward_line = this.is_reward_line;
            json.discount_promotions = this.discount_promotions;
            json.price_unit_pdf = this.price_unit_pdf;
            json.descuento_pdf = this.descuento_pdf;
            json.price_so = this.price_so;
            return json;
        },
    });

});