#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
import sys
import logging
import unittest

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
        self.reboot = Reboot(connection=Mockup())

    def tearDown(self):
        self.reboot.stop()
        self.reboot = None

    def test_init(self):
        pass

    def test_put(self):
        test_msg = {
            "id": 12345,
            "method": "put",
            "resource": "/system/reboot"
        }

        # case 1: no data attribute
        def resp1(code=200, data=None):
            self.assertEqual(400, code)
            self.assertEqual(data, {"message": "Invalid Input."})
        message = Message(test_msg)
        self.reboot.put(message, response=resp1, test=True)

        # case 2: data dict is empty or no enable exist
        def resp2(code=200, data=None):
            self.assertEqual(400, code)
            self.assertEqual(data, {"message": "Invalid Input."})
        test_msg["data"] = dict()
        message = Message(test_msg)
        self.reboot.put(message, response=resp2, test=True)

        # case 3: disable (do nothing)
        def resp3(code=200, data=None):
            self.assertEqual(200, code)
        test_msg["data"]["enable"] = 0
        message = Message(test_msg)
        self.reboot.put(message, response=resp3, test=True)

        # case 4: enable
        def resp4(code=200, data=None):
            self.assertEqual(200, code)
        test_msg["data"]["enable"] = 1
        message = Message(test_msg)
        self.reboot.put(message, response=resp4, test=True)

    def test_reboot(self):
        # TODO
        pass

if __name__ == "__main__":
    FORMAT = "%(asctime)s - %(levelname)s - %(lineno)s - %(message)s"
    logging.basicConfig(level=20, format=FORMAT)
    logger = logging.getLogger("Reboot Test")
    unittest.main()
