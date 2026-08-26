import logging


class TransactionLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        transaction_id = self.extra.get(
            "transaction_id",
            "-",
        )

        return (
            f"[x-tps-value-id={transaction_id}] {msg}",
            kwargs,
        )


def get_logger() -> logging.Logger:
    logger = logging.getLogger("av-scan-svc")

    if not logger.handlers:
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False

    return logger


def get_transaction_logger(
    transaction_id: str | None,
) -> TransactionLoggerAdapter:
    return TransactionLoggerAdapter(
        get_logger(),
        {
            "transaction_id": transaction_id or "-",
        },
    )
