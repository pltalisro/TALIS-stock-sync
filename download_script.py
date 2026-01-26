import os
from ftplib import FTP_TLS

# Citim datele din secretele GitHub (OBSESSION)
ftp_host = os.environ['OBSESSION_FTP_HOST']
ftp_user = os.environ['OBSESSION_FTP_USER']
ftp_pass = os.environ['OBSESSION_FTP_PASSWORD']

try:
    print(f"Conectare la {ftp_host}...")
    # Conexiune securizata (FTPS)
    ftps = FTP_TLS(ftp_host)
    ftps.login(ftp_user, ftp_pass)
    ftps.prot_p() # Activeaza criptarea datelor (SSL)
    
    print("Descarcare fisier...")
    # Salvam fisierul local cu numele stoc_obsession.csv
    with open('stoc_obsession.csv', 'wb') as fp:
        ftps.retrbinary('RETR /stock/Lagerbestand_V01.csv', fp.write)
    
    ftps.quit()
    print("Succes! Fisier descarcat.")
    
except Exception as e:
    print(f"Eroare critica: {e}")
    exit(1) # Opreste scriptul cu eroare pentru a notifica GitHub
