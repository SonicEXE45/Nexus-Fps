NEXUS FPS — PUBLIC WEBSITE PACKAGE
==================================

PUBLIC ADRES
https://nexusfps.io

Bu paket, siteyi public bir Python hosting hizmetinde çalıştırmak üzere hazırlanmıştır.
Site artık ziyaretçinin bilgisayarında Python çalıştırmasına bağlı değildir.
Baslat.pyw yalnızca public adresi kontrol eder ve tarayıcıda açar.

ÖNEMLİ: ŞU ANDA OTOMATİK OLARAK YAYINLANMIŞ DEĞİLDİR
-----------------------------------------------
Bir alan adı yalnızca Python kodunu değiştirerek internete açılamaz. Public yayın için:
1. nexusfps.io alan adının satın alınmış olması ve DNS panelinin erişilebilir olması gerekir.
2. Bu proje bir public Python hosting hizmetine yüklenip deploy edilmelidir.
3. Hosting panelinde nexusfps.io özel alan adı olarak eklenmelidir.
4. Hosting panelinin verdiği DNS kayıtları alan adının DNS yönetim ekranına girilmelidir.
5. Alan adı doğrulandıktan ve HTTPS sertifikası etkinleştikten sonra https://nexusfps.io açılır.

RENDER DEPLOY AYARLARI
----------------------
Proje, Render için render.yaml dosyası içerir.
Git deposuna proje klasörünün tamamını ekle. Render'da New > Blueprint seçip
bu depoyu bağla ve render.yaml yapılandırmasını kullan.

Elle Web Service oluşturulursa:
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
Health Check Path: /api/health

Deploy başarılı olduğunda önce Render'ın verdiği *.onrender.com adresini test et.
Sonra Render servis ayarlarında Custom Domains bölümüne nexusfps.io ekle.
Render'ın gösterdiği DNS kayıtlarını alan adı sağlayıcının DNS paneline gir ve
Render panelinde Verify işlemini çalıştır. HTTPS sertifikası Render tarafından
otomatik oluşturulur ve yenilenir. Ücretsiz Web Service uzun süre istek almazsa uykuya geçebilir;
ilk ziyaret sırasında yeniden başlaması biraz sürebilir.

DOSYA KATEGORİLERİ
------------------
downloads/application  -> Uygulama dosyaları (EXE, MSI vb.)
downloads/updates      -> Güncellemeler
downloads/tools        -> Yardımcı araçlar
downloads/extras       -> Ek içerikler

Dosyalar hosting deploy'una dahil edildiğinde /api/downloads listesinde görünür.
Yeni sürüm eklemek için dosyayı ilgili klasöre koyup depoya gönder ve yeniden deploy et.
Dosya boyutu çok büyükse Git deposu yerine kalıcı disk veya harici dosya/CDN depolaması
kullanılmalıdır. Ücretsiz hosting ortamlarının dosya sistemi kalıcı olmayabilir.

PYTHON BAŞLATICI
----------------
Windows'ta Baslat.pyw dosyasına çift tıkla.
Bu araç public https://nexusfps.io adresini kontrol eder ve erişilebiliyorsa açar.
Siteyi barındırmaz; hostingte yayınlanan site, bu pencere kapansa da çalışmaya devam eder.

GELİŞTİRME ÖNİZLEMESİ
--------------------
Bilgisayarda test etmek için:
  pip install -r requirements.txt
  python app.py
Ardından tarayıcıda http://127.0.0.1:8000 açılır.
Bu adres yalnızca geliştirme önizlemesi içindir; public site adresi değildir.

GEREKSİNİMLER
-------------
Python 3.10+
requirements.txt içindeki Flask ve Gunicorn paketleri

NOT
---
Site içindeki FPS/CPU/GPU değerleri tanıtım amaçlı statik arayüz örneğidir;
gerçek uygulamadan canlı veri okumaz.
