#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
import logging
import subprocess
import sh
from sanji.core import Sanji
from sanji.core import Route
from sanji.connection.mqtt import Mqtt


TURN_OFF_READYLED = "/etc/init.d/showreadyled stop"

# TODO: logger should be defined in sanji package?
logger = logging.getLogger()


class Reboot(Sanji):

    def init(self, *args, **kwargs):
        self.set_to_not_ready = TURN_OFF_READYLED
        self.call_reboot = "reboot"
        self.path_root = os.path.abspath(os.path.dirname(__file__))
        try:
            self.bundle_env = kwargs["bundle_env"]
        except KeyError:
            self.bundle_env = os.getenv("BUNDLE_ENV", "debug")
            self.set_to_not_ready = "echo '%s'" % TURN_OFF_READYLED
            self.call_reboot = "echo reboot"

    def run(self):
        try:
            output = sh.test("-e", "%s/reboot-failed" % self.path_root)
            if output.exit_code == 0:
                self.publish.event.put(
                    "/system/reboot",
                    data={"code": "REBOOT_FAIL", "type": "event"})
            sh.rm("-rf", "%s/reboot-failed" % self.path_root)
        except sh.ErrorReturnCode_1:
            pass

        try:
            output = sh.test("-e", "%s/rebooting" % self.path_root)
            if output.exit_code == 0:
                logger.info("Reboot success!")
                self.publish.event.put(
                    "/system/reboot",
                    data={"code": "REBOOT_SUCCESS", "type": "event"})
            sh.rm("-rf", "%s/rebooting" % self.path_root)
        except sh.ErrorReturnCode_1:
            pass
        sh.sync()

    def reboot(self):
        # TODO: double check web notification with Zack*2
        self.publish.event.put(
            "/system/reboot",
            data={"code": "REBOOTING", "type": "event"})
        sh.touch("%s/rebooting" % self.path_root)
        sh.sync()

        # Waiting for web to log out
        time.sleep(5)
        logger.debug("Turn off the ready led.")
        subprocess.call(self.set_to_not_ready, shell=True)
        logger.info("Rebooting...")
        returncode = subprocess.call(self.call_reboot, shell=True)
        if returncode != 0:
            logger.info("Reboot failed!")
            sh.touch("%s/reboot-failed" % self.path_root)
            sh.sync()

    @Route(methods="put", resource="/system/reboot")
    def put(self, message, response):
        # TODO: status code should be added into error message
        if not hasattr(message, "data") or "enable" not in message.data:
            return response(code=400, data={"message": "Invalid Input."})

        if message.data["enable"] == 1:
            # Response success before reboot
            response()
            self.reboot()
            return
        return response()


if __name__ == "__main__":
    FORMAT = "%(asctime)s - %(levelname)s - %(lineno)s - %(message)s"
    logging.basicConfig(level=0, format=FORMAT)
    logger = logging.getLogger("Reboot")

    reboot = Reboot(connection=Mqtt())
    reboot.start()
