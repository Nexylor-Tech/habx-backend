from dodopayments import AsyncDodoPayments

from app.config import settings
from app.logger_config import setting


class Client:
    if not settings.DODO_API_KEY:
        setting.logger.error("DODO_API_KEY is not set")
    dodo_client = AsyncDodoPayments(
        bearer_token=settings.DODO_API_KEY.get_secret_value(),
        environment=settings.DODO_ENVIRONMENT,
    )


client = Client()
