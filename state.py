import enum


class AppStates(enum.Enum):
    STOPPED    = 'Iniciar'
    IN_SESSION = 'Em sessão'
    IN_REST    = 'Em descanso'
    PAUSED     = 'Pausado'


class AppState:
    last_state    = AppStates.PAUSED.value
    current_state = AppStates.PAUSED.value

GLOBAL_STATE = AppState()
