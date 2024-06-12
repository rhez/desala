import random, sys

def get_lines(path):
    L = []
    with open(path) as f:
        # Reads each line in f as an element to add to a list
        for line in f:
            if len(line.strip()) > 0:
                L.append(line)
    return L

def get_quote(lines):
    if len(lines) > 0:
        return random.choice(lines)
    else:
        return ""

if __name__ == '__main__':
    # Read a text, add each line as an element to a list, choose a random element from the list
    lines = get_lines(sys.argv[1])
    print(get_quote(lines))