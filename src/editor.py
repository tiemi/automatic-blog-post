import json

def read_process_dict(process_dict_path):
    with open(process_dict_path, encoding='utf-8') as file:
        process_dict = json.load(file)
    return process_dict

def read_text(post_path):
    with open(post_path, encoding='utf-8') as file:
        lines = file.readlines()
    text = lines[-1]
    return text

def process_text(text, process_dict):
    processed_text = text
    for word in process_dict.keys():
        processed_text = processed_text.replace(word, process_dict[word])
    return processed_text
