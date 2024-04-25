import aiocron
from datetime import date, datetime, timedelta
from src.logger.logger import logger

error_log_path: str = "error.log"

def check_log_age() -> date | None:
    date_chars: list[str] = []
    try:
        with open(error_log_path, 'r', encoding='utf-8') as file:
            while True:
                char = file.read(1)
                if not char or char.isspace():
                    break
                date_chars.append(char)

            date_str: str = ''.join(date_chars)
            log_age = datetime.strptime(date_str, '%Y-%m-%d').date()
            return log_age
    except Exception as e:
        logger.warning(e)

def is_date_at_least_three_days_old(given_date: date) -> bool:
    today = date.today()
    print(today)
    three_days_ago = today - timedelta(days=3)
    print(three_days_ago)
    return given_date <= three_days_ago

async def clear_error_log() -> None:
    log_age: date | None = check_log_age()
    if not log_age:
        return

    if not is_date_at_least_three_days_old(log_age):
        return

    with open(error_log_path, 'w', encoding='utf-8') as file:
        pass

scheduled_clear = aiocron.crontab('0 0 */3 * *', func=clear_error_log)
