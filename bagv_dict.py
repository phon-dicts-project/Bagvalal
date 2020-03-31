from bs4 import BeautifulSoup as bs
import re

##Проблемы:
##    Слова делятся по слэшам
##    Слова делятся после акутов (?)
    
##&aacute;
##&ocirc;
##&yacute;
##&eacute;
##&oacute;
##&#256;
##&#257;
##&#268;
##&#274;
##&#275;
##&#332;
##&#333;
##&Iuml;

language = 'Bagvalal'
glottolog = 'bagv1239'
reference = 'Magomedova 2004' 
contributor = 'A. Davidenko'

lemma_ipa = ''
pos = ''
borrowing = ''
translation_ru = ''
translation_en = ''

romanic = ['I', 'II', 'III']
input_file = 'bagv_dict.html'
output_file = 'output.csv'
header = 'id\tlanguage\tglottolog\treference\tlemma_source\tlemma_ipa\tpos\tborrowing\ttranslation_ru\ttranslation_en\tcontributor\n'

with open(input_file, 'r', encoding='utf-8') as f: 
    text = f.read()
    
soup = bs(text,'html.parser')
lines = soup.find_all('p')
output = open(output_file, 'w', encoding='utf-8')
output.write(header)
print('Header is done!')
out_id = 0
errors = 0
for line in lines:
    try:
        lemma_source = ''
        lemma_ipa = ''
        pos = ''
        borrowing = ''
        translation_ru = ''
        translation_en = ''
        text = line.get_text()
        text = text.replace ('\n', ' ')
        text = text.replace ('(', ' (')
        splitted_text = text.split()
        lemma_source = splitted_text[0]
        text = text.replace (splitted_text[0], '')
        if splitted_text[1] in romanic:
            pos = 'noun ' + splitted_text[1]
            text = text.replace (splitted_text[1], '')
        regEnding = re.compile('\(.+?\)')
        endings = regEnding.findall(text)
        if len(endings) > 0:
            ending = endings[0]
            text = text.replace (ending, '')
        translation_ru = text
        output_line = str(out_id) + '\t' + language + '\t' + glottolog + '\t' + reference + '\t' + lemma_source + ' ' + ending + '\t' + lemma_ipa + '\t' + pos + '\t' + borrowing + '\t' + translation_ru + '\t' + translation_en + '\t' + contributor + '\n'
        print (output_line)
        output.write (output_line)
        out_id += 1
    except:
        output_line = str(out_id) + 'ERROR'
        errors += 1
output.close()
print ('Done. Errors: ', errors)
