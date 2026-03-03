import os
from tkinter.filedialog import askopenfilename

# set current directory as default
directory = os.getcwd()

# pronouns (beginning of)
pro = ["ih", "íh", "iz", "íz", "z", "h", "s"]
# how many lines are already filled
add = 0
case = "acc"


def sanitize(string):
    # remove newline, sanitize quotations & strip leading and following spaces
    new_string = string.replace("\n", "").replace("\"", "\\\"").replace("¦", " ").strip(" ")
    # new_string = new_string.replace("í", "i")
    # new_string = new_string.replace("Í", "I")
    return new_string


# select file
filename = askopenfilename(initialdir=directory)

# create list
file = []
try:
    with open(filename, mode="r", encoding="UTF-8") as f:
        temp = ""
        for line in f:
            if len(line) > 4:
                temp = temp + sanitize(line)
            else:
                if len(temp) > 1:
                    file.append(temp.split("\t"))
                temp = ""
except FileNotFoundError:
    print("file not found")

# # remove duplicates
# file1 = []
# throwaway = []
# index_list = []
# for i in range(len(file)):
#     try:
#         item = file.pop(0)  # take a line
#         if item[2].split(" ")[4] in file[0][2].split(" ")[4]:       # if the last word before the target word match
#             if item[4] in file[0][4] and item[-1] in file[0][-1]:   # and chapter and verse also match
#                 throwaway.append(item)                              # remove item (add to throwaway)
#             else:
#                 file1.append(item)                                  # else add to new list
#         else:
#             file1.append(item)                                      # ditto
#     except IndexError:
#         pass
#
# file = file1    # replace old (empty) list with new list

# create output file
with open(directory + "/out.txt", mode="w", encoding="UTF-8") as o:
    # o.write("order\tprecont\ttarget\tpostcont\tcase\tprepos\tpostpos\tbook\tchapter\tverse(s)\tspecial\n")    # header
    for i in range(len(file)):
        line = "" + file[i][0][:-1] + "\t"  # add number without period
        special = ""

        # get the target, precont & postcont
        if file[i][2].split(" ")[6].lower() in pro:
            target = file[i][2].split(" ")[6]
            precont = [file[i][2].split(" ")[j] for j in (1, 2, 3, 4, 5)]    # get precont
            postcont = [file[i][2].split(" ")[j] for j in (7, 8, 9, 10, 11)]         # get postcont
        elif file[i][2].split(" ")[-6].lower() in pro:
            special += "E!"               # mark issue in edition
            target = file[i][2].split(" ")[-6]
            precont = [file[i][2].split(" ")[j] for j in (-11, -10, -9, -8, -7)]    # get precont
            postcont = [file[i][2].split(" ")[j] for j in (-5, -4, -3, -2, -1)]         # get postcont
        elif file[i][2].split(" ")[-5].lower() in pro:
            special += "E!"               # mark issue in edition
            special += "T!"               # mark issue in text
            target = file[i][2].split(" ")[-5]
            precont = [file[i][2].split(" ")[j] for j in (-10, -9, -8, -7, -6)]    # get precont
            postcont = [file[i][2].split(" ")[j] for j in (-4, -3, -2, -1)]         # get postcont
        elif file[i][2].split(" ")[-7].lower() in pro:
            special += "E!"               # mark issue in edition
            special += "T!"               # mark issue in text
            target = file[i][2].split(" ")[-7]
            precont = [file[i][2].split(" ")[j] for j in (-12, -11, -10, -9, -8)]    # get precont
            postcont = [file[i][2].split(" ")[j] for j in (-6, -5, -4, -3, -2, -1)]         # get postcont
        else:
            special += "E!"               # mark issue in edition
            special += "T!!!"               # mark issue in text
            target = file[i][2].split(" ")[-6]
            precont = [file[i][2].split(" ")[j] for j in (-11, -10, -9, -8, -7)]    # get precont
            postcont = [file[i][2].split(" ")[j] for j in (-5, -4, -3, -2, -1)]         # get postcont

        # add them together
        line += " ".join(precont) + "\t"        # precontext
        line += target + "\t"                   # target word
        line += " ".join(postcont) + "\t"       # postcontext

        line += case + "\t"                     # case

        # add pos of last precont word & pos of first postcont word
        # three options are given, depending on if the postcont happens to contain fewer (or more) than 5 elements
        if file[i][-1].split(" ")[-6] == "PPER":       # if PPER is sixth latest
            line += file[i][-1].split(" ")[-7] + "\t"   # add precont pos
            line += file[i][-1].split(" ")[-5] + "\t"   # add postcont pos
        elif file[i][-1].split(" ")[-5] == "PPER":       # if PPER is fifth latest
            line += file[i][-1].split(" ")[-6] + "\t"   # add precont pos
            line += file[i][-1].split(" ")[-4] + "\t"   # add postcont pos
        elif file[i][-1].split(" ")[-4] == "PPER":       # if PPER is seventh latest
            line += file[i][-1].split(" ")[-5] + "\t"   # add precont pos
            line += file[i][-1].split(" ")[-3] + "\t"   # add postcont pos
        elif file[i][-1].split(" ")[-3] == "PPER":       # if PPER is seventh latest
            line += file[i][-1].split(" ")[-4] + "\t"   # add precont pos
            line += file[i][-1].split(" ")[-2] + "\t"   # add postcont pos
        elif file[i][-1].split(" ")[-7] == "PPER":       # if PPER is seventh latest
            line += file[i][-1].split(" ")[-8] + "\t"   # add precont pos
            line += file[i][-1].split(" ")[-6] + "\t"   # add postcont pos
        else:
            line += file[i][-1].split(" ")[-7] + "???\t"   # add precont pos
            line += file[i][-1].split(" ")[-5] + "???\t"   # add postcont pos

        line += "" + "\t"                       # book, left empty
        
        if file[i][3] == "chapter":             # if chapter is present
            line += file[i][4].strip().split(" ")[0] + "\t"       # add chapter
        else:
            line += "N/A\t"                         # else: add N/A
        verse = file[i][-3].strip().split(" ")[0]      # first element of verse
        try:
            verse = str(int(verse))
        except:                        # if it is not a number
            verse = file[i][-3].strip().split(" ")[-1]  # add last element of verse
        line += verse + "\t"      # verse

        # ne += special           # special

        # final line break
        line += "\n"

        # write to file
        o.write(line)
