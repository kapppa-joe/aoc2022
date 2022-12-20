from datetime import date
import sys

import aoc_helper

def fetch_today():
    print("fetching today's puzzle...")
    fetch_day(date.today().day)

def fetch_day(day: int):
    if not day in range(1, 25 + 1):
        raise RuntimeError("can only fetch puzzle for day 1~-25")

    raw_data = aoc_helper.fetch(day, 2022)
    path = f'puzzle/day_{day:02}.txt'

    with open(path, 'w') as f:
        f.write(raw_data)
    
    print(f'Saved: {path}')

def fetch_all():
    for day in range(1, 26):
        fetch_day(day)

def interactive():
    print('please enter the day that you want to fetch puzzle for, or enter A to fetch all.')
    arg = input()
            
    match arg:
        case day if 1 <= int(day) <= 25:
            fetch_day(int(day))
        case 'A':
            fetch_all()
    


if __name__ == "__main__":

    got_argument = len(sys.argv) > 1
    today = date.today()

    if got_argument and sys.argv[1] == 'today' and today.month == 12 and today.day <= 25:
        fetch_today()
    elif got_argument and sys.argv[1] == 'all':
        fetch_all()
    else:
        interactive()