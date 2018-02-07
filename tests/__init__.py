# This file is part sale_data module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.sale_data.tests.test_sale_data import suite
except ImportError:
    from .test_sale_data import suite

__all__ = ['suite']
