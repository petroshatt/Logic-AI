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


def GSAT(KB, var_used, maxTries, maxFlips):

    var_values = {}

    for i in range(maxTries):

        for lit in var_used:
            var_values[lit] = random.choice([True,False])

        current_cost = sum(1 for v in var_values.values() if v == False) #counts the Falses

        # for j in range(maxFlips):
        #
        #     if satisfies(var_values, KB):
        #         return var_values
        #
        #     else







if __name__ == '__main__':

    KB, var_used = constructKB()

    GSAT(KB, var_used, 100, 100)

    # for s in KB:
    #     print(*s)
