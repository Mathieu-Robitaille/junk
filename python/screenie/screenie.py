#!/usr/bin/env python3

import datetime
import json
import os
import smtplib
import subprocess
import sys
from time import sleep

try:
    from colorama import Fore, Back, Style
except ImportError:
    print("Could not import colorama, please install it \n\t pip3 install colorama")
    sys.exit(0)

LINUX = False
if sys.platform.startswith("linux"):
    import syslog

    LINUX = True


def fast_ping(ip_to_ping):
    params = ['nmap', '-n', '-sP', '{}'.format(ip_to_ping.split(" ")[0])]
    r = subprocess.Popen(params, stdout=subprocess.PIPE)
    if "1 host up" in str(r.communicate()[0]):
        return "successfully pinged {}".format(ip_to_ping)
    else:
        return "failed to ping {}".format(ip_to_ping)


def console_manager(data):
    os.system('clear')
    for line in data:
        if line.split(' ')[0] == "successfully":
            print(Back.GREEN + Fore.LIGHTBLACK_EX + line + Style.RESET_ALL)
            if LINUX:
                syslog.syslog(syslog.LOG_INFO, line)
        else:
            print(Back.RED + Fore.LIGHTBLACK_EX + line + Style.RESET_ALL)
            if LINUX:
                syslog.syslog(syslog.LOG_ERR, line)


def import_ips():
    with open('ips.json') as data_file:
        return json.load(data_file)


def convert_status_to_bool(string):
    if string.startswith('successfully'):
        return True
    else:
        return False


def write_status(ping_status):
    output = []
    for line in ping_status:
        output.append(convert_status_to_bool(line))
    with open('status.json', 'w') as data_file:
        json.dump(output, data_file)


def check_status(current_data_set):
    with open('status.json') as old_data_set:
        loaded_old_set = json.load(old_data_set)
        for i in range(len(current_data_set)):
            if convert_status_to_bool(current_data_set[i]) is not loaded_old_set[i]:
                if loaded_old_set[i]:
                    send_email('{} is down'.format(import_ips()[i]), 'mathieu@avidtwo.com', False)


def send_email(data, dest_email, use_internal_relay=False):
    print(
        Back.MAGENTA + Fore.LIGHTBLACK_EX + 'Emailing {} about failed connection'.format(dest_email) + Style.RESET_ALL)
    if LINUX:
        syslog.syslog(syslog.LOG_INFO, 'Emailing {} about failed connection'.format(dest_email))
    try:
        if use_internal_relay:
            server = smtplib.SMTP('smtp.avidtwo.com.')
        else:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login('notice@avidtwo.com', '100% the real password')
        server.sendmail('notice@avidtwo.com', dest_email, data)
    except:
        if LINUX:
            syslog.syslog(syslog.LOG_ERR, 'Sending the email failed')


def main():
    ping_status = []
    for ip in import_ips():
        ping_status.append(fast_ping(ip))
    console_manager(ping_status)
    check_status(ping_status)
    write_status(ping_status)


if __name__ == "__main__":
    while True:
        main()
        print('Current time is - {} - sleeping {} seconds until next loop'
              .format(datetime.datetime.now(),
                      (5 - datetime.datetime.now().minute % 5) * 60))
        sleep((5 - datetime.datetime.now().minute % 5) * 60)
