import sys
import re

# define the morse's dictionary
morsedictionary = { 'a':'.-' , 'b':'-...' , 'c':'-.-.' , 'd':'-..' , 'e':'.' , 'f':'..-.' , 'g':'--.' , 'h':'....' ,
                    'i':'..' , 'j':'.---' , 'k':'-.-' , 'l':'.-..' , 'm':'--' , 'n':'-.' , 'o':'---' , 'p':'.--.' ,
                    'q':'--.-' , 'r':'.-.' , 's':'...' , 't':'-' , 'u':'..-' , 'v':'...-' , 'w':'.--' , 'x':'-..-' ,
                    'y':'-.--' , 'z':'--..' , '.':'.-.-.-' , ',':'--..--' , '?':'..--..' , '/':'-..-.' , '@':'.--.-.' ,
                    '1':'.----' , '2':'..---' , '3':'...--' , '4':'....-' , '5':'.....' , '6':'-....' , '7':'--...' ,
                    '8':'---..' , '9':'----.' , '0':'-----' , ' ':' ' , '':''}

# define the usage in CLI. Must use 3 parameters
def main():
    if len(sys.argv) != 4:
        print ('    Usage: EnglishMorseTranslator.py <translation type> <source filename> <destination filename>')
        print ('           Translation types : e2m (english to morse) or m2e (morse to english) ')
        print ('')
        sys.exit(1)
    elif (sys.argv[1] == 'e2m'):
        sourcefile = sys.argv[2]
        destfile = sys.argv[3]
        translate_e2m(sourcefile,destfile)
    elif (sys.argv[1] == 'm2e'):
        sourcefile = sys.argv[2]
        destfile = sys.argv[3]
        translate_m2e(sourcefile,destfile)
    else:
        print ('    Wrong options usage.')
        print ('')
        sys.exit(1)

# defines translating english to morse
def translate_e2m(sourcefile,destfile):
    # open the source file
    srcfile = open(sourcefile,'r')

    # search for 2 dots in a row with regex, which is forbidden in this case.
    for line in srcfile:
        pattern1 = re.search(r'^\.\.[$\w\s]', line)
        pattern2 = re.search(r'[\w\s]\.\.[$\w\s]', line)

        #if pattern1 or pattern2 or pattern3 or pattern4 or pattern5 or pattern6:
        if pattern1 or pattern2:
            print ('    The are 2 dots in a row in the source file. Please check again your source file.')
            print('')
            sys.exit(1)

    # reset the file reading to the beginning
    srcfile.seek(0,0)

    # create the output file
    write_to = open(destfile,'w')

    # start the translation process
    for line in srcfile:
        translated_char = []    # prepare the list for morse-converted character

        # searching for pattern of 3 or more dots in each line:
        search_multi_dots = re.search(r'\.\.\.+', line)

        # if multiple dots pattern found, proceed as below:
        if search_multi_dots:
            splitted_letters = []  # prepare the list for each splitted letters
            split_space = line.lower().split()  # split by whitespaces

            for words in split_space:
                split_dot = words.split('.')  # if it's dotted words, split by dot.
                                              # ex: .c.o.d.e. --> ['','c','o','d','e','']

                for i in range(2,len(split_dot)):
                    if split_dot[i - 2] == "" and split_dot[i - 1] == "" and split_dot[i] == "":
                        split_dot[i - 1] = '.'  # put back the dots that have been removed by split('.')

                for each_letters in split_dot:  # if it's normal word, split per letter.
                                                # ex: code --> ['c','o','d','e']
                                                #                |
                    splitted_letters = splitted_letters + list(each_letters)  # accumulate all separated letters

                splitted_letters = splitted_letters + [" "]  # add additional whitespace between each words

            for letters in splitted_letters:  # begin translation for all separated letters
                if (letters != "") and (letters != "\n"):  # filter out null ("") strings and new line strings

                    # translate with dictionary, catch possibility of no translation:
                    translated_char.append(morsedictionary.get(letters, "(No morse translation for "+ letters +")"))
                    translated_char.append(" ")  # append white space for each morse codes, so it'll be easy to read


        # if no multiple dots pattern found, proceed normally as below:
        else:
            splitted_letters = []   # prepare the list for each splitted letters
            split_space = line.lower().split()  # split by whitespaces
            for words in split_space:
                split_dot = words.split('.')    # if it's dotted words, split by dot.
                                                # ex: .c.o.d.e. --> ['','c','o','d','e','']

                for each_letters in split_dot:  # if it's normal word, split per letter.
                                                # ex: code --> ['c','o','d','e']
                                                #                |
                    splitted_letters = splitted_letters + list(each_letters)    #accumulate all separated letters

                splitted_letters = splitted_letters + [" "] # add additional whitespace between each words

            for letters in splitted_letters:    # begin translation for all separated letters
                if (letters != "") and (letters != "\n"):   # filter out null ("") strings and new line strings

                    # translate with dictionary, catch possibility of no translation:
                    translated_char.append(morsedictionary.get(letters,"(No morse translation for "+ letters +")"))
                    translated_char.append(" ") # append white space for each morse codes, so it'll be easy to read

        converted_line = "".join(translated_char)   # convert the List of translated line into single string

        write_to.write(converted_line)  # write that single string into output file
        write_to.write("\n")    # add new line to separate each original line


# defines translating morse to english
def translate_m2e(sourcefile,destfile):
    # open the source file
    srcfile = open(sourcefile,'r')

    # create the output file
    write_to = open(destfile,'w')

    # start the reverse translation process
    for line in srcfile:
        reversed_line = []    # prepare the list for reverse-translated line

        reversed_char = []   # prepare the list for each reverse-translated characters
        split_space = re.split(r'\s{2,}', line)  # split by 2 or more whitespaces, to separate each words

        for word in split_space:
            split_char = word.split()  # split every character inside a word.

            for each_char in split_char:  # for each character inside a word:
                for key in morsedictionary.keys():      # reverse lookup inside morse-dictionary
                    if each_char == morsedictionary[key]:
                        reversed_char.append(key)
                        break

                if key == "":   # if the key is not found during reverse lookup
                    reversed_char.append(" ( '" + each_char + "' is not a valid morse-code.) ")


            reversed_char = reversed_char + [" "]   # add whitespace between words

        reversed_line = reversed_line + reversed_char  # add all reverse-translated words into the line

        joined_reversed_line = "".join(reversed_line)   # convert the List of reverse-translated line into single string

        write_to.write(joined_reversed_line.upper())  # write that uppercased single string into output file
        write_to.write("\n")    # add new line to separate each original line


# start running the program
if __name__ == '__main__':
  main()
