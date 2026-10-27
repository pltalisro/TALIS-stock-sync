import urllib.request
import xml.etree.ElementTree as ET
import csv

# Pune link-ul complet intre ghilimele (pastreaza ghilimelele)
url_feed = "https://www.uniquefurniture.dk/dwapi/Feeds/GetFeedOutput?Id=12&languageId=LANG2&currencyId=EUR&shopId=SHOP10"

print("Descarcare date de la Unique Furniture...")
try:
    # Setam un user-agent ca sa nu fim blocati de server
    req = urllib.request.Request(url_feed, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        xml_data = response.read()
    
    print("Parsare XML...")
    root = ET.fromstring(xml_data)
    
    # Cream fisierul CSV curat (separator punct si virgula)
    with open('stoc_unique.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        
        # Capul de tabel (doar ce ai nevoie)
        writer.writerow(['SKU', 'Stoc', 'EAN', 'Nume', 'Imagine'])
        
        # Extragem informatiile din fiecare <Product>
        for prod in root.findall('.//Product'):
            sku = prod.find('Sku')
            sku = sku.text if sku is not None else ''
            
            stoc = prod.find('stock')
            stoc = stoc.text if stoc is not None else '0'
            
            ean = prod.find('ean')
            ean = ean.text if ean is not None else ''
            
            nume = prod.find('title')
            nume = nume.text if nume is not None else ''
            
            img = prod.find('additional_image_link')
            img = img.text if img is not None else ''
            
            # Daca exista un Sku, salvam randul
            if sku:
                writer.writerow([sku, stoc, ean, nume, img])
                
    print("Fisier CSV generat cu succes!")
except Exception as e:
    print(f"Eroare: {e}")
    exit(1)
