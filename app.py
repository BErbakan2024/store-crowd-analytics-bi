import streamlit as st
import cv2
import tempfile
import numpy as np
import time
import matplotlib.pyplot as plt
from ultralytics import YOLO
from src.tracker import CustomerTracker

# 1. SAYFA VE TEMA AYARLARI
st.set_page_config(
    page_title="Mağaza İş Zekası ve Kalabalık Analiz Paneli", 
    layout="wide", 
    page_icon="🏬"
)

# Kurumsal UI Tasarımı için Custom CSS
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
    .metric-card { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
        border: 1px solid #eef2f5;
        text-align: center;
    }
    .alarm-card {
        background-color: #ffeaea;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #ff4d4d;
        color: #cc0000;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. MODEL VE TRACKER BAŞLATMA
@st.cache_resource
def load_yolo_model():
    return YOLO('yolov8n.pt')

model = load_yolo_model()
tracker = CustomerTracker()

# 3. YAN PANEL (SIDEBAR) - GELİŞMİŞ AYARLAR
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2622/2622140.png", width=80)
st.sidebar.title("🎛️ Sistem Kontrolleri")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader("📹 Mağaza Güvenlik Kamerası Videosu", type=["mp4", "avi", "mov"])
st.sidebar.markdown("---")

st.sidebar.subheader("🎯 Algılama Hassasiyeti")
conf_threshold = st.sidebar.slider("YOLO Güven Eşiği (Confidence)", 0.1, 1.0, 0.40, step=0.05)
heatmap_alpha = st.sidebar.slider("🔥 Isı Haritası Şeffaflığı", 0.1, 0.9, 0.55, step=0.05)

st.sidebar.markdown("---")
st.sidebar.subheader("🚨 Güvenlik & Kapasite")
max_capacity = st.sidebar.number_input("Maksimum Mağaza Kapasitesi", min_value=1, value=5, step=1)

# 4. ANA SAYFA BAŞLIK ALANI
st.title("🏬 AI Tabanlı Mağaza İş Zekası (BI) ve Analitik Paneli")
st.markdown(" *Müşteri davranış analitiği, reyon yoğunluk haritaları, dwell-time takibi ve kapasite yönetimi.*")
st.write("---")

# 5. ANLIK ANALİTİK KARTLARI (KPIs)
st.subheader("📈 Canlı Mağaza Performans Metrikleri")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    current_count_placeholder = st.empty()
with kpi_col2:
    total_count_placeholder = st.empty()
with kpi_col3:
    dwell_time_placeholder = st.empty()
with kpi_col4:
    status_placeholder = st.empty()

# Dinamik Alarm Alanı
alarm_placeholder = st.empty()
st.write("---")

# 6. SEKME (TAB) MİMARİSİ
tab1, tab2, tab3 = st.tabs([
    "📷 Canlı Kamera Takip Yayını", 
    "🔥 Reyon Yoğunluk Isı Haritası (Heatmap)", 
    "📊 Zaman Serisi Trafik Grafiği"
])

with tab1:
    st.markdown("### `Canlı Nesne Takibi ve Giriş İstatistikleri`")
    video_placeholder = st.empty()

with tab2:
    st.markdown("### `Müşterilerin Reyonlarda Yoğunlaşma Alanları`")
    heatmap_placeholder = st.empty()

with tab3:
    st.markdown("### `Zamana Göre Anlık Mağaza Müşteri Grafiği`")
    chart_placeholder = st.empty()

# 7. VİDEO İŞLEME VE ANALİTİK MOTORU
if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    cap = cv2.VideoCapture(tfile.name)
    
    # Veri Takip Sözlükleri
    already_counted = set()
    customer_entry_times = {}  # ID -> Giriş Zamanı
    customer_dwell_times = []  # Tamamlanan kalış süreleri listesi
    
    # Grafik için veri listeleri
    time_steps = []
    customer_counts = []
    frame_counter = 0
    
    # Isı Haritası Başlatma
    ret, first_frame = cap.read()
    if ret:
        height, width, _ = first_frame.shape
        heatmap_accumulator = np.zeros((height, width), dtype=np.float32)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
    start_time = time.time()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_counter += 1
        height, width, _ = frame.shape
        line_y = int(height * 0.6) 
        base_frame = frame.copy()
        
        # YOLO Tespiti (Sadece İnsan sınıfı: 0)
        results = model(frame, conf=conf_threshold, classes=[0], verbose=False)
        
        list_of_rects = []
        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            list_of_rects.append([int(x1), int(y1), int(x2 - x1), int(y2 - y1)])
            
        boxes_ids = tracker.update(list_of_rects)
        current_in_frame = len(boxes_ids)
        
        # Zaman grafiği verilerini toplama (Her 5 karede bir kaydet)
        if frame_counter % 5 == 0:
            time_steps.append(len(time_steps) * 0.2) # Yapay zaman adımı
            customer_counts.append(current_in_frame)
        
        # KAPASİTE ALARMI KONTROLÜ
        if current_in_frame > max_capacity:
            alarm_placeholder.markdown(
                f"<div class='alarm-card'>⚠️ ALARM: MAĞAZA İÇİ MAKSİMUM KAPASİTE SINIRI AŞILDI! (İçerideki: {current_in_frame} / Sınır: {max_capacity})</div>", 
                unsafe_allow_html=True
            )
        else:
            alarm_placeholder.empty()
            
        for box_id in boxes_ids:
            x, y, w, h, id = box_id
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            
            # --- DWELL TIME (KALMA SÜRESİ) HESABI ---
            if id not in customer_entry_times:
                customer_entry_times[id] = frame_counter  # Giriş yaptığı kare numarasını tut
            else:
                # Mağazada kalma süresini kare tabanlı simüle et (Saniye cinsinden)
                duration = (frame_counter - customer_entry_times[id]) / 25.0
                if duration > 1.0: # 1 saniyeden uzun süredir buradaysa kaydet
                    customer_dwell_times.append(duration)
            
            # --- GELİŞMİŞ ISI HARİTASI İZİ ---
            cv2.circle(heatmap_accumulator, (cx, cy), 20, 2, -1)
            
            # Tasarım Çizimleri
            cv2.rectangle(frame, (x, y), (x + w, y + h), (52, 152, 219), 2) # Modern Mavi Kutu
            cv2.putText(frame, f"ID: {id}", (x, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (52, 152, 219), 2)
            cv2.circle(frame, (cx, cy), 4, (46, 204, 113), -1) 
            
            # Giriş Çizgisi Sayım Kontrolü
            if line_y - 15 < cy < line_y + 15:
                already_counted.add(id)
                
        # Çizgi Çizimi
        cv2.line(frame, (0, line_y), (width, line_y), (231, 76, 60), 2)
        cv2.putText(frame, "MAĞAZA GİRİŞ SINIRI", (10, line_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (231, 76, 60), 1)
        
        # --- ISI HARİTASI BLUR VE RENKLENDİRME ---
        if np.max(heatmap_accumulator) > 0:
            heatmap_blur = cv2.GaussianBlur(heatmap_accumulator, (75, 75), 0)
            heatmap_norm = cv2.normalize(heatmap_blur, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        else:
            heatmap_norm = np.zeros((height, width), dtype=np.uint8)
            
        heatmap_color = cv2.applyColorMap(heatmap_norm, cv2.COLORMAP_JET)
        overlay_frame = cv2.addWeighted(heatmap_color, heatmap_alpha, base_frame, 1 - heatmap_alpha, 0)
        
        # Matplotlib ile Canlı Grafik Çizimi
        fig, ax = plt.subplots(figsize=(6, 2.5))
        ax.plot(time_steps, customer_counts, color="#3498db", linewidth=2)
        ax.set_title("Anlık Müşteri Grafiği", fontsize=10)
        ax.set_xlabel("Zaman (sn)", fontsize=8)
        ax.set_ylabel("Kişi Sayısı", fontsize=8)
        ax.grid(True, linestyle="--", alpha=0.5)
        
        # Format Dönüşümleri
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        overlay_rgb = cv2.cvtColor(overlay_frame, cv2.COLOR_BGR2RGB)
        
        # Sekme Ekranlarını Güncelleme
        video_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
        heatmap_placeholder.image(overlay_rgb, channels="RGB", use_container_width=True)
        chart_placeholder.pyplot(fig)
        plt.close(fig) # Hafıza şişmesin diye grafiği kapatıyoruz
        
        # Ortalama Kalma Süresi Metni
        avg_dwell = np.mean(customer_dwell_times) if customer_dwell_times else 0.0
        
        # KPI KARTLARININ HTML İLE ŞIKLAŞTIRILMASI
        current_count_placeholder.markdown(f"<div class='metric-card'><span style='font-size:14px;color:#7f8c8d;'>👥 İçerideki Güncel</span><br><span style='font-size:26px;font-weight:bold;color:#2c3e50;'>{current_in_frame}</span></div>", unsafe_allow_html=True)
        total_count_placeholder.markdown(f"<div class='metric-card'><span style='font-size:14px;color:#7f8c8d;'>🚪 Toplam Giriş</span><br><span style='font-size:26px;font-weight:bold;color:#27ae60;'>{len(already_counted)}</span></div>", unsafe_allow_html=True)
        dwell_time_placeholder.markdown(f"<div class='metric-card'><span style='font-size:14px;color:#7f8c8d;'>⏱️ Ort. Kalış Süresi</span><br><span style='font-size:26px;font-weight:bold;color:#e67e22;'>{avg_dwell:.1f} sn</span></div>", unsafe_allow_html=True)
        status_placeholder.markdown("<div class='metric-card'><span style='font-size:14px;color:#7f8c8d;'>⚡ Sistem Durumu</span><br><span style='font-size:22px;font-weight:bold;color:#2980b9;'>İŞLENİYOR</span></div>", unsafe_allow_html=True)
        
    cap.release()
    status_placeholder.markdown("<div class='metric-card'><span style='font-size:14px;color:#7f8c8d;'>⚡ Sistem Durumu</span><br><span style='font-size:22px;font-weight:bold;color:#27ae60;'>BİTTİ</span></div>", unsafe_allow_html=True)
else:
    st.info("💡 Başlamak için lütfen sol paneldeki menüyü kullanarak analiz edilecek video dosyasını yükleyin.")