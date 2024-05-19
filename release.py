#!/usr/bin/env python3
NULL_CHAR = chr(0)

import time


def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

write_report(NULL_CHAR*8)