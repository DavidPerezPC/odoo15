odoo.define('pos_cliente_almacen.ClientListScreen', function (require) {
    "use strict";

    const ClientListScreen = require('point_of_sale.ClientListScreen');
    const Registries = require('point_of_sale.Registries');
    var models = require('point_of_sale.models');
    var utils = require('web.utils');

    models.load_fields('res.partner', ['property_warehouse_id','pos_order_count','total_invoiced','customer_rank','city','parent_id']);

    const PosClienteAlmacenClientListScreen = (ClientListScreen) => class extends ClientListScreen {
        get clients() {
            let check_all_client_picking_type = this.env.pos.config.check_all_client_picking_type
            if (this.state.query && this.state.query.trim() !== '') {
                if(check_all_client_picking_type) {
                    let clientes = this.env.pos.db.search_partner(this.state.query.trim()).filter(e => (e.customer_rank>0));
                    return clientes;
                }
                else {
                    let warehouse_id = this.env.pos.config.property_warehouse_id[0]
                    let clientes_filtrados = this.env.pos.db.get_partners_sorted().filter(e => (e.property_warehouse_id[0] == warehouse_id && e.customer_rank>0));
                    let patron = this.state.query.trim();
                    let clientes = [];
                    for(var i = 0; i < clientes_filtrados.length; i++){
                        if(clientes_filtrados[i].name.toUpperCase().includes(patron.toUpperCase()) || (clientes_filtrados[i].parent_id && clientes_filtrados[i].parent_id[1].toUpperCase().includes(patron.toUpperCase()))){
                            clientes.push(clientes_filtrados[i]);
                        }
                    }
                    return clientes;
                }
            } else {
                if(check_all_client_picking_type) {
                    let clientes = this.env.pos.db.get_partners_sorted().filter(e => (e.customer_rank>0));
                    return clientes;
                }
                else {
                    let warehouse_id = this.env.pos.config.property_warehouse_id[0]
                    let clientes = this.env.pos.db.get_partners_sorted().filter(e => (e.property_warehouse_id[0] == warehouse_id && e.customer_rank>0));
                    return clientes;
                }
            }
        }
        get nextButton() {
            if (!this.props.client) {
                return { command: 'set', text: 'Seleccionar Cliente' };
            } else if (this.props.client && this.props.client === this.state.selectedClient) {
                return { command: 'deselect', text: 'Deseleccionar Cliente' };
            } else {
                return { command: 'set', text: 'Cambiar Cliente' };
            }
        }
    };

    Registries.Component.extend(ClientListScreen, PosClienteAlmacenClientListScreen);
    return ClientListScreen;

});