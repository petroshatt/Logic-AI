# Logic AI - Chatzitoulousis Petros, Giannakoulas Giorgos
import random
import copy
from itertools import combinations

f = open("kb.txt", "w", encoding="utf-8")


# Dhmiourgei tyxaia thn vash gnwshs me vash tis parametrous pou dinei o xrhsths.
def construct_kb():

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

    print("\nKnowledge Base successfully created!\nNumber of Logical Variables: " + str(var_num) + "\nNumber of Sentences: " + str(sent_num) + "\nMax Literals in each Sentence: " + str(lit_num) + "\n\n")

    f.write("Number of Logical Variables: " + str(var_num) + " | Number of Sentences: " + str(sent_num) + " | Max Literals in each Sentence: " + str(lit_num) + "\n\nKnowledge Base:\n\n")
    for s in kb:
        s = str(s).replace("[", "").replace("'", "").replace("]", "").replace(",", "").replace(" ", " ∨ ")
        f.write(s + "\n")
    f.close()

    return kb, var_used


# O algorithmos tou GSAT me orismata ton megisto arithmo flips kai epanekkinhsewn.
# Oso megalwnei to provlhma toso pio dyskola vriskei lysh kathws kai ayxanetai kai
# o xronos ekteleshs tou.
def gsat(KB, var_used, maxTries, maxFlips):

    var_values = {}

    for i in range(maxTries):

        for lit in var_used:
            var_values[lit] = random.choice([True,False])

        print("Var Values: ", var_values)

        current_solution = solve(KB, var_values)
        #print("CURR SOL: ", current_solution)
        current_cost = len(current_solution) - sum(current_solution)  # counts False
        # print("Current: ", current_cost)

        for j in range(maxFlips):

            print("Current: ", current_cost)

            if current_cost == 0:
                print("Proved entailment using GSAT!")
                return True

            else:

                key_to_change = find_key_to_change(KB, var_values)
                #print(key_to_change)
                var_values[key_to_change] = not(var_values[key_to_change])
                print("New Var Values: ", var_values)
                new_solution = solve(KB, var_values)
                #print("NEW SOL: ", new_solution)
                new_cost = len(new_solution) - sum(new_solution)  # counts False
                print("New: ", new_cost)

                if current_cost <= new_cost:
                    #print("OKOKOK")
                    var_values[key_to_change] = not(var_values[key_to_change])
                else:
                    current_cost = new_cost

    print("Could not prove entailment using GSAT.")
    return False


# Epistrefei th metavlhth h opoia tha epiferei thn megalyterh meiwsh twn False.
def find_key_to_change(KB, var_values):

    temp_var_values = copy.deepcopy(var_values)
    new_costs = {}

    for key in var_values:
        temp_var_values[key] = not(temp_var_values[key])
        temp_solution = solve(KB, temp_var_values)
        new_costs[key] = len(temp_solution) - sum(temp_solution)  # counts False
        temp_var_values[key] = not(temp_var_values[key])

    key_to_change = random.choice([k for k,v in new_costs.items() if v == min(new_costs.values())])
    return key_to_change


# Lynei
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

    return solution


def resolution(KB):

    clauses = copy.deepcopy(KB)
    new = []
    result = []

    while True:

        clauses_comb = combinations(clauses, 2)

        for i,j in clauses_comb:
            x_found = []
            y_found = []
            for x in i:
                for y in j:
                    if x == find_negative(y):
                        if y not in y_found:
                            y_found.append(y)
                        if x not in x_found:
                            x_found.append(x)

            new_x = []
            for x1 in i:
                if x1 not in x_found:
                    new_x.append(x1)

            new_y = []
            for y1 in j:
                if y1 not in y_found:
                    new_y.append(y1)

            result.append("Clause 1: " + str(i))
            result.append("Clause 2: " + str(j))
            result.append("New Clause 1: " + str(new_x))
            result.append("New Clause 2: " + str(new_y) + "\n")

            if not new_x and not new_y:
                print("Proved entailment using Resolution!\nCheck the txt file for the results.\n")
                with open('kb.txt', 'a') as f:
                    f.write("\n\n--------------------------------------\n\n\nResolution Procedure:\n\n")
                    for s in result:
                        f.write(str(s) + "\n")
                    f.close()
                return True

            if new_x:
                if new_x not in new:
                    new.append(new_x)
            if new_y:
                if new_y not in new:
                    new.append(new_y)

        if all(x in clauses for x in new):
            print("Could not prove entailment using Resolution.\nNo results are available at the txt file.\n")
            return False

        if new:
            for n1 in new:
                clauses.append(n1)
            result.append("New Set of Clauses: " + str(list(clauses)) + "\n")


def find_negative(char):

    if "-" in char:
        return char.replace("-", "")
    else:
        return "-" + char


def literal_input(KB):

    entail_check_str = input("\nEnter the literal for entailment check (use '-' for negativity): ")
    entail_check_str = find_negative(entail_check_str)

    entail_check = []
    entail_check.append(entail_check_str)
    KB.append(entail_check)


if __name__ == '__main__':

    KB_basic, var_used = construct_kb()

    continue_flag = "Y"
    while continue_flag == "Y":

        KB = copy.deepcopy(KB_basic)
        literal_input(KB)

        # Prints the knowledge base
        for s in KB:
            print(s)

        if not gsat(KB, var_used, 100, 100):
            resolution(KB)

        continue_flag = input("\nWould you like to check another literal? (Y/N): ")
        while continue_flag != "Y" and continue_flag != "N":
            continue_flag = input("Enter an acceptable value! (Y/N): ")


