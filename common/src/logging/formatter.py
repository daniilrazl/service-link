import json
from typing import Any


def text_formatter(record: dict[str, Any]) -> str:
    user_extra = record["extra"].get("extra", {})
    if not isinstance(user_extra, dict):
        user_extra = {}

    extra_parts = []
    for key, value in user_extra.items():
        if value is not None:
            extra_parts.append(f"{key}={value}")

    extra_str = f" ({', '.join(extra_parts)})" if extra_parts else ""

    return (
        f"{record['time'].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} | "
        f"{record['level'].name: <8} | "
        f"{record['module']}:{record['function']}:{record['line']} | "
        f"{record['message']}{extra_str}\n"
    )


def json_formatter(record: dict[str, Any]) -> str:
    user_extra = record["extra"].get("extra", {})
    if not isinstance(user_extra, dict):
        user_extra = {}

    extra_fields = {k: v for k, v in user_extra.items() if v is not None}

    log_entry = {
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "module": record["module"],
        "function": record["function"],
        "line": record["line"],
        **extra_fields,
    }
    return json.dumps(log_entry, ensure_ascii=False) + "\n"