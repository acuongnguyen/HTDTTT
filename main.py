import random
from itertools import permutations
import os
import csv
import nltk
import itertools
import numpy as np

directory_path = 'D:\HTTT\HTDTTT\data\data'  # Đường dẫn tới thư mục chứa dữ liệu
def get_user_input():   # Hàm lấy dữ liệu từ bàn phím
    words = input("Nhập các từ rời rạc cách nhau bằng dấu phẩy: ")
    word_list = words.split(", ")
    return word_list

def initialize_individual():    # Hàm khởi tạo một cá thể ngẫu nhiên
    return ' '.join(random.sample(input, len(input)))

def generate_word_permutations():  # Hàm sinh hoán vị cho từng từ trong câu
    word_permutations = list(permutations(input))
    return word_permutations

def read_word_csv(file_path):    # Hàm để đọc dữ liệu từ file CSV và trả về set các từ
    words = set()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            words.update(row)
    return words
def validate_input(input, classified_words):
    if len(input) < 2 or len(input) > 8:
        return False, "Số lượng từ phải từ 2 đến 8."
    for word in input:
        if word not in classified_words or not classified_words[word]:
            return False, "Dữ liệu không có trong hệ thống."
    return True, ""

while True:
    user_input = get_user_input()
    population_size = 6

    # Bắt đầu xét các từ vừa nhập
    word_types = {    # Tạo một từ điển với tên của các loại từ và đường dẫn đến file từ điển
        'NN': os.path.join(directory_path, 'noun.com.csv'),
        'NNP': os.path.join(directory_path, 'noun.diff.csv'),
        'VB': os.path.join(directory_path, 'verb.csv'),
        'JJ': os.path.join(directory_path, 'adj.csv'),
        'RB': os.path.join(directory_path, 'adv.csv'),
        'C': os.path.join(directory_path, 'conj.csv'),
        'PRP': os.path.join(directory_path, 'pron.csv'),
        'IN': os.path.join(directory_path, 'prep.csv'),
        'UN': os.path.join(directory_path, 'noun.quantity.csv'),
        'CD': os.path.join(directory_path, 'cd.csv'),
    }
    word_dict = {word_type: read_word_csv(file_path) for word_type, file_path in word_types.items()}

    # Phân loại từng từ
    classified_words = {word: [] for word in user_input}
    for word in user_input:
        for word_type, word_set in word_dict.items():
            if word in word_set:
                classified_words[word].append(word_type)

    # Kiểm tra dữ liệu nhập
    validation_result, message = validate_input(user_input, classified_words)
    if not validation_result:
        print(message)
        continue
    for word, types in classified_words.items():
        print(f"Từ '{word}' thuộc loại: {', '.join(types) if types else 'không xác định'}")

    grammar_rules = []
    for word_type, words in word_dict.items():
        rules = ' | '.join([f"'{word}'" for word in words])
        grammar_rules.append(f"{word_type} -> {rules}")

    #tập luật
    grammar_string = "\n".join([
            "S -> NP VP",
            "NP -> NN UN | UN NN | NN NN | CD NN | NNP | PRP | CD NP  | CD NP ADJP | NP ADJP",
            "VP -> VB | VB NVP  | RB VB NN | C NVP | VB NN | NN | RB VB NVP | RB VB | VB INN",
            "NVP -> UN NN | VB VP | NN JJ | CD NN | CD NVP",
            "INN -> IN NN",
            "ADJP -> RB JJ",
            "ADJP -> JJ",
            *grammar_rules
        ])

    grammar_string_2= "\n".join([
            "S -> NP VP",
            "NP -> NUN | UNN | NNN | CD NN | NNP | PRP | NP RB JJ",
            "VP -> VB | VB NVP | VB INN | RB VB UNN | RB VB NVP | C NVP | VB NN | NN | ADJP VB",
            "NVP -> UN NN | VB VP | NN JJ | CD NN | CD NVP | RB JJ | NNN ADJP | NNN JJ ADJP | NNN | CD UNN",
            "NNN -> NN NN",
            "INN -> IN NN",
            "NUN -> NN UN",
            "UNN -> UN NN",
            "ADJP -> RB JJ",
            "ADJP -> JJ",
            *grammar_rules
        ])

    grammar = nltk.CFG.fromstring(grammar_string)
    grammar_2 = nltk.CFG.fromstring(grammar_string_2)

        # Hàm sinh hoán vị của các từ
    def generate_word_permutations():
        return list(itertools.permutations(user_input))

    # Hàm khởi tạo cá thể cho giải thuật di truyền (ví dụ)
    def initialize_individual():
            # Cá thể có thể là một hoán vị ngẫu nhiên của các từ
        return list(np.random.permutation(user_input))

        #hàm fitness
    def evaluate_sentence_fitness(sentence, grammar):
            parser = nltk.ChartParser(grammar)
            tokens = nltk.word_tokenize(sentence)
            
            try:
                # Parse the sentence based on the defined grammar
                trees = parser.parse(tokens)
                
                # If no parse errors occur, the sentence is considered grammatically correct
                for tree in trees:
                    return True
                
            except nltk.ParseError:
                # If there's a parse error, the sentence is not grammatically correct
                return False

    sentences = []
    if len(user_input) <= 5:
            permutations = generate_word_permutations()
            print("Các hoán vị của từng từ:")
            for idx, perm in enumerate(permutations, 1):
                sentence = ' '.join(perm)
                print(sentence)
                if evaluate_sentence_fitness(sentence, grammar):
                    print(f"Câu hợp lệ: {sentence}")
                    sentences.append(sentence)
                    break
    else:
            population_size = 10  # Giả sử kích thước quần thể
            valid_sentences_count = 0  # Đếm số lượng câu hợp lệ
            max_valid_sentences = 1  # Số lượng câu hợp lệ cần tìm

            while valid_sentences_count < max_valid_sentences:
                population = [initialize_individual() for _ in range(population_size)]
                for individual in population:
                    sentence = ' '.join(individual)
                    print(sentence)
                    if evaluate_sentence_fitness(sentence, grammar_2):
                        print(f"Cá thể hợp lệ: {sentence}")
                        sentences.append(sentence)
                        valid_sentences_count += 1
                        if valid_sentences_count == max_valid_sentences:
                            break  # Đã tìm thấy đủ câu hợp lệ, thoát vòng lặp

            print(f"Đã tìm thấy {max_valid_sentences} câu hợp lệ.")
    break