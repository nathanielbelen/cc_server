from src.common.hid_writer import write_report
from src.common.keyboard_dict import keyboard_dict, modifier_dict
import time

class Key_State:
    def __init__(self):
        self.modifier = None
        self.key_list = []
        self.time_last = time.time()

    def key_down(self, key):
        if key not in keyboard_dict and key not in modifier_dict:
            raise KeyError(f"Key '{key}' not found in keyboard_dict and modifier_dict")

        if key in modifier_dict:
            self.modifier = key
            return self.send_report()

        if key not in self.key_list:  # check if key is already in the list
            self.key_list.append(key)

        self.send_report()

    def key_up(self, *keys_to_remove):
        removed = False
        for key in keys_to_remove:
            if self.modifier == key:
                removed = True
                self.modifier = None
            while key in self.key_list:
                removed = True
                self.key_list.remove(key)
        if removed:
            self.send_report()

    def key_release_all(self):
        self.key_list = []  # empty the key_list
        self.modifier = None
        self.send_report()

    def direction(self, key):
        if key != 'RIGHT' and key != 'LEFT':
            raise KeyError(f"Key '{key}' not a directional key")

        required_send = False

        for direction in ['RIGHT', 'LEFT']:
            if direction != key:
                if direction in self.key_list:
                    self.key_list.remove(direction)
                    required_send = True

        if key not in self.key_list:  # check if key is already in the list
            self.key_list.append(key)
            required_send = True

        if required_send:
            self.send_report()

    def send_report(self):
            # format of report:
            # write_report(NULL_CHAR*2+chr(4)+NULL_CHAR*5)
            # MODIFIER | NULL_CHAR | 6X KEYS
            # when empty, send NULL_CHAR*8
        # print(f'{self.modifier}, {self.key_list}')
        if self.key_list or self.modifier:
            curr_time = time.time()
            print(f"{round(curr_time - self.time_last, 4)}s - {self.modifier} {self.key_list}")
            self.time_last = curr_time
        report = generate_report(self.modifier, self.key_list)
        write_report(report)


def generate_report(modifier, char_list):
    base = keyboard_dict['NULL'] * 2
    if modifier:
        base = modifier_dict[modifier] + keyboard_dict['NULL']
    for char in char_list:
        base += keyboard_dict[char]
    while len(base) < 8:
        base += keyboard_dict['NULL']
    return base