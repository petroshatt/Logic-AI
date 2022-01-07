#Logic AI - Petros Chatzitoulousis
import random


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

    f = open("kb.txt", "w")
    f.write("Number of Logical Variables: " + str(var_num) + " | Number of Sentences: " + str(sent_num) + " | Max Literals in each Sentence: " + str(lit_num) + "\n")
    for s in kb:
        s = str(s).replace("[", "").replace("'", "").replace("]", "").replace(",", "").replace(" ", " ∨ ")
        f.write(s + "\n")
    f.close()

    return kb, var_used


def GSAT(KB, var_used):#, maxTries, maxFlips):

    var_values = {}

    # for i in range(maxTries):

    for lit in var_used:
        var_values[lit] = random.choice([True,False])

    print(var_values)
    print(KB)

    current_solution = solve(KB, var_values)
    print(current_solution)
    current_cost = 0
    for i in current_solution:
        if not i:
            current_cost+=1
    #current_cost = sum(not(current_solution))
    #current_cost = sum(1 for v in var_values.values() if v == False) #counts the Falses

    # for j in range(maxFlips):

    temp_var_values = var_values
    new_costs = {}

    if all(current_solution):   #na ginei satisfies
        return var_values

    else:
        for key in var_values:
            temp_var_values[key] = not(temp_var_values[key])
            temp_solution = solve(KB, temp_var_values)
            print(temp_solution)
            new_costs[key] = 0
            for i in temp_solution:
                if not i:
                    new_costs[key] += 1
            temp_var_values = var_values
        print(new_costs)


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

    GSAT(KB, var_used)

    # for s in KB:
    #     print(s)
