import random
import redis

from dataparser import remove_punc

max_words = 30
redis_con = redis.Redis()

def analyze_input(phrase):
    message_tuples = []
    phrase = remove_punc(phrase)
    phrase += ' <stop>'
    words = phrase.split()
    length = len(words)
    messages = []
    for i, word in enumerate(words):
        if i < length - 2:
            redis_con.sadd('-'.join([words[i],words[i+1]]), words[i+2])
            message_tuples.append((words[i],words[i+1], words[i+2]))

    for words in message_tuples:
        longest = ''
        for i in range(10):
            gen_message = generate_message([words[0], words[1]])
            if len(gen_message) > len(longest):
                longest = gen_message
        if longest:
            messages.append(longest)

    if len(messages):
        return random.choice(messages)


    

def generate_message(words):
    gen_words = []

    for i in range(max_words):
        gen_words.append(words[0])

        next_word = redis_con.srandmember('-'.join(words))
        if not next_word:
            break

        words = [words[1], next_word]


    return ' '.join(gen_words)




while True:
    user_response = raw_input()

    print analyze_input(user_response)