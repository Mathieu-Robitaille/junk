'''
https://www.codewars.com/kata/a-simplistic-tcp-finite-state-machine-fsm/train/python
'''


def traverse_TCP_states(events):
    STATES = ["CLOSED",
              "LISTEN",
              "SYN_RCVD",
              "SYN_SENT",
              "ESTABLISHED",
              "FIN_WAIT_1",
              "CLOSING",
              "FIN_WAIT_2",
              "TIME_WAIT",
              "CLOSE_WAIT",
              "LAST_ACK"]
    COMMANDS = ["APP_PASSIVE_OPEN",
                "APP_ACTIVE_OPEN",
                "RCV_SYN",
                "APP_SEND",
                "APP_CLOSE",
                "RCV_ACK",
                "RCV_SYN",
                "RCV_SYN_ACK",
                "APP_CLOSE",
                "RCV_FIN",
                "RCV_FIN_ACK",
                "RCV_ACK",
                "RCV_FIN",
                "APP_TIMEOUT",
                "APP_CLOSE",
                "RCV_ACK"]
    state = "CLOSED"
    for i in events:
        if state is STATES[0]:  # CLOSED
            if i is COMMANDS[0]:  # APP_PASSIVE_OPEN
                state = STATES[1]
                continue
            elif i is COMMANDS[1]:  # APP_ACTIVE_OPEN
                state = STATES[3]
                continue
        elif state is STATES[1]:  # LISTEN
            if i is COMMANDS[6]:
                state = STATES[2]
                continue
            elif i is COMMANDS[3]:
                state = STATES[3]
                continue
            elif i is COMMANDS[4]:
                state = STATES[0]
                continue
        elif state is STATES[2]:  # SYN_RCVD
            if i is COMMANDS[4]:
                state = STATES[5]
                continue
            elif i is COMMANDS[5]:
                state = STATES[4]
                continue
        elif state is STATES[3]:  # SYN_SENT
            if i is COMMANDS[6]:
                state = STATES[2]
                continue
            elif i is COMMANDS[7]:
                state = STATES[4]
                continue
            elif i is COMMANDS[4]:
                state = STATES[0]
                continue
        elif state is STATES[4]:  # ESTABLISHED
            if i is COMMANDS[4]:
                state = STATES[5]
                continue
            elif i is COMMANDS[9]:
                state = STATES[9]
                continue
        elif state is STATES[5]:  # FIN_WAIT_1
            if i is COMMANDS[9]:
                state = STATES[6]
                continue
            if i is COMMANDS[10]:
                state = STATES[8]
                continue
            if i is COMMANDS[11]:
                state = STATES[7]
                continue
        elif state is STATES[6]:  # CLOSING
            if i is COMMANDS[5]:
                state = STATES[8]
                continue
        elif state is STATES[7]:  # FIN_WAIT_2
            if i is COMMANDS[9]:
                state = STATES[8]
                continue
        elif state is STATES[8]:  # TIME_WAIT
            if i is COMMANDS[13]:
                state = STATES[0]
                continue
        elif state is STATES[9]:  # CLOSE_WAIT
            if i is COMMANDS[14]:
                state = STATES[10]
                continue
        elif state is STATES[10]:  # LAST_ACK
            if i is COMMANDS[15]:
                state = STATES[0]
                continue
    return state
