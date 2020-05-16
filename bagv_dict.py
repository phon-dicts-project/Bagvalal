from bs4 import BeautifulSoup as bs
import re

language = 'Bagvalal'
glottolog = 'bagv1239'
reference = 'Magomedova 2004' 
contributor = 'A. Davidenko'

romanic = ['I', 'II', 'III']
input_file = 'bagv_dict.html'
output_file = 'bagv_dict.csv'
dict_beginning = 521
dict_ending = 8265
header = 'id\tlanguage\tglottolog\treference\tlemma_source\tending\tpos\tborrowing\tdialect\ttranslation_ru\tcontributor\tsource\n'

dialect_list = ['(гим.)', '(кван.)', '(тлиб.)', '(тлис.)', '(тлон.)', '(гим)', '(кван)', '(тлиб)', '(тлис)', '(тлон)', '(кван., гим.)']

def preprocessing(text):
    text = text.replace('<sup>Н</sup>', 'ᴴ')
    text = text.replace('<sup>н</sup>', 'ᴴ')
    text = text.replace('<sup>1</sup>', '¹')
    text = text.replace('<sup>2</sup>', '²')
    text = text.replace('<sup>2</sup>', '³')
    return text

def replacing(text):
    if text[0] == '²':
        text = text.replace('²', 'Э´')
    text = text.replace('/²', '/Э´')
    text = text.replace('\n', ' ')
    text = text.replace('¯', '̄')
    text = text.replace('A', 'А')
    text = text.replace('Ā', 'Ā')
    text = text.replace('À', 'Á')
    text = text.replace('ä', 'Б̄')
    text = text.replace('μ', 'У´')
    text = text.replace('ЕÁ', 'Л̄Á')
    text = text.replace('ЕÊ', 'Л̄Á̄')
    text = text.replace('E', 'Е')
    text = text.replace('X', 'Х')
    text = text.replace('R', 'И´')
    text = text.replace('Ç', 'О´')
    text = text.replace('N', 'X̄')
    text = text.replace('Ð', 'С̄Ī')
    text = text.replace('Æ', 'Ē')
    text = text.replace('∙', 'У´')
    text = text.replace('Z', 'Ӯ')
    text = text.replace('ã', 'М̄')
    text = text.replace('ÁI', 'ÁЛ̄Ъ̄')
    text = text.replace('АI', 'АЛ̄Ъ̄')
    text = text.replace('ç', 'Д̄')
    text = text.replace(' /', '/')
    text = text.replace('/ ', '/')
    text = text.replace(' :', ':')
    text = text.replace(': ', ':')
    text = text.replace(' )', ')')
    text = text.replace('( ', '(')
    return text

def not_lemma_replacing(text):
    text = text.replace('B', 'с̄')
    text = text.replace('S', 'ӣ')
    text = text.replace('F', 'л̄')
    text = text.replace('†', '́а̄')    
    text = text.replace('Н', 'л̄ъ̄')
    text = text.replace('Þ', 'н̄')
    text = text.replace('}', 'е́̄')
    return(text)

with open(input_file, 'r', encoding='utf-8') as f: 
    text = f.read()

text = preprocessing(text)

soup = bs(text,'html.parser')
lines = soup.find_all('p')

output = open(output_file, 'w', encoding='utf-8')
output.write(header)
print('Header is done!')
out_id = 0

i = dict_beginning
while i < dict_ending + 1:
    lemma_source = ''
    pos = ''
    borrowing = ''
    translation_ru = ''
    dialect = ''
    text = replacing(lines[i].get_text())
        
    regBrackets = re.compile('\(.+?\)')
    brackets = regBrackets.findall(text)
    if len(brackets) > 0:
        if brackets[0] in dialect_list:
            dialect = brackets[0]
            text = text.replace(dialect, '')
        else:
            ending = brackets[0]
            text = text.replace(ending, '')
            ending = not_lemma_replacing(ending)
                    
    splitted_text = text.split()
    if len(splitted_text) > 1:
        lemma_source = splitted_text[0]
        text = text.replace (splitted_text[0], '')
        if splitted_text[1] in romanic:
            pos = 'noun ' + splitted_text[1]
            text = text.replace (splitted_text[1], '')
        translation_ru = not_lemma_replacing(text)
        print(lemma_source)
        str_line = str(lines[i]).replace('\n', ' ')
        output_line = str(i) + '\t' + language + '\t' + glottolog + '\t' + reference + '\t' + lemma_source + '\t' + ending + '\t' + pos + '\t' + borrowing + '\t' + dialect + '\t' + translation_ru + '\t' + contributor + '\t' + str_line + '\n'
        output.write (output_line)
        print('writing to csv ', i)
    i +=1

output.close()
