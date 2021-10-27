odoo.define('pos_impresion_ticket.PrintBillButtonLey', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class PrintBillButtonLey extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        async onClick() {
            const order = this.env.pos.get_order();
            if (!order.get_client()) {
                  this.showPopup('ErrorPopup', {
                    title: 'Seleccionar cliente',
                    body: 'Por favor seleccionar cliente antes de calcular promociones.',
                  });
                }
                else{
                 if (order.get_orderlines().length > 0) {
                const amount_in_words= await this.rpc({ model: 'pos.order',
                            method: 'l10n_mx_edi_cfdi_amount_to_text_order',
                             args: [[this.currentOrder],{
                                          'amount_total':order.get_total_with_tax(),
                                          'pricelist_id': order.pricelist.id,
                                          'currency_id':order.pricelist.currency_id,
                                           }
                                    ],
                                })
                                .then(function(res) {

                                     order.amount_in_words=res
                                     order.price_discount=order.pricelist.items[0].price_discount
                                     console.log(order.pricelist.items[0].price_discount)
                                     return res
                                })
                                .catch(error => {
                                console.error(error);
                              });
               // await this.showTempScreen('ImprimirTicketScreen');
                //Agregando variables para calcular promociones
                var discountpromo = 0;
                var promo_linea = 0;
                var discount_tarifa_promo =0;
                var total_discount_tarifa=0;
                let list_price;
                self = this

                    const datat = order.orderlines.models.filter(e => (e.is_reward_line == false)).map((value) => {
                        let uom_id
                        if (value.hasOwnProperty("uom_id")){
                            uom_id = value.uom_id
                        } else {
                            uom_id = value.product.uom_id[0]
                        }
                        return {
                            id: value.product.id,
                            quantity: value.quantity,
                            discount: value.discount,
                            uom_id: uom_id,
                            new_price: value.new_price,
                        };
                    })
                    const result = await  this.rpc({
                        model: 'sale.order',
                        method: 'calcular_promociones',
                        args: [[], order.attributes.client.id, order.pricelist.id, datat],
                    });
                    if (result){
                        for (const line of [...order.get_orderlines()]) {
                            await order.remove_orderline(line);
                        }
                        for (const line of result) {
                            await self.trigger('click-product', self.env.pos.db.get_product_by_id(line.product_id));
                        }
                        order.get_orderlines().forEach((line, index) => {
                            line.is_reward_line = result[index].is_reward_line;
                            line.price_manually_set = true;
                            line.set_unit_price(result[index].price_unit_pdf * (1 - (result[index].descuento_pdf / 100)));
                            line.set_quantity(result[index].cantidad);
                            line.set_unit(result[index].uom_id);
                            line.discount_promotions = result[index].discount_promotions;
                            line.price_unit_pdf = result[index].price_unit_pdf;
                            line.descuento_pdf = result[index].descuento_pdf;
                            line.price_so = (result[index].price_unit_pdf * (1 - (result[index].descuento_pdf / 100))).toFixed(6)
                            line.new_price = result[index].new_price

                            if(!line.is_reward_line){
                                list_price=line.price_unit_pdf;
                                discount_tarifa_promo= (line.quantity *list_price) * (line.descuento_pdf/100.0)
                                total_discount_tarifa + = discount_tarifa_promo;
                            }
                            promo_linea=line.quantity*(list_price*(line.discount_promotions/100))
                            discountpromo +=  promo_linea;
                        })
                        total_discount_tarifa= total_discount_tarifa - discountpromo;
                        order.total_discount_tarifa=total_discount_tarifa;
                        order.discountpromo=discountpromo;
                    }
                    await this.showTempScreen('ImprimirTicketScreen');
            } else {
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Nada para imprimir'),
                    body: this.env._t('No existen líneas de producto en esta orden de venta.'),
                });
            }
                }

        }
    }
    PrintBillButtonLey.template = 'PrintBillButtonLey';

    ProductScreen.addControlButton({
        component: PrintBillButtonLey,
        condition: function() {
            return this.env.pos.config.imprimir_ticket;
        },
    });

    Registries.Component.add(PrintBillButtonLey);

    return PrintBillButtonLey;
});
