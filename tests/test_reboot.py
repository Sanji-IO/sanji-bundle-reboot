#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import sys
import logging
import unittest

from mock import MagicMock

from sanji.connection.mockup import Mockup
from sanji.message import Message

try:
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
    from reboot import Reboot
except ImportError as e:
    print os.path.dirname(os.path.realpath(__file__)) + "/../"
    print sys.path
    print e
    print "Please check the python PATH for import test module. (%s)" \
        % __file__
    exit(1)

dirpath = os.path.dirname(os.path.realpath(__file__))


class TestRebootClass(unittest.TestCase):

    def setUp(self):
        self.bundle = Reboot(connection=Mockup())
        self.bundle.publish = MagicMock()

    def tearDown(self):
        self.bundle.stop()
        self.bundle = None

    def test__init(self):
        """
        init: do nothing
        """
        pass

    def test__reboot(self):
        """
        reboot: TODO
        """
        pass

    def test__put__no_data(self):
        """
        put (/system/reboot)
        """
        msg = {
            "id": 12345,
            "method": "put",
            "resource": "/system/reboot"
        }

        def resp(code=200, data=None):
            self.assertEqual(400, code)
            self.assertEqual(data, {"message": "Invalid Input."})
        message = Message(msg)
        self.bundle.put(message, response=resp, test=True)

    def test__put__empty_data(self):
        """
        put (/system/reboot): data attribute is empty
        """
        msg = {
            "id": 12345,
            "method": "put",
            "resource": "/system/reboot"
        }
        msg["data"] = dict()

        def resp(code=200, data=None):
            self.assertEqual(400, code)
            self.assertEqual(data, {"message": "Invalid Input."})
        message = Message(msg)
        self.bundle.put(message, response=resp, test=True)

    def test__put__disable(self):
        """
        put (/system/reboot): disable, do nothing
        """
        msg = {
            "id": 12345,
            "method": "put",
            "resource": "/system/reboot",
            "data": {
                "enable": 0
            }
        }

        def resp(code=200, data=None):
            self.assertEqual(200, code)
        message = Message(msg)
        self.bundle.put(message, response=resp, test=True)

    def test__put(self):
        """
        put (/system/reboot): reboot
        """
        msg = {
            "id": 12345,
            "method": "put",
            "resource": "/system/reboot",
            "data": {
                "enable": 1
            }
        }

        def resp(code=200, data=None):
            self.assertEqual(200, code)
        message = Message(msg)
        self.bundle.put(message, response=resp, test=True)

    def test_run(self):
        """
        run
        """
        # TODO: check run
        self.bundle.run()


if __name__ == "__main__":
    FORMAT = "%(asctime)s - %(levelname)s - %(lineno)s - %(message)s"
    logging.basicConfig(level=20, format=FORMAT)
    logger = logging.getLogger("Reboot Test")
    unittest.main()
