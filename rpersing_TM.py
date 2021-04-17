import sys
import re

try:
    filename = sys.argv[1]
    # filename = "awa.tm"
    given_string = sys.argv[2]
    # given_string = "abbaab"
    mode = "non-verbose"
except IndexError:
    print("Correct usage: [py file] [filename] [string] optional: verbose")
    sys.exit(1)


try:
    mode = sys.argv[3]
except IndexError:
    pass


# Ask Stephen for help on this. Clearly you are doing something wrong and do not yet hold the
# knowledge to unlock the door to success
def transitionV(curr_string, tape_state, accept, reject, tape_pos):

    for s in curr_string:
        if s not in INPUT_ALPHABET:
            return print("Malformed.")

    curr_string.insert(tape_pos, tape_state)
    print(curr_string)
    curr_string.pop(tape_pos)

    while True:
        # curr_string.insert(tape_pos, tape_state)
        symbol_at_pos = curr_string[tape_pos]

        curr_string[tape_pos] = transitions[tape_state][symbol_at_pos][1]
        if transitions[tape_state][symbol_at_pos][2] == "R":

            tape_pos += 1
            curr_string.insert(tape_pos, tape_state)
            print(curr_string)
            curr_string.pop(tape_pos)
            if tape_pos == len(curr_string):
                curr_string.append("_")

        elif transitions[tape_state][symbol_at_pos][2] == "L":

            tape_pos -= 1
            curr_string.insert(tape_pos, tape_state)
            print(curr_string)
            curr_string.pop(tape_pos)
            if curr_string[-1] == "_" and tape_pos == len(curr_string) - 2:
                curr_string.pop()

        tape_state = transitions[tape_state][symbol_at_pos][0]
        if tape_state == accept:
            curr_string.insert(tape_pos, tape_state)
            print(curr_string)
            curr_string.pop(tape_pos)
            return print("Accepted!")

        if tape_state == reject:
            curr_string.insert(tape_pos, tape_state)
            print(curr_string)
            curr_string.pop(tape_pos)
            return print("Rejected.")


def transitionNV(curr_string, tape_state, accept, reject, tape_pos):

    for s in curr_string:
        if s not in INPUT_ALPHABET:
            return print("Malformed.")

    while True:
        # curr_string.insert(tape_pos, tape_state)
        symbol_at_pos = curr_string[tape_pos]

        curr_string[tape_pos] = transitions[tape_state][symbol_at_pos][1]
        if transitions[tape_state][symbol_at_pos][2] == "R":

            tape_pos += 1
            if tape_pos == len(curr_string):
                curr_string.append("_")

        elif transitions[tape_state][symbol_at_pos][2] == "L":

            tape_pos -= 1
            if curr_string[-1] == "_" and tape_pos == len(curr_string) - 2:
                curr_string.pop()

        tape_state = transitions[tape_state][symbol_at_pos][0]

        if tape_state == accept:
            return print("Accepted!")

        if tape_state == reject:
            return print("Rejected.")


# hard-coded idea to make sure I'm not smooth-brained
'''start = "A"
states = ["A", "B"]
input_alphabet = ["a", "b"]
tape_alphabet = ["a", "b", "_"]

transitions = {"A": {"a": ("B", "a", "R"), "b": ("E", "b", "L")}}'''

transitions_lhs = []
transitions_rhs = []
transitions = {}

STATES = []
INPUT_ALPHABET = []
TAPE_ALPHABET = []

start_state = ""
accept_state = ""
reject_state = ""

with open(filename) as f:
    STATES = f.readline().strip().split(",")
    INPUT_ALPHABET = f.readline().strip().split(",")
    TAPE_ALPHABET = f.readline().strip().split(",")

    line = f.readline().strip()

    while "->" in line:
        parts = line.split("->")
        lhs = parts[0]
        rhs = parts[1]
        lhs = re.sub("[()]", "", lhs)
        lhs = lhs.split(",")
        rhs = re.sub("[()]", "", rhs)
        rhs = rhs.split(",")

        lhs = tuple(lhs)
        rhs = tuple(rhs)

        transitions_lhs.append(lhs)
        transitions_rhs.append(rhs)

        line = f.readline().strip()

    f.seek(0, 0)
    lines = f.readlines()
    start_state = lines[-3].strip()
    accept_state = lines[-2].strip()
    reject_state = lines[-1].strip()

for count, i in enumerate(transitions_lhs):
    transitions[i[0]] = {}

for count, i in enumerate(transitions_lhs):
    transitions[i[0]][i[1]] = transitions_rhs[count]

# transitions["A"]["a"] = "(B,a,R)"

tape_string = [c for c in given_string]

# print(transitions)

if mode == "non-verbose":
    transitionNV(tape_string, start_state, accept_state, reject_state, 0)
elif mode == "verbose":
    transitionV(tape_string, start_state, accept_state, reject_state, 0)
