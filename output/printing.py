import defaults

def printing(string):
    if defaults.do_print_to_txt == True:
        file = open("output\cs_analysis.txt", "a+")
        file.write(string)
        file.close()
    if defaults.do_print_to_terminal == True:
        print(string, end = "")
