#event ( 종류 문자열, 실제 값)
from pygame.event import event_name
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT


def space_down(e):
    return (e[0] == 'INPUT' and
            e[1].type == SDL_KEYDOWN and
            e[1].key == SDLK_SPACE)

def time_out(e):
    return (e[0] == 'TIME_OUT')

def start_event(e):
    return e[0] == 'START'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT




#상태 머신을 처리 관리 해주는 클래스
class StateMachine:
    def __init__(self, o):
        self.o = o
        self.event_que = []

    def update(self):
        self.cur_state.do(self.o)
        if self.event_que:
            e = self.event_que.pop(0)
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e):
                    self.cur_state.exit(self.o, e)
                    print(f'EXIT from {self.cur_state}')
                    self.cur_state = next_state
                    self.cur_state.enter(self.o, e)
                    print(f'ENTER from {next_state}')
                    return


    def start(self, start_state):
        self.cur_state = start_state
        self.cur_state.enter(self.o, ('START',0))
        print(f'Enter into {self.cur_state}')

    def draw(self):
        self.cur_state.draw(self.o)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def add_event(self, e):
        self.event_que.append(e)
        print(f'    DEBUG: new event {e} is added')