from lxml import html
import re
import redis
import requests

phrase_dict = {}

def remove_punc(line):
    return line.replace('\r', ' ').replace('\n', ' ').replace('\t',' ').replace('"', ' ')

def cleanup(script):
    lines = []
    for line in script:
        line = remove_punc(line)
        line_list = re.split('-', line)
        for new in line_list:
            if ':' in new or '[' in new:
                pass
            else:
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

def add_to_redis():
    redis_conn = redis.Redis()
    for key, value in phrase_dict.iteritems():
        for word in value:
            redis_conn.sadd('-'.join(key), word)


def parse_data():
    with open('trailer_park.txt', 'r') as f:
        urls = f.readlines()

    for url in urls:
        url = url.replace('\n', '')
        webpage = requests.get(url)
        tree = html.fromstring(webpage.text)

        # print webpage.text
        script_container = tree.xpath('//div[@class="episode_script"]')
        script = tree.xpath('//div[@class="scrolling-script-container"]/text()')
        script = cleanup(script)

        three_base_chain(script)


    add_to_redis()

if __name__ == '__main__':
    parse_data()
