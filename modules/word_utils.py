import requests

def is_real_word(word: str) -> bool:
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # The presence of 'meanings' indicates a valid word
        return bool(data and 'meanings' in data[0])
    return False
