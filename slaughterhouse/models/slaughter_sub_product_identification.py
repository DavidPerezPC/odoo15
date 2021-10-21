# -*- coding: utf-8 -*-

'''
    /*************************************************************************
    * Description
      Permitir al usuario clave registrar la identificación de los diferentes sub-productos existentes.
    * VERSION
      1.1
    * Author:
      Erick Enrique Abrego Gonzalez
    * Date:
      17/09/2021
    *************************************************************************/
'''

from odoo import models, fields, api
from odoo.exceptions import ValidationError



class SlaughterSubProductIndentification(models.Model):
    _name = "slaughter.sub.product.identification"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Sub Product Identification"

    name = fields.Char(related="product_id.name", string="Description", store=True, tracking=True)
    primary_code = fields.Char(related="product_id.default_code", string="Primary Code", store=True, tracking=True)
    secondary_code = fields.Char(string="Secondary code", store=True, tracking=True, help="Secondary code of the sub-product")
    pz_per_animal_qty = fields.Integer(string="Pieces per animal", store=True, tracking=True, help="Quantity of pieces per animal")
    sequence_line = fields.Integer(string="Sequence Line")
    container_weight = fields.Float(string="Container Weight", store=True, tracking=True, help="Approximate weight of the container")
    qty_or_percentage = fields.Float(string="Quantity or Percentage", store=True, tracking=True, help="Indicates the qty or the percentage depends on the type of waste")
    weight_per_pz = fields.Float(string="Weight per piece", store=True, tracking=True, help="Average weight per piece")
    product_id = fields.Many2one(comodel_name="product.product", string="Product", store=True, tracking=True, help="Primary product")
    product_uom_id = fields.Many2one(related="product_id.uom_id", string="Unit of Measure", store=True, tracking=True, help="Unit of measure of the sub-product")
    specie_id = fields.Many2one(comodel_name="specie.catalog", string="Species name", store=True, tracking=True, help="Species that exist in the BD")
    sub_product_type_id = fields.Many2one(comodel_name="slaughter.sub.product.type", string="Sub Product Type",
                                          store=True, tracking=True, help="Type of sub product")
    apportion_based_on = fields.Selection(string="Apportion based on", selection=[('piece_weight','Piece weight'),
                                                                                        ('slaughter_count','Slaughter count'),
                                                                                        ('total_channel_weight','Total channel weight'),
                                                                                        ('total_standing_weight','Total standing weight')], tracking=True, help="Apportion based on")
    classification = fields.Selection(string="Classification", selection=[('raw_material', 'Raw Material'),
                                                                          ('finished_product', 'Finished Product')], tracking=True)
    is_lot_control = fields.Selection(string="Lot control", default="no", selection=[('yes','Yes'),('no','No')], tracking=True, help="Is the entry batch controlled by lot.")
    is_pz_per_animal = fields.Boolean(string="Identify piece per animal", default=False, tracking=True, help="Is the entry identify per animal.")
    has_natural_wastes = fields.Boolean(string="Has natural wastes", default=False, tracking=True, help="Has natural wastes?.")
    record_control = fields.Selection(string="Record Control", default="by_introducer", selection=[('by_introducer', 'By Introducer'),
                                                                                                   ('by_slaughter_date', 'By Slaughter Date')], tracking=True)
    waste_type = fields.Selection(string="Waste type", selection=[('percent', 'Percent'), ('qty', 'Quantity')], tracking=True, help="Type pf waste.")
    active = fields.Boolean(string="Active", default=True, tracking=True)

    @api.constrains('is_lot_control')
    def _check_is_lot_control(self):
        for rec in self:
            if rec.record_control != 'by_introducer' and rec.is_lot_control == 'yes':
                raise ValidationError('The control by lot only can be yes if the record control is by introducer.')
