import customtkinter as ctk
import pomodoro
import enum
import json
import apps
from math import ceil
from dacite import from_dict
from dataclasses import dataclass



class AppStates(enum.Enum):
    STOPPED    = 'Iniciar'
    IN_SESSION = 'Em sessão'
    IN_REST    = 'Em descanso'
    PAUSED     = 'Pausado'


class AppState:
    last_state    = AppStates.PAUSED.value
    current_state = AppStates.PAUSED.value

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


class App(ctk.CTkFrame):
    __master = ctk.CTk()
    __state  = AppState()

    def __init__(self, title: str, size: tuple) -> None:
        self.__state.current_state = AppStates.STOPPED.value
        self.__settings = self.__load_settings()
        
        self.__sessions_iter  = pomodoro.create_sessions(self.__settings.sessions, 
                                                        self.__settings.session_time, 
                                                        self.__settings.short_rest_in_seconds, 
                                                        self.__settings.long_rest_in_seconds)

        self.__current_session = next(self.__sessions_iter)
        self.__elapsed = self.__current_session['countdown'] 
 
        self.__master.wm_geometry("{}x{}".format(size[0], size[1]))
        self.__master.minsize(size[0], size[1])
        self.__master.resizable(True, True)
        self.__master.wm_title(title)

        self.__render_home_screen()

    def __render_home_screen(self):
        self.settings_btn = ctk.CTkButton(self.__master,
                                    text="⚙",
                                    command=lambda: print('settings pressed!'),
                                    fg_color='transparent',
                                    width=24,
                                    height=24,
                                    corner_radius=20)

        self.settings_btn.place(relx=0.9, rely=0.1, anchor="center")

        self.header_label = ctk.CTkLabel(self.__master,
                                         text=self.__state.current_state,
                                         font=("Halvetica bold", 26))
       
        self.header_label.place(relx=0.5, rely=0.3, anchor="center")

        self.timer_label = ctk.CTkLabel(self.__master,
                                        text=self.__format(next(self.__elapsed)),
                                        font=("Halvetica bold", 26))

        self.timer_label.place(relx=0.5, rely=0.4, anchor="center")

        self.button = ctk.CTkButton(self.__master,
                                    text="Iniciar",
                                    command=self.toggle,
                                    corner_radius=20)

        self.button.place(relx=0.5, rely=0.6, anchor="center")
    
    def __refresh_home_screen(self):
        session_number = self.__current_session['current_session']
        sessions_length = self.__current_session['sessions']

        self.button.configure(text=self.get_text_button())

        if self.__state.current_state == AppStates.PAUSED.value:
            return

        self.header_label.configure(text=self.__state.current_state + ' ' + str(session_number) + ' de ' + str(sessions_length))
        self.__master.after(500, self.__refresh_home_screen)

    def __refresh_all_screen(self):
        self.__master.after(200, self.__refresh_home_screen)
        self.timer_label.after(1000, self.__in_timer)

    def __draw_restart_button(self):
        self.restart_btn = ctk.CTkButton(self.__master,
                                    text="Reiniciar",
                                    command=self.__restart_pomodoro,
                                    corner_radius=20)

        self.restart_btn.place(relx=0.5, rely=0.7, anchor="center")

    def __load_settings(self) -> Settings:
        settings_filename = 'settings.json'
        with open(settings_filename, 'r') as file:
            data = json.load(file)
            return from_dict(data_class=Settings, data=data)

    def __format(self, segundos: int = 0):
        segundos_: int = segundos
        minutos: int = 0
        horas: int = 0

        while True:
            match segundos_:
                case segundos_ if segundos_ >= 3600:
                    segundos_ -= 3600
                    horas += 1
            
                case segundos_ if segundos_ >= 60:
                    segundos_ -= 60
                    minutos += 1
                
                case _:
                    break

        horas_formatadas = f"0{horas}" if horas < 10 else f"{horas}"
        minutos_formatados = f"0{minutos}" if minutos < 10 else f"{minutos}"
        segundos_formatados = f"0{ceil(segundos_)}" if ceil(segundos_) < 10 else f"{ceil(segundos_)}"

        tempo_com_horas = f"{horas_formatadas} : {minutos_formatados} : {segundos_formatados}"
        tempo_sem_horas = f"{minutos_formatados} : {segundos_formatados}"
        return tempo_com_horas if horas else tempo_sem_horas

    def __restart_pomodoro(self):
        print('Reiniciado')
        self.__sessions_iter  = pomodoro.create_sessions(3, 4, 2, 3)
        self.__current_session = next(self.__sessions_iter)
        self.__elapsed = self.__current_session['countdown']
        final_elapsed = self.__format(next(self.__elapsed))
        self.timer_label.configure(text=final_elapsed)
        self.__state.current_state = AppStates.STOPPED.value

    
    def toggle(self):
        match self.__state.current_state:
            case AppStates.STOPPED.value:
                # NOTE: Começa a sessão
                self.__state.current_state = AppStates.STOPPED.value
                self.__state.current_state = AppStates.IN_SESSION.value
                self.__refresh_all_screen()
                self.__draw_restart_button()
            case AppStates.PAUSED.value:
                # NOTE: Retoma a sessão/descanso
                self.__state.current_state = self.__state.last_state
                self.__refresh_all_screen()
                self.__draw_restart_button()
            case AppStates.IN_SESSION.value: 
                # NOTE: Pausa a sessão/decanso
                self.__state.last_state = AppStates.IN_SESSION.value
                self.__state.current_state = AppStates.PAUSED.value
            case AppStates.IN_REST.value:
                self.__state.last_state = AppStates.IN_REST.value
                self.__state.current_state = AppStates.PAUSED.value

    def __in_timer(self):
        match self.__state.current_state:
            case AppStates.IN_SESSION.value | AppStates.IN_REST.value:
                try:
                    if self.__state.current_state == AppStates.IN_SESSION.value:
                        for app in self.__settings.blacklist.apps:
                            apps.finalizar_processo(app)

                    raw_elapsed   = next(self.__elapsed)
                    final_elapsed = self.__format(raw_elapsed)
                    self.timer_label.configure(text=final_elapsed)
                    self.timer_label.after(1000, self.__in_timer)
                except StopIteration:
                    try:
                        self.__state.last_state = AppStates.IN_SESSION.value
                        self.__state.current_state = AppStates.IN_REST.value
                        raw_elapsed, description = next(self.__current_session['rest'])
                        print('Descanso: {}'.format(description))
                        final_elapsed = self.__format(raw_elapsed)
                        self.timer_label.configure(text=final_elapsed)
                        self.timer_label.after(1000, self.__in_timer)
                    except StopIteration:
                        try:
                            self.__state.last_state = AppStates.IN_REST.value
                            self.__state.current_state = AppStates.IN_SESSION.value
                            self.__current_session = next(self.__sessions_iter)
                            self.__elapsed = self.__current_session['countdown']
                            raw_elapsed   = next(self.__elapsed)
                            final_elapsed = self.__format(raw_elapsed)
                            self.timer_label.configure(text=final_elapsed)
                            self.timer_label.after(1000, self.__in_timer)
                        except StopIteration:
                            self.__restart_pomodoro()

    def get_text_button(self):
        match self.__state.current_state:
            case AppStates.STOPPED.value:
                return 'Iniciar'
            case AppStates.PAUSED.value:
                return 'Retomar'
            case AppStates.IN_SESSION.value | AppStates.IN_REST.value:
                return 'Pausar'

    def run(self):
        self.__master.mainloop()

if __name__ == "__main__":
    app = App(title='Pomoroids', size=(480, 480))
    app.run()
