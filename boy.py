from pico2d import load_image, get_time

from state_machine import start_event, a_down
from state_machine import StateMachine, space_down, time_out, right_down, left_down, left_up, right_up


class Idle:
    @staticmethod
    def enter(boy, e):
        if start_event(e):
            boy.dir = 1
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1
        elif e[0] == 'TIME_OUT':
            if boy.face_dir == 1:
                boy.action = 3
            elif boy.face_dir == -1:
                boy.action = 2

        boy.frame = 0
        boy.start_time = get_time()
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 9999999999999999999999999999999999999:
            boy.state_machine.add_event(('TIME_OUT',))  # 튜플 형태로 전달

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class AutoRun:
    @staticmethod
    def enter(boy, e):
        boy.start_time = get_time()
        boy.autorun_plus_speed = 0
        boy.autorun_plus_size = 0
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * (3 + boy.autorun_plus_speed)

        if boy.x >= 800:
            boy.x = 800
        elif boy.x <= 0:
            boy.x = 0

        boy.autorun_plus_speed += 0.1
        boy.autorun_plus_size += 0.1
        if get_time() - boy.start_time > 1:
            boy.state_machine.add_event(('TIME_OUT',))  # 튜플 형태로 전달

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.action = 1
        elif boy.face_dir == -1:
            boy.action = 0

        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100,
                            boy.x, boy.y)
        pass

class Sleep:
    @staticmethod
    def enter(boy, e):
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.action = 3
            rad = 3.141592 / 2
        elif boy.face_dir == -1:
            boy.action = 2
            rad = 3.141592 / 2 * -1

        boy.image.clip_composite_draw(boy.frame * 100,
                                      boy.action * 100,
                                      100, 100,
                                      rad, '',
                                      boy.x - 25 * boy.face_dir,
                                      boy.y - 37,
                                      100, 100)

class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.action = 1
            boy.dir = 1
        elif left_down(e)or right_up(e):
            boy.action = 0
            boy.dir = -1
        boy.frame = 0
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 3
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100,
                            boy.x, boy.y)
        pass

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.autorun_plus_size = 0 #오토런때 추가할 사이즈
        self.autorun_plus_speed = 0 #오토런때 증가할 스피드
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, a_down: AutoRun},#time_out: Sleep},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
                #Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle}
                AutoRun: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(
            ('INPUT', event)
        )
        pass

    def draw(self):
        self.state_machine.draw()
