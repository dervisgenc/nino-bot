import requests
import time

headers = {
    "authority": "kepler-beta.itu.edu.tr",
    "method": "POST",
    "path": "/api/ders-kayit/v21",
    "scheme": "https",
    "accept": "application/json, text/plain, */*",
    # Your Authorization token here
    "authorization": "",
    "origin": "https://kepler-beta.itu.edu.tr",
    "referer": "https://kepler-beta.itu.edu.tr/ogrenci/DersKayitIslemleri/DersKayit",

}

payload = {
    "ECRN": [
        # Crns to added
    ],
    "SCRN": [
        # Crns to deleted
    ]
}
while True:
    response = requests.post(
        "https://kepler-beta.itu.edu.tr/api/ders-kayit/v21", headers=headers, json=payload)
    # print(response.status_code)
    # print(response.text)
    time.sleep(10)
