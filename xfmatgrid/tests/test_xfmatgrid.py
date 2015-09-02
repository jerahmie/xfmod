#!/usr/bin/env python
"""
Test xfmatgrid module.
"""

from __future__ import(absolute_import, division,
                       print_function, unicode_literals)

import unittest


class TestXFMatGrid(unittest.TestCase):
    """Tests for xfmatgrid module."""
    #def setUp(self):
    #
    
    def test_add(self):
        a=3
        b=5
        result=a+b
        self.assertEqual(8,result)

    #def tearDown(self):
    #
    
if __name__ == '__main__':
    unittest.main()
