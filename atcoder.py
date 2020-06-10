import requests
from bs4 import BeautifulSoup

from contest import Contest

ATCODER_BASE_URL = 'https://atcoder.jp'


def fetch_upcoming_contest():
    response = _fetch_home_page()
    upcoming_contests = _parse_upcoming_contests(response)
    contest_info = _get_upcoming_contest_info(upcoming_contests)

    return contest_info


def _fetch_home_page():
    ''' See:
        https://requests.readthedocs.io/en/master/
    '''

    HOME_PAGE = ATCODER_BASE_URL + '/home'
    response = requests.get(HOME_PAGE)

    return response


def _parse_upcoming_contests(response):
    ''' See:
        https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    '''

    soup = BeautifulSoup(response.text, 'html.parser')
    upcoming_contests = soup.find(id='contest-table-upcoming')

    return upcoming_contests


def _get_upcoming_contest_info(upcoming_contests):
    ''' HACK: The codes depend on AtCoder Home page.
        contest_info contains below information:

        ignore       : http://www.timeanddate.com/worldclock/fixedtime.html?
                       iso=202xxxxxTxxxx&px=xxx
        contest date : 202x-xx-xx xx:xx:xx+0900
        contest url  : /contests/abbreviated_contest_name
        contest name : hogehoge
    '''
    contest_info = upcoming_contests.find_all('a', limit=2)
    name, start_date, url = '', '', ''

    for index, link in enumerate(contest_info):
        if index == 0:
            start_date = _fix_contest_date_format(link.text)
        elif index == 1:
            name = link.text
            url = ATCODER_BASE_URL + link['href']

    contest = Contest(name=name, start_date=start_date, url=url)

    return contest


# HACK: Not good solution.
#       It is necessary to add '+X:XX',
#       but builtin function may be existed.
def _fix_contest_date_format(date: str) -> str:
    ''' Expected: 202x-xx-xx xx:xx:xx+09:00
        Actual  : 202x-xx-xx xx:xx:xx+0900
    '''
    left = date[:-2]
    right = date[-2:]

    fixed_date_format = left + ':' + right

    return fixed_date_format


def main():
    contest_info = fetch_upcoming_contest()
    print(contest_info)


if __name__ == '__main__':
    main()