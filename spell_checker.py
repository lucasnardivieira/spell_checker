import nltk


def separete_words(tokens):
  word_list = []
  for token in tokens:
    if token.isalpha():
      word_list.append(token)
    else:
      continue
  return word_list

def normalize_words(list):
  word_list = []
  for word in list:
    word_list.append(word.lower())
  return word_list

def generate_word(word):
  slices = []
  for i in range(len(word) + 1):
    slices.append((word[:i], word[i:]))
  new_words = insert_letter(slices)
  new_words += delete_character(slices)
  new_words += change_character(slices)
  new_words += change_pos(slices)
  return new_words

def insert_letter(slices):
  new_words = []
  letters = "abcdefghijklmnopqrstuvwxyzáàãâéèêíìîóòõôúùûç"
  for l_slice, r_slice in slices:
    for letter in letters:
      new_words.append( l_slice + letter + r_slice)
  return new_words


def probability(generated_word):
    freq = nltk.FreqDist(word_list)
    word_count = len(word_list)
    return freq[generated_word]/word_count

def create_test_data(file):
  test_words = []
  f = open(file, "r", encoding="utf8")
  for line in f:
    right_word, wrong_word = line.split()
    test_words.append((right_word, wrong_word))
  f.close()
  return test_words

def validate_corrector():
    test_words = create_test_data("palavras.txt")
    number_test_words = len(test_words)
    got_right = 0
    for right_word, wrong_word in test_words: 
        corrected_word = corrector(wrong_word)
        if corrected_word == right_word:
            got_right += 1
    hit_rate = round(got_right * 100/number_test_words, 2)
    print(f'{hit_rate}% de palavras corrigidas a partir de {number_test_words} palavras')

def delete_character(slices):
    new_words = []
    for l_slice, r_slice in slices:
        new_words.append(l_slice + r_slice[1:])
    return new_words

def change_character(slices):
    new_words = []
    letters = "abcdefghijklmnopqrstuvwxyzáàãâéèêíìîóòõôúùûç"
    for l_slice, r_slice in slices:
        for letter in letters:
            new_words.append(l_slice + letter + r_slice[1:])
    return new_words

def change_pos(slices):
    new_words = []
    for l_slice, r_slice in slices:
        if len(r_slice) > 1:
            new_words.append(l_slice + r_slice[1] + r_slice[0] + r_slice[2:])
    return new_words

def corrector(word):
    generated_words = generate_word(word)
    right_word = max(generated_words, key = probability)
    return right_word

with open("artigos.txt", "r", encoding="utf8") as file:
    print('lendo artigo')
    artigos = file.read()

tokens = nltk.tokenize.word_tokenize(artigos)
word_list = separete_words(tokens)
word_list = normalize_words(word_list)
