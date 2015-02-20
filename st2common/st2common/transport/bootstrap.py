# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import st2common.config as config

from kombu import Connection
from oslo.config import cfg
from st2common.transport.execution import EXECUTION_XCHG
from st2common.transport.liveaction import LIVEACTION_XCHG
from st2common.transport.reactor import TRIGGER_CUD_XCHG, TRIGGER_INSTANCES_XCHG

LOG = logging.getLogger('st2common.transport.bootstrap')

EXCHANGES = [EXECUTION_XCHG, LIVEACTION_XCHG, TRIGGER_CUD_XCHG, TRIGGER_INSTANCES_XCHG]


def _setup():
    config.parse_args()

    # 2. setup logging.
    logging.basicConfig(format='%(asctime)s %(levelname)s [-] %(message)s',
                        level=logging.DEBUG)


def _do_register_exchange(exchange, channel):
    try:
        channel.exchange_declare(exchange=exchange.name, type=exchange.type,
                                 durable=exchange.durable, auto_delete=exchange.auto_delete,
                                 arguments=exchange.arguments, nowait=False, passive=None)
        LOG.info('registered exchange %s.', exchange.name)
    except Exception:
        LOG.exception('Failed to register exchange : %s.', exchange.name)


def _resgister_exchanges():
    LOG.info('=========================================================')
    LOG.info('############## Registering exchanges ####################')
    LOG.info('=========================================================')
    with Connection(cfg.CONF.messaging.url) as conn:
        channel = conn.default_channel
        for exchange in EXCHANGES:
            _do_register_exchange(exchange, channel)

def main():
    _setup()
    _resgister_exchanges()

# The scripts sets up Exchanges in RabbitMQ.
if __name__ == '__main__':
    main()
