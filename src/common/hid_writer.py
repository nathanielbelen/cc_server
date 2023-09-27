def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())
