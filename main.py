#Logic AI - Petros Chatzitoulousis
import random
import copy


def constructKB():

    kb = []

    var_num = int(input("Enter the number of Logical Variables (1-26): "))
    while (var_num < 1) or (var_num > 26):
        var_num = int(input("Try again! Enter a number between 1 and 26: "))

    lit_num = int(input("Enter the number of Literals: "))
    while (lit_num < 1) or (lit_num > var_num):
        lit_num = int(input("Try again! Enter a number greater that 0: "))

    sent_num = int(input("Enter the number of Sentences: "))
    while sent_num < 1:
        sent_num = int(input("Try again! Enter a number greater that 0: "))

    sent_counter = 0
    var_used = []
    while sent_counter < sent_num:

        var_list = []
        for letter in range(97, 97+var_num):
            var_list.append(chr(letter))

        sent = []

        lit_rand = random.randint(1, lit_num)
        for k in range(lit_rand):

            lit = random.choice(var_list)
            var_list.remove(lit)
            if lit not in var_used:
                var_used.append(lit)
                var_used.sort()

            negative_possibility = random.choice([0, 1])
            if negative_possibility == 1:
                lit = "-" + lit

            sent.append(lit)

        if sent not in kb:
            kb.append(sent)
            sent_counter += 1

    print("\nKnowledge Base succesfully created!\nNumber of Logical Variables: " + str(var_num) + "\nNumber of Sentences: " + str(sent_num) + "\nMax Literals in each Sentence: " + str(lit_num) + "\n")

    f = open("kb.txt", "w", encoding="utf-8")
    f.write("Number of Logical Variables: " + str(var_num) + " | Number of Sentences: " + str(sent_num) + " | Max Literals in each Sentence: " + str(lit_num) + "\n")
    for s in kb:
        s = str(s).replace("[", "").replace("'", "").replace("]", "").replace(",", "").replace(" ", " ∨ ")
        f.write(s + "\n")
    f.close()

    return kb, var_used


def GSAT(KB, var_used, maxTries, maxFlips):

    var_values = {}

    for i in range(maxTries):

        if i%10 == 0:
            print(i)

        for lit in var_used:
            var_values[lit] = random.choice([True,False])

        # print(var_values)
        # print(KB)

        current_solution = solve(KB, var_values)
        # print("original: ", current_solution)
        current_cost = len(current_solution) - sum(current_solution) #counts Falses

        for j in range(maxFlips):

            if all(current_solution):   #na ginei satisfies
                print("Solution Found!")
                return var_values

            else:
                key_to_change = findKeyToChange(KB, var_values)
                var_values[key_to_change] = not(var_values[key_to_change])
                #print(var_values)

    print("Solution NOT Found!")


def findKeyToChange(KB, var_values):

    temp_var_values = copy.deepcopy(var_values)
    new_costs = {}

    for key in var_values:
        temp_var_values[key] = not(temp_var_values[key])
        temp_solution = solve(KB, temp_var_values)
        #print(temp_solution)
        new_costs[key] = len(temp_solution) - sum(temp_solution) #counts Falses
        temp_var_values = copy.deepcopy(var_values)

    key_to_change = random.choice([k for k,v in new_costs.items() if v == min(new_costs.values())]) #na ginei random
    #print(key_to_change)
    return(key_to_change)


def solve(KB, var_values):

    convert_to_true_false = []
    for lists in KB:
        x = [None] * len(lists)
        convert_to_true_false.append(x)

    for key in var_values:
        for lists in KB:
            list_index = KB.index(lists)
            for ch in lists:
                char_index = lists.index(ch)
                if key in ch:
                    if len(ch) == 1:
                        convert_to_true_false[list_index][char_index] = (var_values[key])
                    elif len(ch) == 2:
                        convert_to_true_false[list_index][char_index] = (not var_values[key])

    solution = []
    for lists in convert_to_true_false:
        res = any(lists)
        solution.append(res)

    return(solution)


if __name__ == '__main__':

    KB, var_used = constructKB()

    #input("Enter the literal for entailment check (use '-' for negativity): ")

    GSAT(KB, var_used, 100, 100)

    # for s in KB:
    #     print(s)
