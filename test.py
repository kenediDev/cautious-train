from ds_user.test.user_test import UserTester
import coloredlogs
import unittest
import logging
import sys
import cowsay

cowsay.dragon(
    "Yei, we managed to run the application for testers, cool bro")


coloredlogs.install()

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    unittest.main()
