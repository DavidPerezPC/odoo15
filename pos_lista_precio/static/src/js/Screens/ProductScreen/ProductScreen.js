odoo.define('pos_lista_precio.ProductScreen', function (require) {
    "use strict";

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');

    const PosListaPrecioProductScreen = (ProductScreen) => class extends ProductScreen {
        async _clickProduct(event) {
        console.log(this.currentOrder.get_client())

          if (!this.currentOrder.get_client()) {
                  this.showPopup('ErrorPopup', {
                    title: 'Seleccionar cliente',
                    body: 'Por favor debe seleccionar cliente.',
                  });
                }
          else {let valido = await super._clickProduct(...arguments);}

        }
        _onClickPay() {
            let cliente = this.currentOrder.get_client();
            if (cliente) {
                const order = this.env.pos.get_order();
                for (const line of order.get_orderlines()) {
                    if (line.price_unit_pdf == 0.0){
                        line.price_unit_pdf = (line.get_fixed_lst_price() * line.pos.units_by_id[line.product.uom_id[0]].factor)/line.get_unit().factor
                        line.descuento_pdf = 100 - (line.price * 100 / line.price_unit_pdf)
                    }
                     if(line.uom_after_promotion)
                        {
                        order.onchange_promotions=2;
                         this.showPopup('ErrorPopup', {
                        title: 'Aplicar promocion',
                        body: 'Por favor recuerde aplicar promocion a producto con nueva unidad de medida.',
                           })
                        }
                }
                if (order.onchange_promotions!=2)
                  {
                   super._onClickPay(...arguments);
                 }
            } else {
                this.showPopup('ErrorPopup', {
                    title: 'Seleccionar cliente',
                    body: 'Por favor seleccionar cliente antes de pasar a la ventana de pago.',
                });
            }
        }
    };

    Registries.Component.extend(ProductScreen, PosListaPrecioProductScreen);
    return ProductScreen;

});