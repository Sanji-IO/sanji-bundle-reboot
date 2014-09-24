#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
from sanji.core import Sanji
from sanji.core import Route
from sanji.connection.mqtt import Mqtt


TURN_OFF_READYLED = '/etc/init.d/showreadyled stop'

class Reboot(Sanji):

    def init(self):
        pass

    @Route(methods='put', resource='/system/reboot')
    def put(self, message, response):
        if not hasattr(message, 'data') or 'enable' not in message.data:
            return response(code=400, data={'message': 'Invaild Input.'})

        if message.data['enable'] == 1:
            # Response success before reboot
            response()

            # Waiting for web to log out
            sleep(5)
            logger.debug('Turn off the ready led')
            subprocess.call(TURN_OFF_READYLED, shell=True)
            logger.info('Rebooting...')
            subprocess.call('reboot', shell=True)
            print 'reboot'
            return

        return response()


if __name__ == '__main__':
    FORMAT = '%(asctime)s - %(levelname)s - %(lineno)s - %(message)s'
    logging.basicConfig(level=0, format=FORMAT)
    logger = logging.getLogger('Reboot')

    reboot = Reboot(connection=Mqtt())
    reboot.start()
