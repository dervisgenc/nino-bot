import requests
from bs4 import BeautifulSoup

# Session başlatılıyor
session = requests.Session()

# İlk GET isteği için headers tanımla
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36"
}

# İlk GET isteği
response = session.get(
    "https://kepler-beta.itu.edu.tr", headers=headers, allow_redirects=False
)
redirect_url = response.headers.get("Location")  # /login/auth/login

response = session.get(
    "https://kepler-beta.itu.edu.tr" + redirect_url,
    headers=headers,
    allow_redirects=False,
)

redirect_url = response.headers.get("Location")
response = session.get(redirect_url, headers=headers, allow_redirects=False)

login_url = response.headers.get("Location")
# print(redirect_url)
response = session.get(login_url, headers=headers, allow_redirects=False)

html = response.text

# BeautifulSoup ile HTML'i ayrıştır
soup = BeautifulSoup(html, "html.parser")

# Gerekli form verilerini çıkar
viewstate = soup.find("input", {"name": "__VIEWSTATE"}).get("value")
viewstategenerator = soup.find("input", {"name": "__VIEWSTATEGENERATOR"}).get("value")
eventvalidation = soup.find("input", {"name": "__EVENTVALIDATION"}).get("value")

# Form verilerini ve POST isteği için headers tanımla
form_data = {
    "__EVENTTARGET": "",
    "__EVENTARGUMENT": "",
    "__VIEWSTATE": viewstate,
    "__VIEWSTATEGENERATOR": viewstategenerator,
    "__EVENTVALIDATION": eventvalidation,
    "ctl00$ContentPlaceHolder1$hfAppName": "Öğrenci Bilgi Sistemi",
    "ctl00$ContentPlaceHolder1$tbUserName": "USERNAME",
    "ctl00$ContentPlaceHolder1$tbPassword": "PASSWORD",
    "ctl00$ContentPlaceHolder1$btnLogin": "Giriş / Login",
}

# POST isteği ile login işlemi gerçekleştir
response = session.post(login_url, data=form_data, headers=headers)

# Token almak için GET isteği at
token_url = "https://kepler-beta.itu.edu.tr/ogrenci/auth/jwt"
token_response = session.get(token_url, headers=headers)
token = "Bearer " + token_response.text
print(token)
# Session headers'ını güncelle
session.headers.update(
    {
        "Authorization": token,
        "Authority": "kepler-beta.itu.edu.tr",
        "Path": "/api/ders-kayit/v21",
        "Scheme": "https",
        "Origin": "https://kepler-beta.itu.edu.tr",
        "Referer": "https://kepler-beta.itu.edu.tr/ogrenci/DersKayitIslemleri/DersKayit",
    }
)

# Ders kaydı için POST isteği yap
ders_kayit_url = "https://kepler-beta.itu.edu.tr/api/ders-kayit/v21"
payload = {
    "ECRN": ["21362"],
    "SCRN": [],
}
ders_kayit_response = session.post(ders_kayit_url, json=payload)

# Yanıtı kontrol et
print(ders_kayit_response.status_code)
print(ders_kayit_response.text)