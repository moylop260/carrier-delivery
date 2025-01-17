# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Sébastien BEAU <sebastien.beau@akretion.com>
#    Copyright (C) 2012-TODAY Akretion <http://www.akretion.com>.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import orm, fields


class DeliveryCarrierTemplateOption(orm.Model):
    """ Available options for a carrier (partner) """
    _name = 'delivery.carrier.template.option'
    _description = 'Delivery carrier template option'

    _columns = {
        'partner_id': fields.many2one(
            'res.partner',
            'Partner Carrier'),
        'name': fields.char(
            'Name',
            readonly=True,
            size=64),
        'code': fields.char(
            'Code',
            readonly=True,
            size=64),
        'description': fields.char(
            'Description',
            readonly=True,
            help="Allow to define a more complete description "
                 "than in the name field."),
    }


class DeliveryCarrierOption(orm.Model):
    """ Option selected for a carrier method

    Those options define the list of available pre-added and available
    to be added on delivery orders

    """
    _name = 'delivery.carrier.option'
    _description = 'Delivery carrier option'
    _inherits = {'delivery.carrier.template.option': 'tmpl_option_id'}

    _columns = {
        'mandatory': fields.boolean(
            'Mandatory',
            help="If checked, this option is necessarily applied "
                 "to the delivery order"),
        'by_default': fields.boolean(
            'Applied by Default',
            help="By check, user can choose to apply this option "
            "to each Delivery Order\n using this delivery method"),
        'tmpl_option_id': fields.many2one(
            'delivery.carrier.template.option',
            string='Option', required=True, ondelete="cascade"),
        'carrier_id': fields.many2one('delivery.carrier', 'Carrier'),
        'readonly_flag': fields.boolean(
            'Readonly Flag',
            help="When True, help to prevent the user to modify some fields "
                 "option (if attribute is defined in the view)"),
    }

    _defaults = {
        'readonly_flag': False,
        'by_default': False,
    }


class DeliveryCarrier(orm.Model):
    _inherit = 'delivery.carrier'

    def _get_carrier_type_selection(self, cr, uid, context=None):
        """ To inherit to add carrier type """
        return []

    def __get_carrier_type_selection(self, cr, uid, context=None):
        """ Wrapper to preserve inheritance for selection field """
        return self._get_carrier_type_selection(cr, uid, context=context)

    _columns = {
        'type': fields.selection(
            __get_carrier_type_selection, 'Type',
            help="Carrier type (combines several delivery methods)"),
        'code': fields.char(
            'Code', size=10,
            help="Delivery Method Code (according to carrier)"),
        'description': fields.text('Description'),
        'available_option_ids': fields.one2many(
            'delivery.carrier.option',
            'carrier_id', 'Option'),
    }
