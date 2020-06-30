
def get_string_chunks(string_val):
    """
    splits the supplied string by ,.!?;:
    that is, it tries to break supplied string into sentences
    """
    return None

    
def get_normalized_string(string_val):
    """
    returns the supplied string with 
        - spaces colapsed
        - non-word characters like #, &, @, etc removed
        - trailing spaces removed
        - lower-case'd
    """
    return None


def get_ngrams(token_list, size=1):
    return None


def get_text_words(text):
    """
    splits the text by space into list of words, removing empty strings from the list
    """
    pass


def get_tokens(string_val):
    chunks = get_string_chunks(string_val)
    cleaned_chunks = list(map(chunks, get_normalized_string))

    tokens = set()

    for text_chunk in cleaned_chunks:
        words = get_text_words(text_chunk)
        tokens.update(get_ngrams(words, 1))
        tokens.update(get_ngrams(words, 2))

    # return list(tokens)
    return None


def add_token_to_index(index_hash, token_str, id):
    """
    token_str is the token string
    id is the id of the original text in the "db"; the index of the text in the text array
    index_hash is index hash of the form {token_str: [1, 2,...]}; 1, 2,...are the list of text id's
    """
    pass


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

    return None


def create_search_index(text_list):
    """
    pass it a list of '\n'-split texts (e.g. from a text file) and it'll return a search_db object
    """

    index_hash = {}

    for id, text in enumerate(text_list):
        add_text_to_index(index_hash, text, id)

    # return index_hash
    return None