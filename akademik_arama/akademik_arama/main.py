import os
import re
import time
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from flask import Flask, render_template, request
import pymongo
from bson import ObjectId
from bs4 import BeautifulSoup
import requests
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['akademik_veritabani']
mongo_collection = mongo_db['yayinlar']
es = Elasticsearch(['http://localhost:9200'])
app = Flask(__name__)


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["akademik_veritabani"]
collection = db["yayinlar"]


def parse_yazarlar(yazarlar_str):

    return [yazar.strip() for yazar in yazarlar_str.split(',')]

def parse_yayinci_ve_tarih(yazarlar_str):

    yayinci_ve_tarih = yazarlar_str.split(' - ')[1]
    return yayinci_ve_tarih

def correct_keyword(keyword):
    try:

        url = f"https://www.google.com/search?q={keyword}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        corrected_element = soup.find("a", {"class": "spell"})
        if corrected_element:
            corrected_keyword = corrected_element.text
            return corrected_keyword
        else:
            return keyword
    except Exception as e:
        print(f"Hata: {e}")
        return keyword
def migrate_data():
    for document in mongo_collection.find():

        document.pop('_id', None)
        es.index(index='akademik_veritabani', body=document)

def web_scraping(anahtar_kelime):
    corrected_keyword = correct_keyword(anahtar_kelime)
    search_url = f"https://scholar.google.com/scholar?q={corrected_keyword}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    papers = soup.find_all('div', class_='gs_ri')

    yayinlar = []
    for index, paper in enumerate(papers):
        if index >= 20:
            break

        yayin_adi_tag = paper.find('h3', class_='gs_rt')
        yayin_adi = yayin_adi_tag.text.strip() if yayin_adi_tag else ''

        yazarlar_tag = paper.find('div', class_='gs_a')
        yazarlar_str = yazarlar_tag.text.strip() if yazarlar_tag else ''
        yazarlar = parse_yazarlar(yazarlar_str)

        tarih_etiketleri = paper.find_all(['div', 'span'], class_='gs_a')
        tarih_text = ''
        for etiket in tarih_etiketleri:
            tarih_text += etiket.text + ' '
        tarihler = re.findall(r'\b(?:19|20)\d{2}\b', tarih_text)
        yayin_tarihi = ' '.join(tarihler) if tarihler else ''

        yayin_turu_tag = paper.find('div', class_='gs_a')
        yayin_turu = yayin_turu_tag.text.strip() if yayin_turu_tag else ''

        yayinci_adi_tag = paper.find('div', class_='gs_a')
        yayinci_adi = yayinci_adi_tag.text.strip() if yayinci_adi_tag else ''

        anahtar_kelimeler_arama = corrected_keyword

        anahtar_kelimeler_makale_tag = paper.find('div', class_='gs_rs')
        anahtar_kelimeler_makale = anahtar_kelimeler_makale_tag.text.strip() if anahtar_kelimeler_makale_tag else ''

        ozet_tag = paper.find('div', class_='gs_rs')
        ozet = ozet_tag.text.strip() if ozet_tag else ''

        referanslar_tag = paper.find('div', class_='gs_fl')
        referanslar = referanslar_tag.text.strip() if referanslar_tag else ''

        alinti_sayisi_tag = paper.find('div', class_='gs_fl')
        alinti_sayisi = ''
        if alinti_sayisi_tag:
            alinti_text = alinti_sayisi_tag.text.strip()
            if 'Alıntı yap' in alinti_text:
                alinti_sayisi = alinti_text.split('Alıntı yap')[1].split('İlgili makaleler')[0].strip()

        doi_tag = paper.find('div', class_='gs_fl')
        doi = doi_tag.text.strip() if doi_tag else ''

        url_tag = paper.find('h3', class_='gs_rt').find('a')
        if url_tag:
            url = url_tag['href']
        else:
            url = ''


        yayin_bilgisi = {
            'yayin_id': str(ObjectId()),
            'yayin_adi': yayin_adi,
            'yazarlar': yazarlar,
            'yayin_turu': yayin_turu,
            'yayin_tarihi': yayin_tarihi,
            'yayinci_adi': yayinci_adi,
            'anahtar_kelimeler_arama': anahtar_kelimeler_arama,
            'anahtar_kelimeler_makale': anahtar_kelimeler_makale,
            'ozet': ozet,
            'referanslar': referanslar,
            'alinti_sayisi': alinti_sayisi,
            'doi': doi,
            'url': url
        }


        collection.insert_one(yayin_bilgisi)


        pdf_url_tag = paper.find('h3', class_='gs_rt').find('a')
        if pdf_url_tag:
            pdf_url = pdf_url_tag['href']
            if pdf_url and pdf_url.endswith('.pdf'):
                pdf = requests.get(pdf_url)
                dosya_adi = f"{yayin_adi}.pdf"
                dosya_yolu = os.path.join("pdf_dosyalari", dosya_adi)  # pdf_dosyalari klasörüne kaydet
                if not os.path.exists("pdf_dosyalari"):
                    os.makedirs("pdf_dosyalari")
                with open(dosya_yolu, 'wb') as f:
                    f.write(pdf.content)
        else:
            print(f"{yayin_adi} PDF indirme hatası: PDF URL bulunamadı")


        time.sleep(1)

        yayinlar.append(yayin_bilgisi)

    return yayinlar[:20]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        anahtar_kelime = request.form['anahtar_kelime']
        yayinlar = web_scraping(anahtar_kelime)
        if not yayinlar:
            return render_template('not_found.html', anahtar_kelime=anahtar_kelime)
    else:
        yayinlar = get_all_yayinlar()
    return render_template('index.html', yayinlar=yayinlar)





@app.route('/detail/<string:yayin_id>')
def detail(yayin_id):
    yayin = collection.find_one({"yayin_id": yayin_id})
    if yayin:
        return render_template('detail.html', yayin=yayin)
    else:
        return "Yayın bilgisi bulunamadı.", 404


def get_all_yayinlar():
    yayinlar = list(collection.find().sort("yayin_adi", pymongo.ASCENDING))

    return yayinlar

if __name__ == '__main__':
    #migrate_data()
    app.run(debug=False)
