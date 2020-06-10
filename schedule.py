from datetime import datetime
from datetime import timedelta
from pytz import timezone


def set_jst():
    # See:
    # https://github.com/stub42/pytz/blob/master/src/README.rst
    # https://note.nkmk.me/python-datetime-pytz-timezone/
    jst = timezone('Asia/Tokyo')

    return jst


def get_now_jst():
    # See:
    # https://docs.python.org/ja/3/library/datetime.html
    jst = set_jst()
    now_jst = datetime.fromisoformat(str(datetime.now(jst)))

    return now_jst


def calc_time_remaining(contest_start_time, now_jst):
    diff = datetime.fromisoformat(str(contest_start_time)) - now_jst
    remain_hours = diff.seconds // 3600
    remain_minutes = (diff.seconds % 3600) // 60

    return remain_hours, remain_minutes


def set_announce_time(contest_start_time: str, before_hours: int):
    delta = timedelta(hours=before_hours)
    contest_start_time = datetime.fromisoformat(contest_start_time)
    announce_start_time = contest_start_time - delta

    return contest_start_time, announce_start_time


# HACK: Not good solution.
#        It is necessary to remove '+X:XX',
#        but builtin function may be existed.
def remove_timezone(time) -> str:
    return str(time).split('+')[0]