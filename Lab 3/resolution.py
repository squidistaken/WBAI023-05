#!/usr/bin/python


class Clause:
    """
    A class for clauses. A clause consists of a list of positive and negative symbols.
    """

    def __init__(self, clause):
        self.positive = []
        self.negative = []

        self.make_clause(clause)

    def make_clause(self, clause):
        """
        Parses a clause given as a string
        :param clause: The clause to be parsed as a string
        """
        idx = 0
        clause = ''.join(clause.split())

        while idx < len(clause):
            if clause[idx] == '~':
                idx += 1
                assert clause[idx].isalpha() and clause[
                    idx].islower(), "Invalid symbol. A symbol must be a single lowercase letter"
                self.negative.append(clause[idx])
                idx += 1
            elif clause[idx] == ',':
                idx += 1
                assert idx < len(clause), "Syntax error: truncated clause"
            else:
                assert clause[idx].isalpha() and clause[
                    idx].islower(), "Invalid symbol. A symbol must be a single lowercase letter"
                self.positive.append(clause[idx])
                idx += 1

    def copy_clause(self, clause):
        """
        Copies the contents of the input clause to this clause
        :param clause: The clause to be copied into this clause
        """
        self.positive = clause.positive
        self.negative = clause.negative

    def print_clause(self):
        """
        Prints a single clause
        """
        all_symbols = sorted(self.positive + self.negative)
        # The duplicate flag is used to deal with terms that occur both in the positive and negative sets
        # This occurs when two clauses are resolved with multiple complementary literals
        duplicate = False

        print("[", end='')

        if len(all_symbols) == 0:
            print("]=FALSE", end="")
        else:
            for symbol in all_symbols[:-1]:
                if not duplicate and symbol in self.negative:
                    if symbol in self.positive:
                        duplicate = True

                    symbol = "~" + symbol
                else:
                    duplicate = False

                print(symbol, end=',')

            symbol = all_symbols[-1]
            if not duplicate and symbol in self.negative:
                symbol = "~" + symbol

            print(symbol, end='')

            print("]", end='')

    def equals(self, clause):
        """
        Check if this clause equals the clause passed to this method
        :param clause: The clause to compare to this clause
        """
        # Sort the positive and negative symbol lists in both clauses (alphabetically). If both lists equal the
        # corresponding lists in the other clause, the clauses are equal
        if sorted(clause.positive) == sorted(self.positive) and sorted(clause.negative) == sorted(self.negative):
            return True

        return False


def print_clause_set(clause_set):
    """
    Prints a clause set
    :param clause_set: The clause set to be printed
    """
    print("{", end='')

    for clause in clause_set[:-1]:
        clause.print_clause()
        print(",", end=' ')

    clause_set[-1].print_clause()

    print("}")


def find_index_of_clause(clause, clause_set):
    """
    Finds the index of the given clause in the given clause set.
    Returns False if the clause is not in the clause set
    :param clause: The clause we want to find the index of
    :param clause_set: The clause set to search in
    :return: Either the index of the clause set or False if the clause is not in the clause set
    """
    for element in clause_set:
        if clause.equals(element):
            return clause_set.index(element)

    return False


def is_element_of_clause_set(clause, clause_set):
    """
    Checks if the given clause is an element in the given clause set
    :param clause: The clause to find
    :param clause_set: The clause set to search in
    :return: True if clause is in clause_set, otherwise false
    """
    for element in clause_set:
        if clause.equals(element):
            return True

    return False


def contains_empty_clause(clause_set):
    """
    Checks if the empty clause is an element in the clause set
    :param clause_set: The clause set to search in
    :return: True if the empty clause is in clause_set, otherwise False
    """
    empty = Clause("")
    if is_element_of_clause_set(empty, clause_set):
        return True

    return False


def is_clause_subset(clause_set1, clause_set2):
    """
    Checks whether clause_set1 is a subset of clause_set2
    :param clause_set1: The first clause set
    :param clause_set2: The second clause set
    :return: True if clause_set1 is a subset of clause_set2, otherwise False
    """
    # If there is clause in the first set that is NOT an element in the second set,
    # the first clause set is not a subset of the second set
    for clause in clause_set1:
        if not is_element_of_clause_set(clause, clause_set2):
            return False

    return True


def union_of_clause_sets(clause_set1, clause_set2):
    """
    Returns the union of two clause sets
    :param clause_set1: The first clause set
    :param clause_set2: The second clause set
    :return: The union of clause_set1 and clause_set2
    """
    for clause in clause_set2:
        if not is_element_of_clause_set(clause, clause_set1):
            clause_set1.append(clause)

    return clause_set1


# Main program

