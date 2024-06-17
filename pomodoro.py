from typing import Generator


def countdown(seconds: int) -> Generator:
    zero_second:    int = 0
    one_second:     int = 1

    for current_elapsed in range(seconds, zero_second - 1, -one_second):
        print('Tempo restante {} segundo(s)'.format(current_elapsed))
        yield current_elapsed

def start_session(session_time: int, description: str = 'Sessão') -> Generator:
    for second in countdown(session_time):
        yield second, description

def start_short_rest(rest_time: int) -> Generator:
    return start_session(rest_time, 'Descanso curto')

def start_long_rest(rest_time: int) -> Generator:
    return start_session(rest_time, 'Descanso longo')

def create_sessions(quantity: int, time_in_sec: int, short_rest_in_sec: int, long_rest_in_sec: int) -> Generator:
    for session_number in range(0, quantity):
        yield {
            'current_session': session_number + 1,
            'sessions': quantity,
            'countdown': countdown(time_in_sec),
            'rest': start_long_rest(long_rest_in_sec) if session_number == quantity - 1 else start_short_rest(short_rest_in_sec)
        }
