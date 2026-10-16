import os
import paramiko
import xml.etree.ElementTree as ET
import csv

host = os.environ['ACTONA_SFTP_HOST']
user = os.environ['ACTONA_SFTP_USER']
password = os.environ['ACTONA_SFTP_PASS']

try:
    print(f"Conectare la serverul SFTP {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=password, port=22)
    sftp = ssh.open_sftp()
    
    print("Descarcare fisier inv_rpt.xml...")
    sftp.get('inv_rpt.xml', 'inv_rpt.xml')
    
    sftp.close()
    ssh.close()
    print("Descarcare finalizata. Incepem conversia in CSV pentru MerchantPro...")
    
    # Parcurgem XML-ul de la Actona
    tree = ET.parse('inv_rpt.xml')
    root = tree.getroot()
    
    # Cream fisierul CSV cu formatare speciala pentru MerchantPro (utf-8-sig si separator ;)
    with open('stoc_actona.csv', 'w', newline='', encoding='utf-8-sig') as f:
        # Folosim punct si virgula ca delimitator
        writer = csv.writer(f, delimiter=';') 
        
        # Capul de tabel (coloanele)
        writer.writerow(['SKU', 'EAN', 'Stoc', 'Stoc_Viitor', 'Data_Viitoare'])
        
        # Extragem fiecare produs
        for produs in root.findall('Data'):
            item = produs.find('item').text if produs.find('item') is not None else ''
            ean = produs.find('ean_code').text if produs.find('ean_code') is not None else ''
            qty = produs.find('available_qty').text if produs.find('available_qty') is not None else '0'
            next_qty = produs.find('available_next_qty').text if produs.find('available_next_qty') is not None else '0'
            next_date = produs.find('available_date').text if produs.find('available_date') is not None else ''
            
            writer.writerow([item, ean, qty, next_qty, next_date])
            
    print("Succes! Fisierul CSV pentru MerchantPro a fost generat.")
    
except Exception as e:
    print(f"Eroare: {e}")
    exit(1)
