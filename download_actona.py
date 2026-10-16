import os
import paramiko

# Citim secretele din GitHub
host = os.environ['ACTONA_SFTP_HOST']
user = os.environ['ACTONA_SFTP_USER']
password = os.environ['ACTONA_SFTP_PASS']

try:
    print(f"Conectare la serverul SFTP {host}...")
    # Initializam clientul SSH/SFTP
    ssh = paramiko.SSHClient()
    # Acceptam automat cheia serverului (necesar pentru prima conectare)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Ne conectam pe portul 22
    ssh.connect(host, username=user, password=password, port=22)
    sftp = ssh.open_sftp()
    
    print("Descarcare fisier inv_rpt.xml...")
    # Descarcam fisierul de pe server si il salvam local ca "stoc_actona.xml"
    sftp.get('inv_rpt.xml', 'stoc_actona.xml')
    
    sftp.close()
    ssh.close()
    print("Succes! Fisierul Actona a fost descarcat.")
    
except Exception as e:
    print(f"Eroare critica la conectarea Actona: {e}")
    exit(1)
