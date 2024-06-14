import customtkinter as ctk
from math import ceil

    
def formatar(segundos: int = 0):
    
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


class App(ctk.CTkFrame):
    def __init__(self,
                 master: ctk.CTk) -> None:
        
        self.master = master
        self.master.geometry("640x480")
        self.master.resizable(False, False)
        self.master.wm_title("Pomoroids")

        self.pause_ = False
        self.timer_counter = 0
        self.sessions = 4
        self.actual_session = 1
        self.session_time = 5
        self.short_rest_time = 5

        self.clock = self.session_time

        # Labels
        self.header_label = ctk.CTkLabel(self.master,
                                         text=self.text_actual_session(self.sessions, self.actual_session),
                                         font=("Halvetica bold", 26))
        self.timer_label = ctk.CTkLabel(self.master,
                                        text=formatar(self.clock),
                                        font=("Halvetica bold", 26))

        # Labels positions
        self.timer_label.place(relx=0.5, rely=0.4, anchor="center")
        self.header_label.place(relx=0.5, rely=0.3, anchor="center")

        self.button = ctk.CTkButton(self.master,
                                    text="start",
                                    command=self.start_timer,
                                    corner_radius=20)
        self.button.place(relx=0.5, rely=0.6, anchor="center")
    
    def text_actual_session(self,
                            sessions,
                            actual_session):
        return f"Sessão {actual_session} de {sessions}"

    def start_timer(self):

        if float(self.clock) >= 0:
            decremento = 1 if self.timer_counter == 30 else 0
            self.clock = float(self.clock) - decremento
            self.formated_timer = formatar(self.clock)
            self.timer_label.configure(text=self.formated_timer)

            self.change_text()

            if not self.pause_:
                self.timer_label.after(33, self.start_timer)
                self.timer_counter = (self.timer_counter + 1) if self.timer_counter < 30 else 0
        else:
            
            self.actual_session += 1
            self.clock = self.session_time
            self.timer_label.configure(text=formatar(segundos=self.clock))
            self.header_label.configure(text=self.text_actual_session(sessions=self.sessions, actual_session=self.actual_session))
            self.button.configure(text="Start")
            self.button.configure(command=self.start_timer)

    def change_text(self):
        match self.pause_:
            case False:
                self.button.configure(text="Pause",
                                        command=self.pause)

            case True:
                self.button.configure(text="Start",
                                        command=self.pause)

    def pause(self):
        match self.pause_:
            case True:
                self.pause_ = False
                self.timer_label.after(33, self.start_timer)
            case False:
                self.pause_ = True


if __name__ == "__main__":
    app = ctk.CTk()
    master = App(master=app)
    app.mainloop()
