# 🏬 AI Tabanlı Mağaza İçi Müşteri Yoğunluğu ve Analitik Paneli

Bu proje; perakende mağazaları, alışveriş merkezleri ve süpermarketler için geliştirilmiş, bilgisayarlı görü (Computer Vision) ve yapay zeka tabanlı bir **İş Zekası (Business Intelligence) ve Analitik Paneli** yazılımıdır.  
Güvenlik kameraları üzerinden canlı olarak müşteri akışını takip eder, reyon bazlı müşteri davranışlarını analiz eder ve mağaza yöneticilerine ticari içgörüler sunar.

---

## 🚀 Öne Çıkan Özellikler

- **Canlı Nesne Takibi (Object Tracking):** YOLOv8 (Ultralytics) mimarisi kullanılarak mağaza içindeki insanlar %95+ doğrulukla tespit edilir ve her müşteriye benzersiz bir `Müşteri ID`'si atanır.
- **Gelişmiş Isı Haritası Analizi (Heatmap):** Müşterilerin reyonlarda geçirdiği vakitler arka planda matrislerde toplanır ve `GaussianBlur` filtresiyle pürüzsüz, kurumsal bir sıcaklık haritası olarak görselleştirilir.
- **Müşteri Giriş Sayımı (Line Counting):** Belirlenen sanal sınır çizgisinden geçen benzersiz müşteri sayısı anlık olarak hesaplanır.
- **Dwell-Time (Kalış Süresi) Takibi:** Her bir müşterinin mağaza veya reyon içerisinde toplamda kaç saniye vakit geçirdiği anlık ve ortalama olarak takip edilir.
- **Kapasite & Güvenlik Alarmı:** Mağaza içi anlık müşteri sayısı, panelden belirlenen maksimum sınırı aştığı anda sistem otomatik olarak kırmızı alarm durumuna geçer.
- **Zaman Serisi Grafik Analizi:** Mağazanın saatlik/dakikalık müşteri trafiği dalgalanmalarını gösteren canlı çizgi grafik desteği sunar.
- **Excel / CSV Raporlama:** Video sonunda toplanan tüm müşteri verileri tek tıkla `.csv` formatında indirilebilir.

---

## 🛠️ Kullanılan Teknolojiler

| Kategori | Teknoloji |
|---|---|
| Dil | Python 3.9+ |
| Yapay Zeka / Derin Öğrenme | YOLOv8 (Ultralytics) |
| Görüntü İşleme | OpenCV |
| Web Arayüzü / Dashboard | Streamlit |
| Veri Analizi & Grafik | Pandas, NumPy, Matplotlib |

---

## 📦 Kurulum ve Çalıştırma

### 1. Projeyi Klonlayın veya İndirin

```bash
git clone https://github.com/kullanici-adi/magaza-analitik-paneli.git
cd magaza-analitik-paneli
```

### 2. Sanal Ortam (Virtual Environment) Oluşturun

```bash
python -m venv venv
```

### 3. Sanal Ortamı Etkinleştirin

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### 4. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 5. Uygulamayı Başlatın

```bash
streamlit run app.py
```

Tarayıcınızda `http://localhost:8501` adresine gidin.

---

## 🎥 Kullanım

1. Sol panelden **Mağaza Güvenlik Kamerası Videosu** bölümüne mp4 formatındaki video dosyanızı yükleyin.
2. **YOLO Güven Eşiği (Confidence)** ve **Isı Haritası Şeffaflığı** ayarlarını ihtiyacınıza göre düzenleyin.
3. **Deploy** butonuna tıklayarak analizi başlatın.
4. Üst sekmeleri kullanarak **Canlı Kamera Takip Yayını**, **Reyon Yoğunluk Isı Haritası** ve **Zaman Serisi Trafik Grafiği** arasında geçiş yapın.
5. Analiz tamamlandığında müşteri verilerini `.csv` formatında indirin.

---

## ⚙️ Yapılandırma

| Parametre | Açıklama | Varsayılan |
|---|---|---|
| YOLO Güven Eşiği | Tespit hassasiyeti (0.0 – 1.0) | 0.25 |
| Isı Haritası Şeffaflığı | Overlay yoğunluğu (0.0 – 1.0) | 0.55 |
| Maksimum Kapasite | Alarm eşiği (kişi sayısı) | 20 |

---

## 📊 Çıktılar

- **Canlı Dashboard:** Anlık metrikler ve görsel analiz
- **Heatmap Görseli:** Reyon bazlı yoğunluk haritası
- **Zaman Serisi Grafiği:** Trafik dalgalanma analizi
- **CSV Raporu:** Tüm müşteri verileri (ID, giriş zamanı, kalış süresi, çizgi geçişi)

---

## 📄 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.

---

## 🤝 Katkı

Katkıda bulunmak için lütfen bir `fork` oluşturun ve `pull request` gönderin. Her türlü geri bildirim ve öneri memnuniyetle karşılanır.
