odoo.define('custom_mrp_replenish.Replenish', function (require){
'use strict';

var core = require('web.core');
var QWeb = core.qweb;
var _t = core._t;
var clientAction = require('mrp_mps.ClientAction');

clientAction.include({

    //Agregamos un evento para el botón de reabastecer por separado extendiendo la funcionalidad.
    events: _.extend({
        'click .o_mrp_mps_procurement1': '_onClickReplenish1',
        'mouseover .o_mrp_mps_procurement1': '_onMouseOverReplenish',
        'mouseout .o_mrp_mps_procurement1': '_onMouseOutReplenish',
    }, clientAction.prototype.events),

    //Sobreescribimos el metodo para agregar la funcionalidad al momento de hacer click en el nuevo botón.
    update_cp: function () {
        var self = this;
        this.$buttons = $(QWeb.render('mrp_mps_control_panel_buttons'));
        this._update_cp_buttons();
        var $replenishButton = this.$buttons.find('.o_mrp_mps_replenish');
        $replenishButton.on('click', self._onClickReplenish.bind(self));
        $replenishButton.on('mouseover', self._onMouseOverReplenish.bind(self));
        $replenishButton.on('mouseout', self._onMouseOutReplenish.bind(self));
        //Se busca el boton en nuestro qweb_template y es asignado a una variable para saber su estado.
        var $replenishButton1 = this.$buttons.find('.o_mrp_mps_replenish1');
        $replenishButton1.on('click', self._onClickReplenish1.bind(self));
        $replenishButton1.on('mouseover', self._onMouseOverReplenish.bind(self));
        $replenishButton1.on('mouseout', self._onMouseOutReplenish.bind(self));

        this.$buttons.find('.o_mrp_mps_create').on('click', self._onClickCreate.bind(self));
        this.$searchview_buttons = $(QWeb.render('mrp_mps_control_panel_option_buttons', {groups: self.groups}));
        this.$searchview_buttons.find('.o_mps_mps_show_line').on('click', self._onChangeCompany.bind(self));
        return this.updateControlPanel({
            title: _t('Master Production Schedule'),
            cp_content: {
                $buttons: this.$buttons,
                $searchview_buttons: this.$searchview_buttons,
            },
        });
    },

    //Función que nos permite llamar a nuestro metodo en python (action_replenish1).
    _actionReplenish1: function (productionScheduleId) {
        var self = this;
        var ids;
        var basedOnLeadTime;
        if (productionScheduleId.length) {
            ids = productionScheduleId;
            basedOnLeadTime = false;
        }
        else {
            ids = self.active_ids;
            basedOnLeadTime = true;
        }
        this.mutex.exec(function () {
            return self._rpc({
                model: 'mrp.production.schedule',
                method: 'action_replenish1',
                args: [ids, basedOnLeadTime]
            }).then(function (){
                return self._reloadContent();
            });
        });
    },

    //Se hereda la función para mostrar o no el nuevo boton dependiendo si hay o no cantidad a reabastecer.
    _update_cp_buttons: function () {   
        var toReplenish = _.filter(_.flatten(_.values(this.state)), function (mps) {
            if (_.where(mps.forecast_ids, {'to_replenish': true}).length) {
                return true;
            } else {
                return false;
            }
        });
        var $replenishButton1 = this.$buttons.find('.o_mrp_mps_replenish1');
        if (toReplenish.length) {
            $replenishButton1.removeClass('o_hidden');
        } else {
            $replenishButton1.addClass('o_hidden');
        }
        console.log(this._super(...arguments))
        return this._super(...arguments);
    },

    //Acción al momento de hacer click en el nuevo boton.
    _onClickReplenish1: function (ev) {
        ev.stopPropagation();
        var productionScheduleId = [];
        var $tbody = $(ev.target).closest('.o_mps_content');
        if ($tbody.length) {
            productionScheduleId = [$tbody.data('id')];
        }
        this._actionReplenish1(productionScheduleId);
    },
})

});