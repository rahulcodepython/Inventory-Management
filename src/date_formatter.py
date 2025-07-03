import datetime


def format_date(date_str: str | None = None) -> str:
    try:
        if date_str is None:
            return datetime.datetime.now().strftime("%d/%m/%Y")
        else:
            # date_str will be 2025-07-03 07:22:26
            return datetime.datetime.strptime(
                date_str, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")

    except ValueError:
        raise ValueError("Invalid date format. Expected YYYY-MM-DD.")
