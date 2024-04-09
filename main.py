from engine import*
from threading import Thread
from random import randint, choice
from colorama import Fore, Style, just_fix_windows_console

from os import environ, system
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame as pg


class Brownian:
    def __init__(self):
        self.__work  = True
        self.__cli   = False

        pg.init()
        pg.event.set_allowed((pg.QUIT, pg.VIDEORESIZE))

        self.__screen = pg.display.set_mode((ps.WIDTH, ps.HEIGHT), pg.RESIZABLE | pg.DOUBLEBUF | pg.HWSURFACE)
        self.__screen.set_alpha(None)

        pg.display.set_caption(ps.CAPTION)
        pg.display.set_icon(
            pg.image.load(ps.ICON)
        )

        self.__engine = Engine()


    def launch(self):
        clock = pg.time.Clock()

        while self.__work:
            self.__screen.fill(ps.FILL)

            for event in pg.event.get():
                if event.type == pg.QUIT and not self.__cli:
                    self.exit()
                elif event.type == pg.VIDEORESIZE:
                    ps.WIDTH, ps.HEIGHT = event.w, event.h
                    self.__screen = pg.display.set_mode((ps.WIDTH, ps.HEIGHT), pg.RESIZABLE)

            self.__engine.act(self.__screen, pg.draw)

            pg.display.update()
            clock.tick(75)


    def create(self, *args):
        N = int(args[0])
        radius, m, dx, dy, r, g, b = ps.RADIUS, ps.MASS, None, None, *ps.COLOR

        if len(args) > 1:
            N = 1
            radius, m = int(args[0]), int(args[1])
            dx, dy = int(args[2]), int(args[3])
            r, g, b = ps.COLOR_ALIASES[args[4]]

        V = [i for i in range(ps.V - 2, ps.V + 1)]
        for _ in range(N):
            self.__engine.create(Particle(
                self.__engine.count,
                (
                    randint(radius, ps.WIDTH - radius*2),
                    randint(radius, ps.HEIGHT - radius*2)
                ),
                (
                    choice((-1, 1)) * choice(V) if dx is None else dx,
                    choice((-1, 1)) * choice(V) if dy is None else dy,
                ),
                radius,
                m,
                (r, g, b)
            ))

        if N == 1:
            return f"{Fore.GREEN}UID:{Fore.WHITE} {self.__engine.count - 1}"


    def environment(self, N):
        N = int(N)
        V = [i for i in range(ps.V - 2, ps.V + 1)]
        for _ in range(N):
            self.__engine.create(Particle(
                self.__engine.count,
                (
                    randint(ps.RADIUS, ps.WIDTH - ps.RADIUS*2),
                    randint(ps.RADIUS, ps.HEIGHT - ps.RADIUS*2),
                ),
                (
                    choice((-1, 1)) * choice(V),
                    choice((-1, 1)) * choice(V)
                ),
                show=False
            ))


    def highlight(self, uid):
        self.__engine.highlight(int(uid))


    def track(self, seconds, uid):
        self.__engine.track(int(seconds), int(uid))
        self.__engine.pause()


    def clay(self):
        self.__engine.k = 0

    def exit(self):
        self.__work = False


    def cli(self):
        HELP = f"""
        {Fore.CYAN}создать{Fore.WHITE} {Fore.GREEN}РАДИУС МАССА DX DY ЦВЕТ{Fore.WHITE} - добавляет 1 частицу с заданными параметрами
        {Fore.CYAN}создать{Fore.WHITE} {Fore.GREEN}N{Fore.WHITE}                       - создаёт {Fore.GREEN}N{Fore.WHITE} частиц с параметрами по-умолчанию
        {Fore.CYAN}окружение{Fore.WHITE} {Fore.GREEN}N{Fore.WHITE}                     - создать {Fore.GREEN}N{Fore.WHITE} невидимых частиц с параметрами по-умолчанию
        {Fore.CYAN}очистить{Fore.WHITE}                        - удаляет все частицы
        {Fore.CYAN}кол-во{Fore.WHITE}                          - выводит кол-во частиц на экране
        {Fore.CYAN}выделить{Fore.WHITE} {Fore.GREEN}UIDS{Fore.WHITE}                   - прячет все частицы, кроме {Fore.GREEN}UISD{Fore.WHITE}
        {Fore.CYAN}следить{Fore.WHITE} {Fore.GREEN}T UID{Fore.WHITE}                   - рисует траекторию {Fore.GREEN}UID {Fore.WHITE} частицы {Fore.GREEN}T{Fore.WHITE} cекунд
        {Fore.CYAN}стоп{Fore.WHITE}                            - останавливает движение
        {Fore.CYAN}выход{Fore.WHITE}                           - выход из приложения
        {Fore.CYAN}сброс{Fore.WHITE}                           - сбрасывает изменения после {Fore.CYAN}выделить{Fore.WHITE}, {Fore.CYAN}следить{Fore.WHITE} или {Fore.CYAN}пластилин{Fore.WHITE}
        {Fore.CYAN}помощь{Fore.WHITE}                          - вывод справки\n"""

        PROMT = f"{Style.NORMAL}{Fore.CYAN}>>> {Fore.RESET}{Style.BRIGHT}"

        if self.__cli:
            commands = {
                "создать"  : self.create,
                "окружение": self.environment,
                "очистить" : self.__engine.collapse,
                "сколько"  : lambda: self.__engine.count,
                "выделить" : self.highlight,
                "следить"  : self.track,
                "стоп"     : self.__engine.pause,
                "выход"    : self.exit,
                "сброс"    : self.__engine.reset,
                "пластилин": self.clay,
                "помощь"   : lambda: HELP
            }

            print(f"{Style.BRIGHT}Добро пожаловать в утилиту BrownianEngine!\n{HELP}{Fore.RESET}")

            while self.__work:
                promt = input(PROMT).lower().split()
                try:
                    if len(promt) > 0:
                        command, args = promt[0], promt[1:] if len(promt) >= 1 else ()
                        if command in commands:
                            result = commands[command](*args)
                            if result:
                                print(result)
                        else:
                            print(f"{Fore.RED}Команда не существует{Fore.WHITE}")
                    
                except IndexError:
                    print(f"{Fore.RED}Частицы с таким {Fore.GREEN}UID{Fore.RED} не существует{Fore.WHITE}")
                except KeyError:
                    print(f"{Fore.RED}Такого цвета нет, но вы можете добавить его в {Fore.CYAN}parameters.py{Fore.WHITE}")
                # except Exception as e:
                #     print("Упс!", Fore.RED, e., Fore.WHITE)
            print(f"Выход...{Style.RESET_ALL}")
            return

        just_fix_windows_console()
        system("cls")
        self.__cli = True
        Thread(target=self.cli).start()


if __name__ == "__main__":
    app = Brownian()
    app.cli()
    app.launch()
