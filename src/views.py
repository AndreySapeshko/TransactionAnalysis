import datetime


def get_start_date() -> datetime:
    todey = datetime.datetime.today().strftime('%m.%Y')
    return datetime.datetime.strptime(f'01.{todey}', '%d.%m.%Y')

print(get_start_date().strftime('%d.%m.%Y'))