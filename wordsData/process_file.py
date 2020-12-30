#!/usr/bin/env python
# -*- coding: utf8 -*-

def readFileContent(filename):
    
    content_dictionary = {}
    print("readFileContent {}".format(readFileContent))
    with open(filename, 'r', encoding='utf-8') as reader:
  
        for line in reader.readlines():
            print(line)
            words = line.split()
            
            if len(words) > 2:
                print("Error line contains more than 2 words: {}".format(words))
                continue
            
            content_dictionary[words[0]] = words[1]

    return content_dictionary


def main():
    file = "D:\Programming\DjangoProjects\Words\words\wordsData\wordsEnglish.txt"
    words = readFileContent(file)
    print("Result word")
    print(words)