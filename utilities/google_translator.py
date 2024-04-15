

import os
import json
from googletrans import Translator
from googletrans import Translator as googleTranslator
import httpcore

class GoogleTranslator:
    def __init__(self):
        self.googleTranslator = googleTranslator()
        self.request_count = 0
        self.request_file_name = 'request_count_google.txt'
        self.read_request_count_from_file()
    
    def __del__(self):
        print("GoogleTranslator object destroyed")
        self.save_request_count_to_file()

    def read_request_count_from_file(self):
        if os.path.exists(self.request_file_name):
            with open(self.request_file_name, 'r') as f:
                self.request_count = int(f.read())
        else:
            print("Request count file not found")
            self.request_count = 0

    def save_request_count_to_file(self):
        with open(self.request_file_name, 'w') as f:
            f.write(str(self.request_count))

    def translate(self, word_eng, src='en', dest='pl'):

        print("Translation by GoogleTranslator wEng: {} ".format(word_eng))
        retry_count = 3
        list_of_words = []
        result = None


        while retry_count > 0:
            try:
                result = self.googleTranslator.translate(word_eng, src=src, dest=dest)
                #result = self.googleTranslator.translate(text=str(word_eng), src='en', dest='pl', kwargs=None)
                #result = self.googleTranslator.translate('apple')
                self.request_count = self.request_count + 1

                break
            except json.decoder.JSONDecodeError:
                print("JSONDecodeError Exception found")
                retry_count = retry_count - 1
            except httpcore._exceptions.ReadTimeoutError:
                print("ReadTimeoutError Exception found")
                retry_count = retry_count - 1

        if result:
            print(str(result.text))
        else:
            print("No translation found for {}".format(word_eng))

        return result



def testTranslator():
    translator1 = Translator()
    result = translator1.translate(text="apple", src='en', dest='pl')
    #get word definition from result

    print("Translation of {} is {}".format("apple", result))
    print("extra_data")
    for item in result.extra_data.items():
       print(item)

    print("origin " + str(result.origin))
    print("translation " + str(result.text))
    print("src " + str(result.src))
    print("dest " + str(result.dest))
    print("origin_pronunciation " + str(result.extra_data['origin_pronunciation']))

def main():

    print("Main Running google_translator script")
    translator = GoogleTranslator()
    print("Request count: {}".format(translator.request_count))
    result = translator.translate("apple")
    print("Translation of {} is {}".format("apple", result.text))
    print("Request count: {}".format(translator.request_count))



if __name__ == "__main__":
    main()