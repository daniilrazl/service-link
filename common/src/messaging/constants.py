from aio_pika import DeliveryMode, ExchangeType

EXCHANGE_TYPE = ExchangeType.TOPIC
DELIVERY_MODE = DeliveryMode.PERSISTENT

ROUTING_KEY_LINK_CREATED = "link.created"
