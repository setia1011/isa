def url_encode(text):
    import urllib.parse
    return urllib.parse.quote(text) 

def cleaner(text):
    return " ".join(text.split()) 