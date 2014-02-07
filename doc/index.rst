Sale Data Module
################

The sale_data module get sale.sale data from a party 
and sale.line data from a product to create a new sales. 
It's design to use two methods from others modules.

Sale
====

    vals = Sale.get_sale_data(party, description)

Sale Line
=========

    line_vals = SaleLine.get_sale_line_data(sale, product, quantity, uom='h', note)
