# Function to eliminate left recursion from a given grammar
def eliminate_left_recursion(grammar):
    # Get a sorted list of nonterminals in the grammar
    keys = sorted(list(grammar.keys()))
    # Iterate over each nonterminal in the grammar
    for i, Ai in enumerate(keys):
        new_rules = []
        # Iterate over each rule for the current nonterminal
        for rule in grammar[Ai]:
            # Check for left recursion with previous nonterminals
            for j, Aj in enumerate(keys):
                if j < i and rule.startswith(Aj):
                    # Eliminate left recursion by replacing the rule
                    # with rules from the previous nonterminal
                    for Aj_rule in grammar[Aj]:
                        new_rules.append(Aj_rule + rule[len(Aj):])
                    break
            else:
                # No left recursion, so keep the rule as is
                new_rules.append(rule)
        # Eliminate immediate left recursion among the Ai rules
        grammar[Ai] = eliminate_immediate_left_recursion(Ai, new_rules)
    return grammar

# Function to eliminate immediate left recursion from a list of rules
def eliminate_immediate_left_recursion(A, rules):
    # Separate the rules into recursive and non-recursive lists
    recursive = []
    non_recursive = []
    for rule in rules:
        if rule.startswith(A):
            recursive.append(rule[len(A):])
        else:
            non_recursive.append(rule)

    # If there is no left recursion, return the original rules
    if not recursive:
        return rules

    # Replace the original rules with a new set of rules
    new_A = A + "'"
    new_rules = [rule + new_A for rule in non_recursive] + [new_A + rule + " | " + "ε" for rule in recursive]
    return new_rules

# Function to parse a grammar from a string
def parse_grammar(input_str):
    grammar = {}
    for line in input_str.strip().split('\n'):
        key, rules = line.split('->')
        key = key.strip()
        rules = rules.strip().split('|')
        grammar[key] = rules
    return grammar

# Function to print a grammar
def print_grammar(grammar):
    for key in sorted(grammar.keys()):
        print(key, ' –>', ' | '.join(grammar[key]))

# Main program
if __name__ == "__main__":
    input_str = """T->T*F|F"""
    grammar = parse_grammar(input_str)
    new_grammar = eliminate_left_recursion(grammar)
    print("After elimination of left recursion the grammar is:")
    print_grammar(new_grammar)