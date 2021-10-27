odoo.define('pos_autorizacion.PaymentScreen', function (require) {
    'use strict';

    var models = require('point_of_sale.models');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    var order_super = models.Order.prototype;

    models.load_fields('res.partner', ['credit_limit', 'total_overdue', 'total_due','credit']);
    models.load_fields('pos.order',['amount_in_words', 'pos_date_due','l10n_mx_edi_cfdi_amount_to_text','invoice_number'])

    models.Order = models.Order.extend({
        initialize: function(attr, options) {
            order_super.initialize.call(this,attr,options);
            this.autorizacion = this.autorizacion || null;
        },
        init_from_JSON: function(json) {
            order_super.init_from_JSON.apply(this, arguments);
            this.autorizacion = json.autorizacion || null;
        },
        export_as_JSON: function() {
            var json = order_super.export_as_JSON.apply(this);
            json.autorizacion = this.autorizacion;
            return json;
        }
    });

    const PosAutorizacionPaymentScreen = (PaymentScreen) => class extends PaymentScreen {
        async _isOrderValid(isForceValidate) {
            let valido = await super._isOrderValid(...arguments);
            if (valido) {
                let cliente = this.currentOrder.get_client();
                let property_payment_term_id = this.currentOrder.get_client().property_payment_term_id
                if ( cliente ) {
                    let es_bloqueado = false;
                    let motivo = '';
                    if (cliente.credit_limit && !this.currentOrder.is_paid_with_cash()) {
                        if (cliente.credit_limit - cliente.credit - (this.currentOrder.get_total_with_tax() - this.currentOrder.get_rounding_applied() )< 0){
                            es_bloqueado = true;
                            motivo += 'Excede límite de crédito. ' + "\n"
                        }
                    }
                    if(cliente.total_due > 0 && !this.currentOrder.is_paid_with_cash())
                    {
                        es_bloqueado = true;
                        motivo += 'El cliente tiene facturas vencidas por un saldo de '  + cliente.total_due + '.' + "\n"
                    }
                    let orderlines = this.currentOrder.orderlines.models
                    for (var i = 0; i < orderlines.length; i++){
                        orderlines[i].cambio_precio = false;
                        orderlines[i].precio_cambiado = 0;
                        if (orderlines[i].discount && !this.currentOrder.is_paid_with_cash()){
                            es_bloqueado = true;
                            motivo += 'Se ha ingresado un descuento manual de ' + orderlines[i].discount + '% para el producto ' + orderlines[i].product.display_name + '. '+ 'No se puede aplicar descuento manual.'
                        }
                        if(!orderlines[i].is_reward_line){
                            if (orderlines[i].discount_promotions == 0){
                                if (orderlines[i].hasOwnProperty("uom_id") && orderlines[i].new_price != 0) {
                                    var pricelist_price = orderlines[i].new_price.toFixed(6)
                                } else {
                                    var pricelist_price = orderlines[i].product.get_price(this.currentOrder.pricelist).toFixed(6);
                                }
                                var product_price = orderlines[i].price.toFixed(6);
                                if (!(product_price >= pricelist_price - 0.1 && product_price <= pricelist_price + 0.1)){
                                    es_bloqueado = true;
                                    orderlines[i].cambio_precio = true;
                                    orderlines[i].precio_cambiado = product_price;
                                    motivo += 'Precio lista ' + pricelist_price + ' del producto ' + orderlines[i].product.display_name + ' y el precio del producto en el pedido es ' + product_price + '.\n'
                                }
                            } else {
                                if (orderlines[i].hasOwnProperty("uom_id") && orderlines[i].new_price != 0) {
                                    if (orderlines[i].price_so != 0) {
                                        var price_so = orderlines[i].price_so
                                    } else {
                                        var price_so = orderlines[i].new_price.toFixed(6);
                                    }
                                } else {
                                    var price_so = parseFloat(orderlines[i].price_so).toFixed(6);
                                }
                                var product_price = orderlines[i].price.toFixed(6);
                                if (!(product_price >= price_so - 0.1 && product_price <= price_so + 0.1)){
                                    es_bloqueado = true;
                                    orderlines[i].cambio_precio = true;
                                    orderlines[i].precio_cambiado = product_price;
                                    motivo += 'Precio lista ' + price_so + ' del producto ' + orderlines[i].product.display_name + ' y el precio del producto en el pedido es ' + product_price + '.\n'
                                }
                            }
                        }
                    }
                    if (es_bloqueado) {
                        let self = this
                        if (this.currentOrder.autorizacion){
                            let autorizacion = this.currentOrder.autorizacion
                            const result = await this.rpc({
                                model: 'pos.autorizacion',
                                method: 'revisar_estado',
                                args: [autorizacion],
                            })
                            if (result == 'pendiente'){
                                self.showPopup('ErrorPopup', {
                                    title: 'Venta bloqueada',
                                    body: 'Esta venta requiere de autorización.',
                                });
                                return false;
                            } else if (result == 'aprobado'){
                                self.currentOrder.autorizacion = null;
                                let detalles = []
                                let unitario_pdf
                                let descuento_pdf
                                for (var i = 0; i < orderlines.length; i++) {
                                    if (orderlines[i].cambio_precio) {
                                        unitario_pdf = orderlines[i].precio_cambiado;
                                        descuento_pdf = 0;
                                    } else {
                                        if (orderlines[i].price_unit_pdf == 0) {
                                            unitario_pdf = orderlines[i].price
                                        } else {
                                            unitario_pdf = orderlines[i].price_unit_pdf
                                        }
                                        if (orderlines[i].descuento_pdf == 0) {
                                            descuento_pdf = orderlines[i].discount
                                        } else {
                                            descuento_pdf = orderlines[i].descuento_pdf
                                        }
                                    }

                                    detalles.push([{
                                        'product_id': orderlines[i].product.id,
                                        'cantidad': orderlines[i].quantity,
                                        'unitario': orderlines[i].price,
                                        'descuento': orderlines[i].discount,
                                        'unitario_pdf': unitario_pdf,
                                        'descuento_pdf': descuento_pdf,
                                    }]);
                                }
                                const comprobar = await this.rpc({
                                    model: 'pos.autorizacion',
                                    method: 'comprobar',
                                    args: [[autorizacion], {
                                        'partner_id': cliente.id,
                                        'pricelist_id': self.currentOrder.pricelist.id,
                                        'detalles': detalles,
                                    }],
                                })
                                if (comprobar){
                                    return true;
                                } else {
                                    self.showPopup('ErrorPopup', {
                                        title: 'Venta modificada',
                                        body: 'La autorización aprobada y la presente venta presentan diferencias.',
                                    });
                                    return false;
                                }
                            } else if (result == 'rechazado'){
                                self.showPopup('ErrorPopup', {
                                    title: 'Venta bloqueada',
                                    body: 'La autorización ha sido rechazada.',
                                });
                                self.currentOrder.autorizacion = null;
                                return false;
                            }
                        } else {
                            this.showPopup('ErrorPopup', {
                                title: 'Venta bloqueada',
                                body: 'Esta venta requiere de autorización.',
                            });
                            let detalles = []
                            let unitario_pdf
                            let descuento_pdf
                            for (var i = 0; i < orderlines.length; i++) {
                                let impuestos = []
                                for (var j = 0; j < orderlines[i].product.taxes_id.length; j++){
                                    impuestos.push([4, orderlines[i].product.taxes_id[j]])
                                }

                                if (orderlines[i].cambio_precio) {
                                    unitario_pdf = orderlines[i].precio_cambiado;
                                    descuento_pdf = 0;
                                } else {
                                    if (orderlines[i].price_unit_pdf == 0) {
                                        unitario_pdf = orderlines[i].price
                                    } else {
                                        unitario_pdf = orderlines[i].price_unit_pdf
                                    }
                                    if (orderlines[i].descuento_pdf == 0) {
                                        descuento_pdf = orderlines[i].discount
                                    } else {
                                        descuento_pdf = orderlines[i].descuento_pdf
                                    }
                                }

                                detalles.push([0, 0, {
                                    'product_id': orderlines[i].product.id,
                                    'cantidad': orderlines[i].quantity,
                                    'unitario': orderlines[i].price,
                                    'descuento': orderlines[i].discount,
                                    'impuesto': impuestos,
                                    'unitario_pdf': unitario_pdf,
                                    'descuento_pdf': descuento_pdf,
                                }]);
                            }
                            this.rpc({
                                model: 'pos.autorizacion',
                                method: 'create',
                                args: [{
                                    'name': this.currentOrder.name,
                                    'partner_id': cliente.id,
                                    'user_id': this.currentOrder.employee.user_id[0],
                                    'pricelist_id': this.currentOrder.pricelist.id,
                                    'detalle_ids': detalles,
                                    'motivo': motivo,
                                    'ruta': this.env.pos.config.name,
                                }],
                            }).then(function (result) {
                                self.currentOrder.autorizacion = result;
                                self.env.pos.db.save_unpaid_order(self.currentOrder);
                            });
                        }
                        alert (motivo)
                        return false;
                    }
                }
                 let self =this
                 const order = this.env.pos.get_order();
                 const amount_in_words= await this.rpc({ model: 'pos.order',
                            method: 'l10n_mx_edi_cfdi_amount_to_text_order',
                             args: [[this.currentOrder],{
                                          'amount_total':this.currentOrder.get_total_with_tax(),
                                          'pricelist_id': this.currentOrder.pricelist.id,
                                          'currency_id':this.currentOrder.pricelist.currency_id,
                                           }
                                    ],
                                })
                                .then(function(res) {

                                     order.amount_in_words=res
                                     return res
                                })
                                .catch(error => {
                                 console.error(error);
                                 });

                 const pos_date_due=await this.rpc({
                      model:'pos.order',
                      method:'calculate_pos_date_due',
                      args:[{
                      'partner_id':cliente.id,
                      'creation_date':this.currentOrder.creation_date,
                      }],
                      }).then(function(date_due) {

                                     order.pos_date_due=date_due
                                     return date_due
                                }).catch(error => {
                       console.error(error);
                        })

            }
            return valido
        }
        //Sobreescribi el metodo para obtener el nro de factura en este proceso antes de mandar a imprimir
          async _finalizeValidation() {
            if ((this.currentOrder.is_paid_with_cash() || this.currentOrder.get_change()) && this.env.pos.config.iface_cashdrawer) {
                this.env.pos.proxy.printer.open_cashbox();
            }

            this.currentOrder.initialize_validation_date();
            this.currentOrder.finalized = true;

            let syncedOrderBackendIds = [];
            try {
                if (this.currentOrder.is_to_invoice()) {
                    syncedOrderBackendIds = await this.env.pos.push_and_invoice_order(
                        this.currentOrder
                    );
                var order = this.env.pos.get_order();
                 var self = this;
               var domain = [['pos_reference', '=', order.name]];
               const invoice_number= await this.rpc({
                    model: 'pos.order',
                    method: 'get_account_move',
                    args: [domain,{'name': order.name,'account_move':order.account_move,
                                    }],
                }).then(function (result) {
                                      order.invoice_number=result;
                                      //receipt.invoice_number=order.invoice_number;
                                      console.log(result)


                                     return result
                                }).catch(error => {
                console.error(error);
             });

                } else {
                    syncedOrderBackendIds = await this.env.pos.push_single_order(this.currentOrder);
                }
            } catch (error) {
                if (error instanceof Error) {
                    throw error;
                } else {
                    await this._handlePushOrderError(error);
                }
            }
            if (syncedOrderBackendIds.length && this.currentOrder.wait_for_push_order()) {
                const result = await this._postPushOrderResolve(
                    this.currentOrder,
                    syncedOrderBackendIds
                );
                if (!result) {
                    await this.showPopup('ErrorPopup', {
                        title: 'Error: no internet connection.',
                        body: error,
                    });
                }
            }

            this.showScreen(this.nextScreen);

            // If we succeeded in syncing the current order, and
            // there are still other orders that are left unsynced,
            // we ask the user if he is willing to wait and sync them.
            if (syncedOrderBackendIds.length && this.env.pos.db.get_orders().length) {
                const { confirmed } = await this.showPopup('ConfirmPopup', {
                    title: this.env._t('Remaining unsynced orders'),
                    body: this.env._t(
                        'There are unsynced orders. Do you want to sync these orders?'
                    ),
                });
                if (confirmed) {
                    // NOTE: Not yet sure if this should be awaited or not.
                    // If awaited, some operations like changing screen
                    // might not work.
                    this.env.pos.push_orders();
                }
            }
        }
    };

    Registries.Component.extend(PaymentScreen, PosAutorizacionPaymentScreen);
    return PaymentScreen;

});