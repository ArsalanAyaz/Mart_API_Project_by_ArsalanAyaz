from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)
BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER", cast=str)
KAFKA_ORDER_TOPIC = config("KAFKA_ORDER_TOPIC", cast=str)
# KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT = config("KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT", cast=str)


SMTP_HOST = config("SMTP_HOST", cast=str)
SMTP_USER = config("SMTP_USER", cast=str)
SMTP_PASSWORD = config("SMTP_PASSWORD", cast=str)
EMAILS_FROM_EMAIL = config("EMAILS_FROM_EMAIL", cast=str)
SMTP_TLS = config("SMTP_TLS", cast=str)
SMTP_SSL = config("SMTP_SSL", cast=str)
SMTP_PORT = config("SMTP_PORT", cast=str)
EMAILS_FROM_NAME = config("EMAILS_FROM_NAME", cast=str)
emails_enabled = True
#EMAILS_FROM_EMAIL = ""



# TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)
