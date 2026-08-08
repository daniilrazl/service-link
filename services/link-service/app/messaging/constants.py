from aio_pika import DeliveryMode, ExchangeType

ROUTING_KEY_LINK_CREATED = "link.created"
EXCHANGE_TYPE = ExchangeType.TOPIC
DELIVERY_MODE = DeliveryMode.PERSISTENT
