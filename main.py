#Logic AI - Petros Chatzitoulousis
import random

KB = []


def constructKB():

    var_num = input("Enter the number of Logical Variables (1-26): ")
    var_num = int(var_num)
    while (var_num < 1) or (var_num > 26):
        var_num = input("Try again! Enter a number between 1 and 26: ")
        var_num = int(var_num)

    lit_num = input("Enter the number of Literals: ")
    lit_num = int(lit_num)
    while (lit_num < 1) or (lit_num > var_num):
        lit_num = input("Try again! Enter a number greater that 0: ")
        lit_num = int(lit_num)

    sent_num = input("Enter the number of Sentences: ")
    sent_num = int(sent_num)
    while sent_num < 1:
        sent_num = input("Try again! Enter a number greater that 0: ")
        sent_num = int(sent_num)

    sent_counter = 0
    while sent_counter < sent_num:

        var_list = []
        for letter in range(97, 97+var_num):
            var_list.append(chr(letter))

        sent = []

        lit_rand = random.randint(1, lit_num)
        for k in range(lit_rand):

            lit = random.choice(var_list)
            var_list.remove(lit)

            negative_possibility = random.choice([0, 1])
            if negative_possibility == 1:
                lit += "'"

            sent.append(lit)

        if sent not in KB:
            KB.append(sent)
            sent_counter += 1

    for s in KB:
        print(*s)

    f = open("demofile3.txt", "w")
    f.write("Number of Logical Variables: " + str(var_num) + " | Number of Sentences: " + str(sent_num) + " | Max Literals in each Sentence: " + str(lit_num))
    f.close()







if __name__ == '__main__':
    constructKB()
