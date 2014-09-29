#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
from time import sleep

from sanji.core import Sanji
from sanji.connection.mqtt import Mqtt


REQ_RESOURCE = "/system/reboot"


class View(Sanji):

    # This function will be executed after registered.
    def run(self):

        for count in xrange(0, 100, 1):
            # Normal CRUD Operation
            #   self.publish.[get, put, delete, post](...)
            # One-to-One Messaging
            #   self.publish.direct.[get, put, delete, post](...)
            #   (if block=True return Message, else return mqtt mid number)
            # Agruments
            #   (resource[, data=None, block=True, timeout=60])

            # case 1: test GET
            print "GET %s" % REQ_RESOURCE
            res = self.publish.get(REQ_RESOURCE)
            if res.code != 404:
                print "GET is not supported, code 404 is expected"
                print res.to_json()
                self.stop()

            # case 2: test PUT with no data
            sleep(2)
            print "PUT %s" % REQ_RESOURCE
            res = self.publish.put(REQ_RESOURCE, None)
            if res.code != 400:
                print "data is required, code 400 is expected"
                print res.to_json()
                self.stop()

            # case 3: test PUT with empty data (no enable attribute)
            sleep(2)
            print "PUT %s" % REQ_RESOURCE
            res = self.publish.put(REQ_RESOURCE, data={})
            if res.code != 400:
                print "data.enable is required, code 400 is expected"
                print res.to_json()
                self.stop()

            # case 4: test PUT with enable=0
            sleep(2)
            print "PUT %s" % REQ_RESOURCE
            res = self.publish.put(REQ_RESOURCE, data={"enable": 0})
            if res.code != 200:
                print "data.enable=1 should reply code 200"
                print res.to_json()
                self.stop()

            # case 5: test PUT with enable=1 (reboot)
            sleep(2)
            print "PUT %s" % REQ_RESOURCE
            res = self.publish.put(REQ_RESOURCE, data={"enable": 1})
            if res.code != 200:
                print "data.enable=1 should reply code 200 and cause reboot"
                print res.to_json()

            # stop the test view
            self.stop()


if __name__ == "__main__":
    FORMAT = "%(asctime)s - %(levelname)s - %(lineno)s - %(message)s"
    logging.basicConfig(level=0, format=FORMAT)
    logger = logging.getLogger("Reboot")

    view = View(connection=Mqtt())
    view.start()
