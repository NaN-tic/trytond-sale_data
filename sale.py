#This file is part sale_data module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

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
    def get_sale_data(self, party, description=None):
        '''
        Return sale values from party
        :param party: the BrowseRecord of the party
        :return: a dict values
        '''
        pool = Pool()
        Sale = pool.get('sale.sale')
        PaymentTerm = pool.get('account.invoice.payment_term')

        company_context = Transaction().context.get('company')
        company = Pool().get('company.company')(company_context)

        values = {'party': party}
        vals = Sale(**values).on_change_party()

        vals['party'] = party

        if description:
            vals['description'] = description

        if not 'payment_term' in vals:
            payment_terms = PaymentTerm.search([], limit=1)
            if not payment_terms:
                self.raise_user_error('missing_payment_term',
                    error_args=(party.name, party))
            payment_term, = payment_terms
            vals['payment_term'] = party.customer_payment_term or payment_term

        if not 'company' in vals:
            vals['company'] = company

        if not 'currency' in vals:
            vals['currency'] = company.currency

        return vals


class SaleLine:
    __name__ = 'sale.line'

    @classmethod
    def __setup__(cls):
        super(SaleLine, cls).__setup__()
        cls._error_messages.update({
            'missing_product_uom': 'Not available Product Uom "%s"',
            })

    @classmethod
    def get_sale_line_data(self, sale, product, quantity, uom='u', note=None):
        '''
        Return sale line values
        :param sale: the BrowseRecord of the invoice
        :param product: the BrowseRecord of the product
        :param quantity: the float of the quantity
        :param uom: str of the unit of mesure
        :param note: the str of the note line
        :return: a dict values
        '''
        SaleLine = Pool().get('sale.line')
        ProductUom = Pool().get('product.uom')

        uoms = ProductUom.search(['symbol', '=', uom], limit=1)
        if not uoms:
            self.raise_user_error('missing_product_uom', error_args=(uom))
        uom = uoms[0]

        line = SaleLine()
        line.unit = uom
        line.quantity = quantity
        line.product = product
        line.sale = sale
        line.description = None
        line.party = sale.party
        vals = line.on_change_product()

        vals['sale'] = sale
        vals['type'] = 'line'
        vals['quantity'] = quantity
        vals['unit'] = uom
        vals['product'] = product
        vals['description'] = product.name
        vals['product_uom_category'] = product.category or None
        vals['taxes'] = [('add', vals.get('taxes'))]
        vals['note'] = note
        vals['sequence'] = 1
        return vals

    @classmethod
    def get_sale_line_product(self, party, product, quantity=1, desc=None):
        """
        Get Product values
        :param party: the BrowseRecord of the party
        :param product: the BrowseRecord of the product
        :param quantity: Int quantity
        :param desc: Str line
        :return: dict product values
        """
        pool = Pool()
        Sale = pool.get('sale.sale')
        SaleLine = pool.get('sale.line')

        sale = Sale()
        sale.party = party
        sale.currency = sale.default_currency()

        line = SaleLine()
        line.quantity = quantity
        line.sale = sale
        line.product = product
        line.description = desc or product.name
        line.unit = product.default_uom
        vals = line.on_change_product()

        vals['type'] = 'line'
        vals['quantity'] = quantity
        vals['unit'] = uom
        vals['product'] = product
        vals['description'] = desc or product.name
        vals['product_uom_category'] = product.category or None
        vals['taxes'] = [('add', vals.get('taxes'))]
        vals['sequence'] = 1
        return vals
