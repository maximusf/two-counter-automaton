#!/usr/bin/env python3

# Maximus Fernandez

"""
2-CA Interpreter for CSCE 355, Spring 2026.

Reads a 2-counter automaton description from a file (given as a command-line
argument), then reads input strings from stdin and simulates the 2-CA on
each one, printing the computation trace and ACCEPT/REJECT.

To run, use:
    python3 my_interpreter.py <2ca_file> < <input_file>
"""

import sys # for command-line args and stdin
import re # for parsing lines with regex

# Set to True to print debug info (transition table, step-by-step trace details).
# Debug output goes to stderr so it won't interfere with stdout even if left on, but turn it off to be safe.
# Must be False for grading
DEBUG = False


def debug(msg):
    """
    Print a debug message to stderr if DEBUG is enabled.
    Using stderr so debug output never mixes with graded stdout.
    Takes: msg (str) - the message to print.
    Returns: nothing.
    """
    if DEBUG:
        print(f"[DEBUG] {msg}", file=sys.stderr)


def sign(n):
    """
    Return the sign character for a counter value.
    This maps a counter's numeric value to the condition symbol
    used in the transition table lookup.
    Takes: n (int) - a counter value (>= 0).
    Returns: '=' if n is zero, '>' if n is positive.
    """
    return '=' if n == 0 else '>'


def apply_action(counter, action):
    """
    Apply a counter action and return the new counter value.
    Decrementing at zero is safe - it just stays at zero (no error).
    This behavior is important for semibalanced.txt.
    Takes: counter (int) - current counter value (>= 0).
           action (str) - one of '+' (increment), 
                                 '=' (unchanged), 
                                 '-' (decrement).
    Returns: (int) the new counter value, floored at 0.
    """
    if action == '+':
        return counter + 1
    elif action == '-':
        return max(0, counter - 1)
    else:
        # action == '=', leave unchanged
        return counter


def parse_line(line):
    """
    Parse a single line from the 2-CA file into transition entries.

    Handles comment stripping, whitespace removal, and wildcard (*) expansion.
    A wildcard in a counter condition expands to both '=' and '>', so one
    line with two wildcards produces up to 4 transition entries.

    Takes: line (str) - a raw line from the 2-CA file.
    Returns: list of tuples, each being (key, value) where
             key = (from_state, symbol, c1_cond, c2_cond)
             value = (to_state, c1_action, c2_action)
             Returns an empty list if the line is blank or a comment.
    """
    # Strip comments - everything from '//' onward
    comment_idx = line.find('//')
    if comment_idx != -1:
        line = line[:comment_idx]

    # Strip ALL spaces and tabs to simplify parsing
    line = line.replace(' ', '').replace('\t', '')

    # Skip empty lines after stripping
    if not line:
        return []

    # Match the transition format:
    # (from_state,symbol?,c1_cond,c2_cond)->(to_state,c1_action,c2_action)
    #
    # The symbol field can be empty (epsilon transition) or a single char
    # After whitespace stripping, commas delimit fields unambiguously
    # because the symbol is at most 1 character and cannot contain commas.
    pattern = r'\(([^,]*),([^,]*),([^,]*),([^,]*)\)->\(([^,]*),([^,]*),([^,]*)\)'
    m = re.match(pattern, line)
    if not m:
        debug(f"Failed to parse line: {line}")
        return [] # skip malformed lines (ideally should not happen)

    from_state = m.group(1) # state label to transition from
    symbol = m.group(2)     # single char or '' for epsilon
    c1_cond = m.group(3)    # '=', '>', or '*'
    c2_cond = m.group(4)    # '=', '>', or '*'
    to_state = m.group(5)   # state label to transition to
    c1_action = m.group(6)  # '+', '=', or '-'
    c2_action = m.group(7)  # '+', '=', or '-'

    # Expand wildcards: '*' means both '=' and '>'
    # This creates a list of possible conditions for each counter, 
    # which we will combine to produce all transition entries
    c1_options = ['=', '>'] if c1_cond == '*' else [c1_cond]
    c2_options = ['=', '>'] if c2_cond == '*' else [c2_cond]

    # Build all combinations from wildcard expansion
    entries = []
    # For example, if c1_cond is '*' and c2_cond is '=', we get:
    # c1_options = ['=', '>']
    # c2_options = ['=']
    for c1 in c1_options:
        for c2 in c2_options:
            key = (from_state, symbol, c1, c2)
            value = (to_state, c1_action, c2_action)
            entries.append((key, value))

    return entries # list of (key, value) tuples to add to the transition table


