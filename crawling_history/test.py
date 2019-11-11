from googletrans import Translator

# Translator function
def kor_2_en(input_word_list):
    word_list_result = []
    translator = Translator()
    for input_word in input_word_list:
        print(translator.detect(input_word))
        if translator.detect(input_word) == 'ko':
            word_list_result.append(translator(input_word))
        elif input_word.src == 'en':
            word_list_result.append(input_word)
        else:
            pass
    
    return word_list_result

result = kor_2_en(['파이썬'])

print(result)