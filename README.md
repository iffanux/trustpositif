# trustpositif
![Kominfo](/kominfo_.png) ![Aduan Content](/aduan_content.png) ![Bind9](/Bind_9_ISC.png)


# Python3 Script to update trustpositif kominfo
* Script sederhana ini bisa untuk Bind dan PowerDNS
* Updating database dari servertrustpositif kominfo.
* Prinsip kerjanya meredirect domain2 ke CNAME yang kita punya.
* Cara Kerjanya adalah mengunduh database truspositif dan menyimpannya dalam domains.txt file,
* Menambahkan SOA Header dan mengubah file ekstensi ke rpz
* Edit SOA di header.txt sesuai server DNS kamu
* Edit atau update (google safesearch) gsafesearch.txt
* Silahkan menjalankan script : python3 update_trustpositif.py atau buat cron * 1 1 * * python3 ~/update_trustpositif.py
* Cron job tersebut akan mengeksekusi file setiap tanggal 1 jam 1 Dini Hari tiap bulan
# Anda bebas untuk mengubah, mendistribusikan script ini untuk keperluan anda
# https://www.gnu.org/licenses/gpl-3.0.html
