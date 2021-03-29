#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import translatorModule

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
        print("ProcessFileTxt")
        content_dictionary = {}
        print("readFileContent {}".format(self.fileName))

        with open(self.fileName, 'r', encoding='utf-8') as reader:

            for line in reader.readlines():
                # print(line)
                words = line.split()

                if len(words) > 2:
                    print("Warning line contains more than 2 words: {}".format(words))
                    separator = " "
                    content_dictionary[words[0]] = separator.join(words[1:])
                    continue
                elif len(words) == 2:
                    content_dictionary[words[0]] = words[1]
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
    file = "D:\Programming\DjangoProjects\Words\words\wordslearn\wordsData\wordsEnglish.txt"
    # wordReader = ProcessFileFactory.factory(file)
    # words = wordReader.process_file()
    words = readFileContent(file)
    print("Result word")
    print(words)


if __name__ == "__main__":
    main()
