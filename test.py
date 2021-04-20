from ds_user.test.user_test import UserTester
from ds_product.test.category_test import CategoryTester
from ds_product.test.product_test import ProductTester
import coloredlogs
import unittest
import logging
import sys
import cowsay

cowsay.dragon(
    "Yei, we managed to run the application for testers, cool bro \n Author : Kenedi Novriansyah")


coloredlogs.install()

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    unittest.main()
