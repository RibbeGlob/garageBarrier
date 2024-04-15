# Calling with a custom engine configuration
import json
import requests
with open(r"C:\Users\gerfr\Downloads\a4a072777c34b6fb7220ed2527c5.jpeg", 'rb') as fp:
    response = requests.post(
        'https://api.platerecognizer.com/v1/plate-reader/',
        data=dict(regions=['pl'], config=json.dumps(dict(region="strict"))),
        files=dict(upload=fp),
        headers={'Authorization': 'Token 6bf05633011339939e0a8ca7002c6774318c63a6'})

# Sprawdzenie, czy odpowiedź jest pozytywna
if response.status_code == 201:
    # Pobranie danych w formacie JSON
    data = response.json()
    print(data["results"][0]['plate'])
else:
    print("Błąd:", response.status_code)

