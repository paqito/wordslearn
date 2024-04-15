#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
    Module to parse any file containing english words and optionally its meanings
    ProcessFileFactory - creates necessary parser for file type
    Returns: dictionary of words
'''

import os

# from utilities import translate_utility

class ProcessFileFactory():
    fileName = None

    def __init__(self, fileName):
        self.fileName = fileName

    def factory(fileName):
        filename, extension = os.path.splitext(fileName)
        if (extension == ".txt"):
            return ProcessFileTxt(fileName)
        elif (extension == ".csv"):
            return ProcessFileCsv(fileName)
        else:
            print("Error: Unable to find process file factory for file {}".format(self.fileName))
            return None


class ProcessFile():
    fileName = None

    def __init__(self, fileName):
        self.fileName = fileName

    def process_file(self):
        pass


class ProcessFileTxt(ProcessFile):

    def process_file(self):
        content_dictionary = {}
        print("readFileContent {}".format(self.fileName))

        with open(self.fileName, 'r', encoding='utf-8') as reader:

            for line in reader.readlines():
                # print(line)
                words = line.split()

                if len(words) > 2:
                    print("Warning line contains more than 2 words skipping: {}".format(words))
                    separator = " "
                    #content_dictionary[words[0]] = separator.join(words[1:])
                    continue
                elif len(words) == 2:
                    # world and its translation
                    content_dictionary[words[0]] = words[1]
                elif len(words) == 1:
                    # world without translation
                    content_dictionary[words[0]] = ""
                elif len(words) == 0:
                    continue
                    #print("Warning empty line")
                else:
                    print("Warning incorrect line content: {}".format(words))

        return content_dictionary


class ProcessFileCsv(ProcessFile):

    def process_file(self):
        print("ProcessFileCsv")
        print("readFileContent {}".format(self.fileName))
        content_dictionary = {}

        return content_dictionary


def readFileContent(filename):
    print("readFileContent {}".format(filename))
    wordReader = ProcessFileFactory.factory(filename)
    content_dictionary = wordReader.process_file()
    return content_dictionary


def main():
    #file = "D:\Programming\DjangoProjects\Words\words\wordsData\wordsEnglish.txt"
    file = r"D:\Programming\DjangoProjects\Words\words\wordsData\test_words.txt"
    # wordReader = ProcessFileFactory.factory(file)
    # words = wordReader.process_file()
    words = readFileContent(file)
    print("Result words:")
    print(words)


if __name__ == "__main__":
    main()
