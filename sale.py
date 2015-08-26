# This file is part sale_data module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta

__all__ = ['Sale', 'SaleLine']
__metaclass__ = PoolMeta


class Sale:
    __name__ = 'sale.sale'

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
        cls._error_messages.update({
            'missing_payment_term': 'Party "%s" (%s) must be a Payment term!',
            })

    @classmethod
    def get_sale_data(cls, party, description=None):
        '''
        Return sale object from party
        :param party: the BrowseRecord of the party
        :return: object
        '''
        pool = Pool()
        PaymentTerm = pool.get('account.invoice.payment_term')

        sale = cls()
        default_values = cls.default_get(cls._fields.keys())
        for key in default_values:
            if 'rec_name' not in key:
                setattr(sale, key, default_values[key])
        sale.party = party
        sale.on_change_party()

        if description:
            sale.description = description

        if not sale.payment_term:
            payment_terms = PaymentTerm.search([], limit=1)
            if not payment_terms:
                cls.raise_user_error('missing_payment_term',
                    error_args=(party.rec_name, party.id))
            payment_term, = payment_terms
            sale.payment_term = party.customer_payment_term or payment_term
        return sale


class SaleLine:
    __name__ = 'sale.line'

    @classmethod
    def __setup__(cls):
        super(SaleLine, cls).__setup__()
        cls._error_messages.update({
            'missing_product_uom': 'Not available Product Uom "%s"',
            })

    @classmethod
    def get_sale_line_data(cls, sale, product, quantity, note=None):
        '''
        Return sale line object from sale and product
        :param sale: the BrowseRecord of the invoice
        :param product: the BrowseRecord of the product
        :param quantity: the float of the quantity
        :param note: the str of the note line
        :return: object
        '''
        Line = Pool().get('sale.line')

        line = Line()
        line.sale = sale
        line.quantity = quantity
        line.product = product
        line.party = sale.party
        line.type = 'line'
        line.sequence = 1
        line.on_change_product()
        if note:
            line.note = note
        return line

    @classmethod
    def get_sale_line_product(cls, party, product, quantity=1, desc=None):
        """
        Get Product object from party and product
        :param party: the BrowseRecord of the party
        :param product: the BrowseRecord of the product
        :param quantity: Int quantity
        :param desc: Str line
        :return: object
        """
        pool = Pool()
        Sale = pool.get('sale.sale')
        Line = pool.get('sale.line')

        sale = Sale()
        sale.party = party
        sale.currency = sale.default_currency()

        line = Line()
        line.quantity = quantity
        line.sale = sale
        line.product = product
        line.unit = product.default_uom
        line.type = 'line'
        line.sequence = 1
        line.on_change_product()
        if desc:
            line.description = desc
        return line