def resolve_clauses(clause1, clause2):
    """
    Returns the clause made from the resolvents of clause1 and clause2
    :param clause1: The first clause
    :param clause2: The second clause
    :return: The resolvent of clause1 and clause2. Returns the empty clause if there is none
    """
    resolvent = Clause("")

    # Find all complementary literals by taking the atoms that are both in clause1's set of positive literals and
    # clause2 negative literals, plus the atoms that are both in clause1's negative literals and clause2's set of
    # positive literals
    complements = [atom for atom in clause1.positive if atom in clause2.negative] + [atom for atom in clause1.negative
                                                                                     if atom in clause2.positive]

    # Sort the complementary literals alphabetically
    complements = sorted(complements)

    resolvent.positive = clause1.positive + clause2.positive
    resolvent.negative = clause1.negative + clause2.negative

    # We only resolve one pair of complementary literals
    if complements[0] in resolvent.positive:
        resolvent.positive.remove(complements[0])
    if complements[0] in resolvent.negative:
        resolvent.negative.remove(complements[0])

    # Remove duplicate literals by converting to a set and then back to a list
    resolvent.positive = list(set(resolvent.positive))
    resolvent.negative = list(set(resolvent.negative))

    return resolvent


def can_resolve(clause1, clause2):
    """
    Check whether resolution can be applied to two clauses. It only makes sense to apply resolution if there is
    at least one negation in clause2 of a symbol in clause1, or vice versa
    :param clause1: The first clause
    :param clause2: The second clause
    :return: True if it's useful to apply resolution, otherwise False
    """
    return bool(set(clause1.positive).intersection(set(clause2.negative))) or bool(
        set(clause2.positive).intersection(set(clause1.negative)))


def resolution(kb):
    """
    Extends the kb with rules that can be inferred by resolution.
    The function returns, as soon as it inferred the empty
    clause (i.e. false). The function also returns, if all possible
    resolvents have been computed.
    :param kb: The knowledge base to be extended
    :return: The extended knowledge base
    """
    while not contains_empty_clause(kb):
        inferred = []

        # Loop through all clauses in the kb and compare each clause to all following clauses
        for i in range(len(kb)):
            for j in range(i + 1, len(kb)):
                # Only apply resolution when there's at least one negation in one set of a symbol in the other set
                if can_resolve(kb[i], kb[j]):
                    resolvent = resolve_clauses(kb[i], kb[j])
                    inferred.append(resolvent)

        # If the set of inferred clauses is a subset of the knowledge base (i.e. all clauses are already in the kb),
        # no new clauses can be inferred
        if (is_clause_subset(inferred, kb)):
            break

        # Add the inferred clauses to the knowledge base
        kb = union_of_clause_sets(kb, inferred)

    return kb


def init():
    kb = []
    # Example input: [a,~b],[a,b,~c,~d],[b,c,e], KB=[[a,~b],[a,b,~c,~d],[b,c,e]]
    kb_standard_input = str(input())
    kb_clause = ""
    idx = 0
    
    # Read input and create clauses for the Knowledge Base
    # Example: KB=[[~a,~b],[a,~b,~c,~d],[b,~d],[c,~d],[d]]
    while idx < len(kb_standard_input):
        # These characters are of no importance, so we skip them
        if kb_standard_input[idx].isupper() or kb_standard_input[idx] in "=,]":
            idx += 1
        
        elif kb_standard_input[idx] == "[":
            # Start of a clause
            if kb_standard_input[idx + 1] != "[":
                idx += 1
                # Loop until we find a closing bracket, signaling the end of a clause in the input
                while kb_standard_input[idx] != "]":
                    # We add every letter in the clause to a placeholder string
                    kb_clause += kb_standard_input[idx]
                    idx += 1
                # Append and reset the string
                kb.append(Clause(kb_clause))
                kb_clause = ""
            else:
                idx += 1

    return kb


##
# It should not be necessary to change any code above this line!
##

def define_str(current, parent1, parent2):
    current.print_clause()
    print(" is inferred from", end=" ")
    parent1.print_clause()
    print(" and", end=" ")
    parent2.print_clause()
    print("\n", end="")


def recursive_print_proof(idx, clause_set, parent_group_list=None):
    if not parent_group_list:
        parent_group_list = []
    current_clause = clause_set[idx]
    parent_clause = Clause("")
    found = False

    for i in range(len(clause_set)):
        if found:
            break
        for j in range(i + 1, len(clause_set)):
            # Only apply resolution when there's at least one negation in one set of a symbol in the other set
            if can_resolve(clause_set[i], clause_set[j]):
                resolvent = resolve_clauses(clause_set[i], clause_set[j])
                if current_clause.equals(resolvent):
                    parent_clause = clause_set[j]
                    found = True
                    parent_group_list.append((current_clause, clause_set[i], clause_set[j]))
                    break

    # Base case: No
    if not found:
        for _ in range(len(parent_group_list)):
            cur, p1, p2 = parent_group_list.pop()
            define_str(cur, p1, p2)
        return
    
    idx = find_index_of_clause(parent_clause, clause_set)
    recursive_print_proof(idx, clause_set, parent_group_list)


def print_proof(clause_set):
    empty_clause = Clause("")
    idx = find_index_of_clause(empty_clause, clause_set)
    recursive_print_proof(idx, clause_set)


def main():
    kb = init()

    print("KB= ")
    print_clause_set(kb)

    kb = resolution(kb)

    print("KB after resolution= ")
    print_clause_set(kb)

    if contains_empty_clause(kb):
        print("Resolution proof completed.")
        print("\nProof:")
        print_proof(kb)
    else:
        print("Resolution proof failed")


if __name__ == "__main__":
    main()
