===================================================
Ventas. Obtener valores para generar nuevos pedidos
===================================================

A partir del tercero y un producto, nos permite calcular datos para
la generación de nuevos pedidos y sus linias.

Venta
=====

    sale = Sale.get_sale_data(party, description=None)
    sale.save()

Línea de venta
==============

    sale_lines = SaleLine.get_invoice_line_data(sale, product, quantity, uom='u', note=None)
    sale_lines.save()

Además, si la venta todavía no está creada, este método permite calcular los
datos de línea de venta a partir de un tercero y un producto:

    sale_lines = SaleLine.get_sale_line_product(party, product, qty=1, desc=None)
    sale_lines.save()