def parse_file(path):
    """
    Read the 2-CA description file and build the transition table

    Takes: path (str) - path to the .txt file describing the 2-CA
    Returns: dict mapping 
            (from_state, symbol, c1_cond, c2_cond)
            to 
            (to_state, c1_action, c2_action)
    """
    delta = {} # the transition table

    # Read the file line by line, parse each line into transition entries,
    # and add them to the delta dictionary. The parse_line function handles
    # comment stripping, whitespace removal, and wildcard expansion.
    with open(path, 'r') as f:
        for line in f:
            entries = parse_line(line)
            for key, value in entries:
                delta[key] = value

    # Print debug information about the parsed transitions (if DEBUG is enabled)
    debug(f"Parsed {len(delta)} transitions:")
    if DEBUG:
        for key, value in sorted(delta.items()):
            state, sym, c1, c2 = key
            to_state, a1, a2 = value
            sym_display = sym if sym else 'eps'
            debug(f"  ({state}, {sym_display}, {c1}, {c2}) -> ({to_state}, {a1}, {a2})")

    return delta # the completed transition table dictionary


def format_id(state, input, c1, c2):
    """
    Format a configuration (ID) as a string for output.
    The format matches what the reference executable produces:
    state,remaining_input,counter1,counter2

    Takes: state (str) - current state label.
           input (str) - remaining input string.
           c1 (int) - counter 1 value.
           c2 (int) - counter 2 value.
    Returns: (str) formatted ID like "#,aabb,0,0".
    """
    return f"{state},{input},{c1},{c2}"


def simulate(delta, input):
    """
    Simulate the 2-CA on a single input string.

    Prints the full computation trace (one ID per line) followed by
    ACCEPT or REJECT. Uses the greedy rule: non-epsilon transitions
    always take priority over epsilon transitions.

    Takes: delta (dict) - the transition table from parse_file().
           input (str) - the input string to simulate on.
    Returns: nothing (output goes to stdout).
    """
    state = '#'
    c1 = 0
    c2 = 0

    debug(f"--- Simulating on input: '{input}' ---")

    while True:
        # Print the current configuration
        print(format_id(state, input, c1, c2))

        s1 = sign(c1)
        s2 = sign(c2)
        moved = False

        # Greedy rule: try consuming an input symbol first
        if input:
            key = (state, input[0], s1, s2)
            if key in delta:
                to_state, a1, a2 = delta[key]
                debug(f"  Non-eps transition: ({state},{input[0]},{s1},{s2}) -> ({to_state},{a1},{a2})")
                state = to_state
                input = input[1:]  # consume the symbol
                c1 = apply_action(c1, a1)
                c2 = apply_action(c2, a2)
                moved = True

        # If no non-epsilon transition was taken, try epsilon
        if not moved:
            key = (state, '', s1, s2)
            if key in delta:
                to_state, a1, a2 = delta[key]
                debug(f"  Eps transition: ({state},eps,{s1},{s2}) -> ({to_state},{a1},{a2})")
                state = to_state
                # No symbol consumed for epsilon transitions
                c1 = apply_action(c1, a1)
                c2 = apply_action(c2, a2)
                moved = True

        # No transition available - computation halts
        if not moved:
            debug(f"  No transition available, halting.")
            break

    # Acceptance: input fully consumed AND both counters are zero
    # This is the same acceptance condition as the reference executable, and
    # is emphasized in the BB announcement. It is NOT just reaching a halting state.
    if input == '' and c1 == 0 and c2 == 0:
        debug(f"  Result: ACCEPT (input empty, c1={c1}, c2={c2})")
        print("----ACCEPT")
    else:
        debug(f"  Result: REJECT (input='{input}', c1={c1}, c2={c2})")
        print("----REJECT")


def main():
    """
    Main entry point. Reads the 2-CA file from the command line argument,
    then reads input strings from stdin one at a time and simulates
    the 2-CA on each.
    """
    # The 2-CA file path is the first (and only) command-line argument
    if len(sys.argv) < 2:
        print("Usage: python3 my_interpreter.py <2ca_file>", file=sys.stderr)
        sys.exit(1)

    ca_file = sys.argv[1] # the .txt file describing the 2-CA
    debug(f"Loading 2-CA from: {ca_file}") # debug info about which file is being loaded

    # Phase 1: Parse the 2-CA description
    delta = parse_file(ca_file)

    # Phase 2 + 3: Read input strings and simulate each one
    # sys.stdin gives us lines until EOF (Ctrl-D from keyboard, or end of piped file)
    for line in sys.stdin:
        # Strip the trailing newline from the input line.
        # The input string itself might be empty (just a newline), 
        # which represents the empty string epsilon.
        input = line.rstrip('\n').rstrip('\r')
        simulate(delta, input)

    # Print one extra newline at the end as emphasized on BB announcement
    print()


if __name__ == '__main__':
    main()
