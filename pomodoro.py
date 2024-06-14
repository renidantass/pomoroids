from contextlib import redirect_stdout
from dataclasses import dataclass
from dacite import from_dict
from apps import finalizar_processo
from typing import Generator
import time
import json


def countdown(seconds: int) -> Generator:
    initial_second: int = 1
    one_second:     int = 1

    for current_elapsed in range(initial_second, seconds + 1):
        print('Tempo decorrido {} segundo(s)'.format(current_elapsed))
        time.sleep(one_second)
        yield current_elapsed

def pomodoro(sessions: int, session_time: int, short_rest_time: int, long_rest_time: int, apps: list[str]):
    total_elapsed: int = 0

    pomodoro_stats = {
        'sessions': [],
        'short_rest_sessions': [],
        'long_rest_sessions': []
    }

    for session_number in range(0, sessions):
        print('Session {} in progress'.format(session_number + 1))

        session_elapsed = 0

        for second in countdown(session_time):
            session_elapsed += second
            
            for app in apps:
                finalizar_processo(app)

        pomodoro_stats['sessions'].append({
            'session_number': session_number + 1,
            'session_time': session_elapsed,
            'status': 'completed'
        })

        print('Session {} completed'.format(session_number + 1))
        
        total_elapsed += session_elapsed

        if session_number < sessions - 1:
            print('Short rest')
            rest_elapsed = 0

            for second in countdown(short_rest_time):
                rest_elapsed += second

            pomodoro_stats['short_rest_sessions'].append({
                'session_number': session_number + 1,
                'rest_time': rest_elapsed,
                'status': 'completed'
            })

            total_elapsed += rest_elapsed
        else:
            print('Long rest')
            long_rest_elapsed = 0

            for second in countdown(long_rest_time):
                long_rest_elapsed += second

            pomodoro_stats['long_rest_sessions'].append({
                'session_number': session_number + 1,
                'rest_time': long_rest_elapsed,
                'status': 'completed'
            })

            total_elapsed += long_rest_elapsed
            print('Pomodoro completed')

            print(pomodoro_stats)

            return pomodoro_stats
    return {}

@dataclass
class Blacklist:
    apps: list[str]
    sites: list[str]

@dataclass
class Settings:
    pomodoro: int
    sessions: int
    session_time: int
    short_rest_in_seconds: int
    long_rest_in_seconds: int
    blacklist: Blacklist


def load_settings() -> Settings:
    settings_filename = 'settings.json'
    with open(settings_filename, 'r') as file:
        data = json.load(file)
        return from_dict(data_class=Settings, data=data)
        

if __name__ == '__main__':
    settings = load_settings()

    pm = pomodoro(
        settings.pomodoro, 
        settings.session_time, 
        settings.short_rest_in_seconds, 
        settings.long_rest_in_seconds,
        settings.blacklist.apps
    )
