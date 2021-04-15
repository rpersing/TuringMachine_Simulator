import sys
import re

# filename = sys.argv[1]
filename = "wordhashword.tm"
# given_string = sys.argv[2]
given_string = "101#101"


# Ask Stephen for help on this. Clearly you are doing something wrong and do not yet hold the
# knowledge to unlock the door to success
def transitionV(curr_string, tape_state, accept, reject, tape_pos):

    for s in curr_string:
        if s not in INPUT_ALPHABET:
            print("Malformed.")
            exit(0)

    # symbol_at_pos = curr_string[tape_pos]

    while tape_state != reject:

        symbol_at_pos = curr_string[tape_pos]

        if tape_state == accept:
            print("Accepted!")
            exit(0)

        curr_string[tape_pos] = transitions[tape_state][symbol_at_pos][1]
        tape_state = transitions[tape_state][symbol_at_pos][0]
        if transitions[tape_state][symbol_at_pos][2] == "R":
            tape_pos += 1
            if tape_pos >= len(curr_string):
                curr_string.append("_")
        elif transitions[tape_state][symbol_at_pos][2] == "L":
            tape_pos -= 1
            if curr_string[-1] == "_":
                curr_string.pop()

        print(curr_string)

    if tape_state == reject:
        print("Rejected.")


def transitionNV(curr_string, tape_state, accept, reject, tape_pos):

    for s in curr_string:
        if s not in INPUT_ALPHABET:
            print("Malformed.")
            exit(0)

    # symbol_at_pos = curr_string[tape_pos]

    while tape_state != reject:

        symbol_at_pos = curr_string[tape_pos]

        if tape_state == accept:
            print("Accepted!")
            exit(0)

        curr_string[tape_pos] = transitions[tape_state][symbol_at_pos][1]
        tape_state = transitions[tape_state][symbol_at_pos][0]
        if transitions[tape_state][symbol_at_pos][2] == "R":
            tape_pos += 1
            if tape_pos >= len(curr_string):
                curr_string.append("_")
        elif transitions[tape_state][symbol_at_pos][2] == "L":
            tape_pos -= 1
            if curr_string[-1] == "_":
                curr_string.pop()

    if tape_state == reject:
        print("Rejected.")


try:
    mode = sys.argv[3]
except IndexError:
    pass

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
# print(tape_string)
transitionV(tape_string, start_state, accept_state, reject_state, 0)
