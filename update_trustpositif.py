#! /usr/bin/env python3
#! Updating database trustpositif kominfo
#! Prinsip kerjanya meredirect domain2 ke CNAME yang kita punya
#! Cara Kerjanya adalah mengunduh database truspositif dan menyimpannya dalam domains.txt file,
#! Menambahkan SOA Header dan merubah file ekstensi ke rpz
#! Menjalankan script : python3 update_trustpositif.py
import ssl
import shutil
import requests
import os
from pathlib import Path
import dbus
if os.path.exists("domains.txt"):
  os.remove("domains.txt")
else:
  print("File database tidak ada")

#! Membuat file domains.txt kosong yang nanti akan kita re-write
open('domains.txt', 'a').close()
print("file database kosong baru sudah dibuat")
ssl._create_default_https_context = ssl._create_unverified_context

#! Membypass SSL Certificate
print("bypassing SSL Mohon tunggu beberapa saat")
response = requests.get('https://trustpositif.kominfo.go.id/Rest_server/domains', timeout=30, verify=False)
files = {'f': ('domains.txt', open('domains.txt', 'rb'))}
response.encoding = 'utf-8'
response.raise_for_status()
file = open("domains.txt", "w")
file.write(response.text)
file.close()

#! Mengunduh file database dari trustpostif
print('database berhasil diunduh')

inputFile = "domains.txt"
outputFile = "database.txt"
headerFile = "header.txt"
zoneFile = "db.zone.rpz"
#! Silahkan ganti sesuai dengan domain CNAME kamu
my_string = " IN CNAME trustpositif.iforte.net.id. "

with open(inputFile, 'r') as inFile:
    with open(outputFile, 'w+') as outFile:
     for line in inFile:
        line = line.rstrip("\n")
        outFile.write(line + my_string + "\n")
file.close()

#! Membuat file rpz kosong
if os.path.exists("db.zone.rpz"):
  os.remove("db.zone.rpz")
open('db.zone.rpz', 'a').close()

filenames = ['header.txt', 'database.txt']
with open('zoneFile', 'a+') as zoneFile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                zoneFile.write(line)
file.close()

#! Menggabungkan file SOA Header dan database lalu merubah ke ekstension rpz

print("\nThe content is merged successfully.!")
print("sedang menulis ulang database ke rpz..Mohon tunggu sejenak!")
print("file rpz sudah dibuat ulang")
print("memindahkan file rpz")
shutil.move('zoneFile', '/etc/named/db.zone.rpz')

print("restarting bind service .......")
sysbus = dbus.SystemBus()
systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
job = manager.RestartUnit('named.service', 'fail')

print("File sudah dipindah dan bind service di restart, silahkan periksa kembali file rpz")
print ("Jangan lupa buat cronjob * 1 1 * * python3 ~/update_trust.py kalau tdk males silahkan update secara manual")
