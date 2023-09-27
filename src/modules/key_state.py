from common.hid_writer import write_report
from src.common.keyboard_dict import keyboard_dict

class Key_State:
    def __init__(self):
        self.key_list = []

    def key_down(self, key):
        if key not in keyboard_dict:
            raise KeyError(f"Key '{key}' not found in keyboard_dict")

        self.key_list.append(key)
        self.send_report()

    def key_up(self, *keys_to_remove):
        for key in keys_to_remove:
            while key in self.key_list:
                self.key_list.remove(key)
        self.send_report()

    def key_release_all(self):
        self.key_list = []  # empty the key_list
        self.send_report()

    def send_report(self):
        # format of report:
        # write_report(NULL_CHAR*2+chr(4)+NULL_CHAR*5)
        # MODIFIER | NULL_CHAR | 6X KEYS
        # when empty, send NULL_CHAR*8
        print(self.key_list)
        report = generate_report(self.key_list)
        write_report(report)


def generate_report(list):
    base = keyboard_dict['NULL']*2
    for char in list:
        base += keyboard_dict[char]
    while len(base) < 8:
        base += keyboard_dict['NULL']
    return base