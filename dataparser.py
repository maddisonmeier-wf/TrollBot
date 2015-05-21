from lxml import html
import re
import requests

phrase_dict = {}

def cleanup(script):
    lines = []
    for line in script:
        line = line.replace('-', '').replace('\r', '').replace(',','').replace('\n', '').replace('\t','').replace('.', '!').replace('?','!')
        line_list = re.split('!', line)
        for new in line_list:
            lines.append(new)

    return lines


def three_base_chain(phrases):
    """
    takes in a list of phrases and parses into the three based groupings
    to store into the redis datastore
    """ 
    for phrase in phrases:
        phrase = (phrase + ' <stop>').lower().split()
        phrase_length = len(phrase)
        if phrase_length == 2:
            phrase.append('<stop>')
        for index, word in enumerate(phrase):
            if index < phrase_length - 2 and phrase_length > 2:
                phrase_key = (phrase[index], phrase[index+1])
                if phrase_key in phrase_dict:
                    if phrase[index+2] in phrase_dict[phrase_key]:
                        pass
                    else:
                        a = phrase_dict[phrase_key]
                        b = phrase[index+2]
                        a.append(b)
                        phrase_dict[phrase_key] = a
                else:
                    phrase_dict[phrase_key] = [phrase[index+2]]



with open('trailer_park.txt', 'r') as f:
    urls = f.readlines()

for url in urls:
    webpage = requests.get(url)
    tree = html.fromstring(webpage.text)

    # print webpage.text

    script_container = tree.xpath('//div[@class="episode_script"]')
    script = tree.xpath('//div[@class="scrolling-script-container"]/text()')

    script = cleanup(script)

    three_base_chain(script)

    print phrase_dict


