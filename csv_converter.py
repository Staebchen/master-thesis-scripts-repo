import os
from ODSReader import ODSReader as ods
from tkinter.filedialog import askopenfilename


def col_conv(letter="a"):
    conv_dict = {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
        "e": 5,
        "f": 6,
        "g": 7,
        "h": 8,
        "i": 9,
        "j": 10,
        "k": 11,
        "l": 12,
        "m": 13,
        "n": 14,
        "o": 15,
        "p": 16,
        "q": 17,
        "r": 18,
        "s": 19,
        "t": 20,
        "u": 21,
        "v": 22,
        "w": 23,
        "x": 24,
        "y": 25,
        "z": 26
    }

    # if column is 1 letter
    if len(letter) == 1:
        # return the equivalent number, but 0 based
        return conv_dict[letter] - 1

    # if the column is longer than 1 letter
    else:
        # make list from string
        let_list = list(letter)
        # set base num
        num = 0
        # for how many items are in list
        for i in range(len(let_list)):
            # convert first letter to number
            item = conv_dict[let_list[0]]
            # add number to num, but times 26 to the power of stringleghth - 1
            num += item * (26 ** (len(let_list) - 1))
            # remove first letter from list
            let_list.pop(0)

        # return num as 0 based number
        return num - 1


def get_col(ask="Select column:\n"):
    while True:
        try:
            col = col_conv(input(ask))
            return col
        except Exception:
            print("Incorrect format! Try again.")


def create_csv_line(col_a=1, col_b=2, col_list=[], iterator=0, replaced=".", replacee=",", separator=";"):
    try:
        value_a = str(col_list[iterator][col_a]).split()[0].replace(replaced, replacee)
    except IndexError:
        value_a = None
    try:
        value_b = str(col_list[iterator][col_b]).split()[0].replace(replaced, replacee)
    except IndexError:
        value_b = None
    return value_a+separator+value_b


if __name__ == "__main__":
    # set current directory as default
    directory = os.getcwd()

    # get column 1
    col1 = get_col("Select independent variable column:\n")
    print(col1)
    # get column 2
    col2 = get_col("Select dependent variable column:\n")
    print(col2)

    # filter column
    while True:
        fil = input("Filter column? (Enter to skip)\n")
        fil_words = []
        if fil == "":
            break
        else:
            try:
                fil = col_conv(fil)
                temp = input("Please enter included values (comma separated):\n").replace(" ", "").split(",")
                for item in temp:
                    fil_words.append(item)
                print(fil_words)
                break
            except Exception:
                print("Incorrect format! Try again.")

    # select instances file
    doc = ods(directory+"\\instances.ods", True)
    sheet = doc.getSheet("Otfried")

    # define number of data points
    while True:
        data_num = input("How many data points? (enter to skip)\n")
        if data_num != "":
            try:
                data_num = int(data_num)
                break
            except ValueError:
                print("Incorrect format! Try again.")
        else:
            data_num = len(sheet)
            break

    # get name of final file
    name = input("Name of output file: ")

    # convert line by line array to column by column array
    with open(directory+"\\rscript\\"+name+".csv", mode="w", encoding="UTF-8") as f:
        f.write("indep;dep\n")
        for i in range(len(sheet)):
            # skip the first line
            if i == 0:
                pass
            elif i <= data_num:
                if fil == "":
                    # write all other lines as needed
                    line = create_csv_line(col1, col2, sheet, iterator=i)
                    f.write(line+"\n")
                else:
                    # write lines where the filter word is present in the filter column
                    for j in fil_words:
                        if j == sheet[i][fil]:
                            line = create_csv_line(col1, col2, sheet, iterator=i)
                            f.write(line+"\n")