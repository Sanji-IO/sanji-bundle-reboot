#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
import logging
import subprocess
from sanji.core import Sanji
from sanji.core import Route
from sanji.connection.mqtt import Mqtt


TURN_OFF_READYLED = '/etc/init.d/showreadyled stop'

# TODO: logger should be defined in sanji package?
logger = logging.getLogger()

class Reboot(Sanji):

    def init(self, bundle_env=os.getenv('BUNDLE_ENV', 'debug')):
        self.set_to_not_ready = TURN_OFF_READYLED
        self.call_reboot = 'reboot'
        if bundle_env == 'debug': # pragma: no cover
            self.set_to_not_ready = 'echo "%s"' % TURN_OFF_READYLED
            self.call_reboot = 'echo reboot'

    @Route(methods='put', resource='/system/reboot')
    def put(self, message, response):
        # TODO: status code should be added into error message
        if not hasattr(message, 'data') or 'enable' not in message.data:
            return response(code=400, data={'message': 'Invalid Input.'})

        if message.data['enable'] == 1:
            # Response success before reboot
            response()
            self.reboot()
            return
        return response()

    def reboot(self):
        # Waiting for web to log out
        time.sleep(5)
        logger.debug('Turn off the ready led')
        subprocess.call(self.set_to_not_ready, shell=True)
        # TODO: this should be a notice log for web
        logger.info('Rebooting...')
        subprocess.call(self.call_reboot, shell=True)


if __name__ == '__main__':
    FORMAT = '%(asctime)s - %(levelname)s - %(lineno)s - %(message)s'
    logging.basicConfig(level=0, format=FORMAT)
    logger = logging.getLogger('Reboot')

    reboot = Reboot(connection=Mqtt())
    reboot.start()
