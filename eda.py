# Easy data augmentation techniques for text classification
# Jason Wei and Kai Zou

import random
from random import shuffle
from pyhanlp import *
from ciLin import CilinSimilarity

random.seed(1)

#stop words list
stop_words = set()

def stopword_init():
    stopwords_file = '哈工大停用词表.txt'
    with open(stopwords_file, 'r') as f:
        for line in f.readlines():
            stop_words.add(line.strip())

    stopwords_file = '百度停用词表.txt'
    with open(stopwords_file, 'r') as f:
        for line in f.readlines():
            stop_words.add(line.strip())

    print("已经初始化停用词表词个数: ", len(stop_words))

stopword_init()
synonym_handler =  CilinSimilarity()

def get_segment(line):
    HanLP.Config.ShowTermNature = False
    StandardTokenizer = JClass("com.hankcs.hanlp.tokenizer.StandardTokenizer")
    segment_list = StandardTokenizer.segment(line)
    terms_list = []
    for terms in segment_list :
        terms_list.append(str(terms))
    return terms_list

########################################################################
# Synonym replacement
# Replace n words in the sentence with synonyms from wordnet
########################################################################


def synonym_replacement(words, n):
    new_words = words.copy()
    random_word_list = list(set([word for word in words if word not in stop_words]))
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        synonyms = get_synonyms(random_word)
        if len(synonyms) >= 1:
            synonym = random.choice(list(synonyms))
            new_words = [synonym if word == random_word else word for word in new_words]
            #print("replaced", random_word, "with", synonym)
            num_replaced += 1
        if num_replaced >= n: #only replace up to n words
            break

    #this is stupid but we need it, trust me
    sentence = ' '.join(new_words)
    new_words = sentence.split(' ')

    return new_words

def get_synonyms(word):
    synonyms = set()
    if word not in synonym_handler.vocab:
        print(word, '未被词林词林收录！')
    else:
        codes = synonym_handler.word_code[word]
        for code in codes:
            key = synonym_handler.code_word[code]
            synonyms.update(key)
        if word in synonyms:
            synonyms.remove(word)

    return list(synonyms)

########################################################################
# Random deletion
# Randomly delete words from the sentence with probability p
########################################################################

def random_deletion(words, p):

    #obviously, if there's only one word, don't delete it
    if len(words) == 1:
        return words

    #randomly delete words with probability p
    new_words = []
    for word in words:
        r = random.uniform(0, 1)
        if r > p:
            new_words.append(word)

    #if you end up deleting all words, just return a random word
    if len(new_words) == 0:
        rand_int = random.randint(0, len(words)-1)
        return [words[rand_int]]

    return new_words

########################################################################
# Random swap
# Randomly swap two words in the sentence n times
########################################################################

def random_swap(words, n):
    new_words = words.copy()
    for _ in range(n):
        new_words = swap_word(new_words)
    return new_words

def swap_word(new_words):
    random_idx_1 = random.randint(0, len(new_words)-1)
    random_idx_2 = random_idx_1
    counter = 0
    while random_idx_2 == random_idx_1:
        random_idx_2 = random.randint(0, len(new_words)-1)
        counter += 1
        if counter > 3:
            return new_words
    new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1] 
    return new_words

########################################################################
# Random insertion
# Randomly insert n words into the sentence
########################################################################

def random_insertion(words, n):
    new_words = words.copy()
    for _ in range(n):
        add_word(new_words)
    return new_words

def add_word(new_words):
    synonyms = []
    counter = 0
    while len(synonyms) < 1:
        random_word = new_words[random.randint(0, len(new_words)-1)]
        synonyms = get_synonyms(random_word)
        counter += 1
        if counter >= 10:
            return
    random_synonym = synonyms[0]
    random_idx = random.randint(0, len(new_words)-1)
    new_words.insert(random_idx, random_synonym)

########################################################################
# main data augmentation function
########################################################################

def eda(sentence, alpha_sr=0.1, alpha_ri=0.1, alpha_rs=0.1, p_rd=0.1, num_aug=9):

    words = get_segment(sentence)

    num_words = len(words)

    augmented_sentences = []
    num_new_per_technique = int(num_aug/4)+1
    n_sr = max(1, int(alpha_sr*num_words))
    n_ri = max(1, int(alpha_ri*num_words))
    n_rs = max(1, int(alpha_rs*num_words))

    #sr
    for _ in range(num_new_per_technique):
        a_words = synonym_replacement(words, n_sr)
        augmented_sentences.append(''.join(a_words))

    #ri
    for _ in range(num_new_per_technique):
        a_words = random_insertion(words, n_ri)
        augmented_sentences.append(''.join(a_words))

    #rs
    for _ in range(num_new_per_technique):
        a_words = random_swap(words, n_rs)
        augmented_sentences.append(''.join(a_words))

    #rd
    for _ in range(num_new_per_technique):
        a_words = random_deletion(words, p_rd)
        augmented_sentences.append(''.join(a_words))

    augmented_sentences = [get_segment(sentence) for sentence in augmented_sentences]

    shuffle(augmented_sentences)



    #trim so that we have the desired number of augmented sentences
    if num_aug >= 1:
        augmented_sentences = augmented_sentences[:num_aug]
    else:
        keep_prob = num_aug / len(augmented_sentences)
        augmented_sentences = [s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]

    augmented_sentences = [''.join(sentence) for sentence in augmented_sentences]
    #append the original sentence
    augmented_sentences.append(sentence)

    return list(set(augmented_sentences))

