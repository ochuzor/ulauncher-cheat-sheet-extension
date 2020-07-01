import re

def get_string_chunks(string_val):
    """
    splits the supplied string by ,.!?;:
    that is, it tries to break supplied string into sentences
    """
    # https://stackoverflow.com/a/9797398
    string_list = re.split('[?.,!;:]', string_val)
    string_list = map(str.strip, string_list)
    return list(filter(len, string_list))

    
rex = re.compile(r"\W+")
def get_normalized_string(string_val):
    """
    returns the supplied string with 
        - spaces colapsed
        - non-word characters like #, &, @, etc removed
        - trailing spaces removed
        - lower-case'd
    """
    return rex.sub(' ', string_val).strip().lower()


def get_digrams(token_list):
    token_count = len(token_list)

    if token_count < 2:
        return []
    if token_count == 2:
        return [" ".join(token_list)]

    digrams = set()
    for index, token in enumerate(token_list):
        if index < (token_count - 1):
            digrams.add(f"{token} {token_list[index + 1]}")

    return list(digrams)


def get_text_words(text):
    """
    splits the text by space into list of words, removing empty strings from the list
    """
    return text.split(' ')


def get_tokens(string_val):
    chunks = get_string_chunks(string_val)
    cleaned_chunks = list(map(chunks, get_normalized_string))

    tokens = set()

    for text_chunk in cleaned_chunks:
        words = get_text_words(text_chunk)
        tokens.update(words)
        tokens.update(get_digrams(words))

    return list(tokens)


def add_token_to_index(index_hash, token_str, id):
    """
    token_str is the token string
    id is the id of the original text in the "db" 
        (i.e the index of the text in the text array)
    index_hash is index hash of the form {token_str: set(1, 2,...)}; 
        1, 2,...are the list of text id's
    """

    if token_str not in index_hash:
        index_hash[token_str] = set()
    
    index_hash[token_str].add(id)

    return index_hash



def add_text_to_index(index_hash, text, id):
    """
    give it a text and a "db" object it adds it to text list o
    then adds its text chunks (search words) into the index hash 
        indexed with the id (the list index) of the newly added text
    db.text_list = the list of the texts untouched
    index_hash = the search index hash
    """

    tokens = get_tokens(text)
    for token in tokens:
        add_token_to_index(index_hash, token, id)

    return index_hash


def create_search_index(text_list):
    """
    pass it a list of '\n'-split texts (e.g. from a text file) 
    and it'll return a search_db object
    """

    index_hash = {}

    for id, text in enumerate(text_list):
        add_text_to_index(index_hash, text, id)

    return index_hash