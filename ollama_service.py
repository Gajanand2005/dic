import requests

def get_meaning(word):
    
    prompt = f"""
        Explain the meaning of '{word}'in Hindi.
        
        Give :
        1. Hindi meaning
        2. simple explanation
        3. one example  sentence
        
    """
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    
    data =response.json()
    return data['response']