'''
Created on 09.11.2016

@author: Moustafa Shama
'''
import unittest


class TestDataSource(unittest.TestCase):


    def test_get_BBG_PriceData(self):
        from .datasource import get_BBG_PriceData
        from datetime import datetime

        instrument = 'VG1 Index'
        fields = ['PX_LAST']
        lastPriceDate = datetime.strptime('20161101','%Y%m%d')
        price_data = get_BBG_PriceData(instrument, fields, lastPriceDate)
        print(price_data)


if __name__ == "__main__":
    import sys;sys.argv = ['', 'TestDataSource.test_get_BBG_PriceData']
    unittest.main()