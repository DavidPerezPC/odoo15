odoo.define("pos_precio_lista_precio.PosModel", function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    var utils = require('web.utils');

    var OrderlineSuper = models.Orderline;
    var round_pr = utils.round_precision;

    models.Orderline = models.Orderline.extend({
        get_fixed_lst_price: function() {
            var precio_base = OrderlineSuper.prototype.get_fixed_lst_price.apply(this, arguments);
            let product_tmpl_id = this.product.product_tmpl_id
            let encontro = false

            var BreakException = {};
            try{
                this.order.pricelist.items.forEach((value) => {
                    if(value.product_tmpl_id && value.product_tmpl_id[0] == product_tmpl_id){

                        precio_base =  parseFloat(value.price.replace("$", ""));
                        encontro = true
                        if (encontro) throw BreakException;
                    }
                })
            }catch (e) {
              if (e !== BreakException) throw e;
            }

            if (!encontro){
                this.order.pricelist.items.forEach((value) => {
                    if(value.base_pricelist_id){
                        BreakException = {};
                        try{
                            this.pos.pricelists.find(e => e.id == value.base_pricelist_id[0]).items.forEach((value) => {
                                if(value.product_tmpl_id && value.product_tmpl_id[0] == product_tmpl_id){

                                    precio_base =  parseFloat(value.price.replace("$", ""));
                                    encontro = true
                                    if (encontro) throw BreakException;
                                }
                            })
                        }catch (e) {
                          if (e !== BreakException) throw e;
                        }
                    }
                })
            }

            return precio_base;
        },
        compute_all: function(taxes, price_unit, quantity, currency_rounding, handle_price_include=true) {
            var self = this;

            var _collect_taxes = function(taxes, all_taxes){
                taxes.sort(function (tax1, tax2) {
                    return tax1.sequence - tax2.sequence;
                });
                _(taxes).each(function(tax){
                    if(tax.amount_type === 'group')
                        all_taxes = _collect_taxes(tax.children_tax_ids, all_taxes);
                    else
                        all_taxes.push(tax);
                });
                return all_taxes;
            }
            var collect_taxes = function(taxes){
                return _collect_taxes(taxes, []);
            }

            taxes = collect_taxes(taxes);
            var initial_currency_rounding = 0.000001

            var recompute_base = function(base_amount, fixed_amount, percent_amount, division_amount){
                 return (base_amount - fixed_amount) / (1.0 + percent_amount / 100.0) * (100 - division_amount) / 100;
            }

            var base = round_pr(price_unit * quantity, initial_currency_rounding);

            var sign = 1;
            if(base < 0){
                base = -base;
                sign = -1;
            }

            var total_included_checkpoints = {};
            var i = taxes.length - 1;
            var store_included_tax_total = true;

            var incl_fixed_amount = 0.0;
            var incl_percent_amount = 0.0;
            var incl_division_amount = 0.0;

            var cached_tax_amounts = {};
            if (handle_price_include){
                _(taxes.reverse()).each(function(tax){
                    if(tax.include_base_amount){
                        base = recompute_base(base, incl_fixed_amount, incl_percent_amount, incl_division_amount);
                        incl_fixed_amount = 0.0;
                        incl_percent_amount = 0.0;
                        incl_division_amount = 0.0;
                        store_included_tax_total = true;
                    }
                    if(tax.price_include){
                        if(tax.amount_type === 'percent')
                            incl_percent_amount += tax.amount;
                        else if(tax.amount_type === 'division')
                            incl_division_amount += tax.amount;
                        else if(tax.amount_type === 'fixed')
                            incl_fixed_amount += quantity * tax.amount
                        else{
                            var tax_amount = self._compute_all(tax, base, quantity);
                            incl_fixed_amount += tax_amount;
                            cached_tax_amounts[i] = tax_amount;
                        }
                        if(store_included_tax_total){
                            total_included_checkpoints[i] = base;
                            store_included_tax_total = false;
                        }
                    }
                    i -= 1;
                });
            }

            var total_excluded = round_pr(recompute_base(base, incl_fixed_amount, incl_percent_amount, incl_division_amount), initial_currency_rounding);
            var total_included = total_excluded;

            base = total_excluded;

            var skip_checkpoint = false;

            var taxes_vals = [];
            i = 0;
            var cumulated_tax_included_amount = 0;
            _(taxes.reverse()).each(function(tax){
                if(!skip_checkpoint && tax.price_include && total_included_checkpoints[i] !== undefined){
                    var tax_amount = total_included_checkpoints[i] - (base + cumulated_tax_included_amount);
                    cumulated_tax_included_amount = 0;
                }else
                    var tax_amount = self._compute_all(tax, base, quantity, true);

                tax_amount = round_pr(tax_amount, currency_rounding);

                if(tax.price_include && total_included_checkpoints[i] === undefined)
                    cumulated_tax_included_amount += tax_amount;

                taxes_vals.push({
                    'id': tax.id,
                    'name': tax.name,
                    'amount': sign * tax_amount,
                    'base': sign * round_pr(base, currency_rounding),
                });

                if(tax.include_base_amount){
                    base += tax_amount;
                    if(!tax.price_include)
                        skip_checkpoint = true;
                }

                total_included += tax_amount;
                i += 1;
            });

            return {
                'taxes': taxes_vals,
                'total_excluded': sign * round_pr(total_excluded, 0.000001),
                'total_included': sign * round_pr(total_included, 0.000001),
            }
        },

    });




});