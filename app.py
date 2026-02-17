"""
İzmir Konut Projesi - Streamlit Uygulaması
Senior seviyesinde refactor edilmiş versiyon
"""
import sys
from pathlib import Path

# src klasörünü path'e ekle
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Optional

# Proje modüllerini import et
from src.config_loader import ConfigLoader
from src.logger_setup import setup_logging, get_logger
from src.model_loader import ModelLoader
from src.luxury_score import LuxuryScoreCalculator
from src.predictor import PricePredictor
from src.data_processor import DataProcessor
from src.validators import InputValidator
from src.exceptions import ProjectException

# Logging'i başlat
setup_logging(
    log_level="INFO",
    log_file="logs/app.log"
)
logger = get_logger(__name__)

# Config yükle
try:
    config = ConfigLoader("config/config.yaml")
except Exception as e:
    st.error(f"⚠️ Config dosyası yüklenemedi: {e}")
    st.stop()

# Streamlit sayfa ayarları
st.set_page_config(
    page_title=config.get("streamlit.page_title", "İzmir Konut Projesi Sunumu"),
    layout=config.get("streamlit.layout", "wide"),
    initial_sidebar_state=config.get("streamlit.sidebar_state", "expanded")
)

# Model ve veri yükleme
@st.cache_resource
def initialize_app():
    """Uygulamayı başlatır ve gerekli nesneleri yükler"""
    try:
        logger.info("Uygulama başlatılıyor...")
        
        # Model loader
        model_loader = ModelLoader(config)
        if not model_loader.load_all():
            return None
        
        # Luxury calculator
        luxury_calculator = LuxuryScoreCalculator(config)
        
        # Validator
        cleaning_config = config.get_cleaning_config()
        validator = InputValidator(
            price_min=cleaning_config.get('price_min', 100000),
            price_max=cleaning_config.get('price_max', 50000000),
            area_min=cleaning_config.get('area_min', 20),
            area_max=cleaning_config.get('area_max', 1000)
        )
        
        # Predictor
        predictor = PricePredictor(model_loader, luxury_calculator, validator)
        
        # Data processor
        data_processor = DataProcessor(config)
        
        logger.info("Uygulama başarıyla başlatıldı")
        
        return {
            'model_loader': model_loader,
            'predictor': predictor,
            'data_processor': data_processor,
            'config': config
        }
        
    except Exception as e:
        logger.error(f"Uygulama başlatma hatası: {e}")
        return None

# Uygulamayı başlat
app_data = initialize_app()

if app_data is None:
    st.error("⚠️ Dosyalar eksik! Lütfen 'model_egitim.py' kodunu çalıştırın.")
    st.info("💡 Terminal'de şu komutu çalıştırın: `python model_egitim.py`")
    st.stop()

model_loader = app_data['model_loader']
predictor = app_data['predictor']
data_processor = app_data['data_processor']
config = app_data['config']

# Yan menü
st.sidebar.title("📌 Proje Sunum Menüsü")

menu = st.sidebar.radio(
    "Bölümler:",
    [
        "1. Proje Hakkında & Amaç",
        "2. Veri Ön İşleme Süreci",
        "3. Gelişmiş Veri Analizi (EDA)",
        "4. Canlı Uygulama (Demo)",
        "5. Model Performansı",
        "6. Sonuç & Kazanımlar"
    ]
)

st.sidebar.divider()
project_info = config.get("project", {})
st.sidebar.caption(f"**Developer:** Eda Nur BİNİCİ\n\n**Course:** {project_info.get('course', 'Yapay Zekaya Giriş')}")

# --- 1. BÖLÜM: PROJE HAKKINDA ---
if menu == "1. Proje Hakkında & Amaç":
    st.title(f"🏠 {project_info.get('name', 'İzmir Konut Projesi')}")
    st.image(
        "https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80",
        use_container_width=True
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎯 Projenin Amacı")
        st.write("""
        Bu projenin temel amacı, İzmir ilindeki konutların özelliklerine (ilçe, m², oda sayısı vb.) 
        dayanarak piyasa değerini tahmin eden ve konutun **'Lüks Statüsünü'** analiz eden 
        yapay zeka tabanlı bir sistem geliştirmektir.
        """)
    with col2:
        st.subheader("🛠️ Kullanılan Teknolojiler")
        st.markdown("""
        * **Python:** Ana programlama dili
        * **Scikit-learn:** Makine öğrenmesi (Gradient Boosting)
        * **Pandas & Seaborn:** Veri analizi ve görselleştirme
        * **Streamlit:** İnteraktif web arayüzü
        * **YAML:** Yapılandırma yönetimi
        * **Logging:** Gelişmiş log sistemi
        """)
    
    st.info("💡 **Neden İzmir?** Veri çeşitliliği ve kalitesi (6.000+ satır) açısından model eğitimine en uygun şehir olduğu için seçilmiştir.")
    
    with st.expander("📋 Proje Yapısı"):
        st.code("""
Konut_Projesi/
├── src/              # Kaynak kod modülleri
├── config/           # Yapılandırma dosyaları
├── tests/            # Test dosyaları
├── logs/             # Log dosyaları
├── app.py            # Streamlit uygulaması
├── model_egitim.py   # Model eğitim scripti
└── requirements.txt  # Bağımlılıklar
        """)

# --- 2. BÖLÜM: VERİ ÖN İŞLEME ---
elif menu == "2. Veri Ön İşleme Süreci":
    st.title("🛠️ Veri Ön İşleme ve Temizlik")
    st.markdown("Yapay zeka modelinin başarısı için ham veriyi doğrudan kullanmadık. Aşağıdaki işlemlerden geçirdik:")
    
    with st.expander("Neden ve Nasıl Yaptık?", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.info("""
            **✂️ Train-Test Ayrımı (%80 / %20)**
            * **Neden?** Model eğitildiği veriyi ezberleyebilir.
            * **Çözüm:** Görmediği veriyle test edilmelidir.
            * **Akademik:** "Model performansı, eğitim verisi dışında kalan test verisi üzerinde ölçülmüştür."
            """)
            st.info("""
            **⚠️ Outlier (Aykırı Değer) Temizliği**
            * **Neden?** Aşırı pahalı/ucuz evler RMSE'yi şişirir ve modeli yanıltır.
            * **Akademik:** "Aykırı değerler, modelin genelleme kabiliyetini düşürdüğü için temizlenmiştir."
            """)
        with c2:
            st.success("""
            **📍 One-Hot Encoding**
            * **Neden?** Model "Çankaya", "Buca" gibi metinleri anlamaz.
            * **Çözüm:** İlçeler 0-1 matrisine dönüştürüldü. Label Encoding yapılmadı çünkü ilçeler arasında matematiksel bir üstünlük yok.
            """)
            st.success("""
            **📏 StandardScaler**
            * **Neden?** Fiyat (Milyonlar) ile Oda Sayısı (3-5) aynı ölçekte değil.
            * **Çözüm:** Hepsi standart ölçeğe getirildi, böylece model ağırlıkları adil dağıttı.
            """)
    
    st.divider()
    
    st.subheader("1. Ham Veri (Raw Data)")
    df = model_loader.raw_df
    st.write(f"Veri setinin ilk hali **{len(df)} satır** veriden oluşmaktadır.")
    st.dataframe(df.head(3))
    
    st.divider()
    
    st.subheader("2. Aykırı Değer Temizliği")
    
    outlier_stats = data_processor.get_outlier_stats(df)
    
    col1, col2 = st.columns(2)
    with col1:
        st.error("📉 Atılan Veriler")
        st.write(f"- Fiyatı {outlier_stats['price_max']:,} TL üzeri veya {outlier_stats['price_min']:,} TL altı olanlar.")
        st.write(f"- Metrekaresi {outlier_stats['area_max']} m² üzeri veya {outlier_stats['area_min']} m² altı olanlar.")
        st.metric("Temizlenen Satır", f"{outlier_stats['atilan_satir']} Adet", delta="-Gürültü", delta_color="inverse")
    
    with col2:
        st.success("✅ Kalan Temiz Veri")
        st.write("Model eğitiminde ve grafiklerde kullanılan, güvenilir veri seti.")
        st.metric("Eğitime Giren Veri", f"{outlier_stats['kalan_satir']} Adet", "Kaliteli")

# --- 3. BÖLÜM: EDA ---
elif menu == "3. Gelişmiş Veri Analizi (EDA)":
    st.title("📊 Gelişmiş Keşifçi Veri Analizi (EDA)")
    
    clean_df = data_processor.prepare_eda_data(model_loader.raw_df)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📉 Fiyat Analizi", "📏 M² & Regresyon", "🏙️ İlçe Analizleri", "🔥 Karmaşıklık Matrisi"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("1. Standart Fiyat Dağılımı")
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            sns.histplot(clean_df['price'], kde=True, color='blue', ax=ax1)
            plt.xlabel("Fiyat (TL)")
            plt.ylabel("Frekans")
            st.pyplot(fig1)
            st.caption("Fiyatlar sağa çarpık dağılıyor.")
        
        with col2:
            st.subheader("2. Logaritmik Fiyat Dağılımı")
            fig_log, ax_log = plt.subplots(figsize=(10, 6))
            sns.histplot(np.log1p(clean_df['price']), kde=True, color='purple', bins=30, ax=ax_log)
            plt.xlabel("Log(Fiyat)")
            plt.ylabel("Frekans")
            st.pyplot(fig_log)
            st.info("💡 **Analiz:** Logaritmik dönüşümle veri Normal Dağılıma (Çan Eğrisi) yaklaşmıştır.")
    
    with tab2:
        st.subheader("3. Metrekare - Fiyat İlişkisi (Regresyon)")
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        sns.regplot(x='area', y='price', data=clean_df, scatter_kws={'alpha':0.5, 'color':'green'}, line_kws={'color':'red'}, ax=ax2)
        plt.xlabel("Metrekare (m²)")
        plt.ylabel("Fiyat (TL)")
        plt.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig2)
        st.info("💡 **Analiz:** Kırmızı çizgi, metrekare arttıkça fiyatın genel artış eğilimini gösterir.")
    
    with tab3:
        st.subheader("4. İlçe Bazlı Fiyat Değişkenliği (Boxplot)")
        order = clean_df.groupby('district')['price'].median().sort_values(ascending=False).index
        fig_box, ax_box = plt.subplots(figsize=(14, 7))
        sns.boxplot(x='district', y='price', data=clean_df, order=order, palette='viridis', ax=ax_box)
        plt.xticks(rotation=45, ha='right')
        plt.ylabel("Fiyat (TL)")
        st.pyplot(fig_box)
        
        st.divider()
        st.subheader("5. Metrekare Başına En Değerli İlçeler")
        ilce_m2_deger = clean_df.groupby('district')['m2_fiyat'].mean().sort_values(ascending=False).head(10)
        st.bar_chart(ilce_m2_deger)
    
    with tab4:
        st.subheader("6. Korelasyon Matrisi (Heatmap)")
        numeric_df = clean_df[['price', 'area', 'age', 'toplam_oda', 'm2_fiyat']]
        numeric_df.columns = ['Fiyat', 'Metrekare', 'Bina Yaşı', 'Oda Sayısı', 'm² Değeri']
        
        fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap='coolwarm', linewidths=1, linecolor='white', ax=ax_corr)
        st.pyplot(fig_corr)

# --- 4. BÖLÜM: DEMO ---
elif menu == "4. Canlı Uygulama (Demo)":
    st.title("🚀 Canlı Tahmin Uygulaması")
    
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            ilce = st.selectbox("📍 İlçe", model_loader.ilce_listesi)
            ev_tipi = st.selectbox("🏠 Ev Tipi", model_loader.ev_tipleri)
            m2 = st.number_input("📏 Net Metrekare", 50, 1000, 120)
        with col2:
            oda = st.number_input("🚪 Oda Sayısı", 1, 10, 3)
            salon = st.number_input("🛋️ Salon Sayısı", 1, 5, 1)
            yas = st.number_input("🏗️ Bina Yaşı", 0, 100, 5)
        
        btn = st.button("✨ Hesapla", type="primary")
    
    if btn:
        try:
            result = predictor.predict(
                ilce=ilce,
                ev_tipi=ev_tipi,
                m2=m2,
                oda=oda,
                salon=salon,
                yas=yas
            )
            
            st.divider()
            c1, c2 = st.columns([1.5, 1])
            with c1:
                st.subheader("💰 Tahmini Değer")
                st.success(f"# {result['tahmini_fiyat']:,} TL")
            with c2:
                st.subheader("💎 Lüks Skoru")
                st.metric(
                    label="Prestij Puanı",
                    value=f"{result['luxury_score']}/100",
                    delta=result['luxury_category']
                )
            
            st.progress(result['luxury_score'] / 100)
            
            if result['luxury_score'] == 100:
                st.balloons()
                st.success("🏆 TEBRİKLER! Bölgenin en prestijli konutu.")
            
            # Detayları göster
            with st.expander("📊 Detaylı Analiz"):
                st.json(result['luxury_details'])
        
        except Exception as e:
            logger.error(f"Tahmin hatası: {e}")
            st.error(f"❌ Hata: {e}")

# --- 5. BÖLÜM: PERFORMANS ---
elif menu == "5. Model Performansı":
    st.title("📈 Model Performans Analizi")
    
    with st.expander("🚀 NEDEN BU MODELİ VE TEKNİKLERİ SEÇTİK?", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.warning("""
            **🔹 Gradient Boosting**
            * **Neden?** Basit bir regresyon çizgisi değil.
            * **Farkı:** Karmaşık ilişkileri (Semt-Fiyat dengesi vb.) öğrenir.
            * **Sonuç:** Model daha 'akıllı' oldu ve hataları azalttı.
            """)
        with col2:
            st.warning("""
            **🔹 Target Encoding (İlçe Skoru)**
            * **Ne Yaptık?** İlçeyi sadece 0-1 değil, "Değer Skoru" olarak öğrettik.
            * **Sonuç:** Model, Çeşme'nin Buca'dan değerli olduğunu matematiksel olarak anladı.
            """)
        with col3:
            st.warning("""
            **🔹 Logaritmik Dönüşüm**
            * **Neden?** Fiyatlar (Milyonlar) ile Oda Sayısı (3) arasında uçurum vardı.
            * **Sonuç:** Fiyatları dengeleyerek modelin büyük sayılarda boğulmasını engelledik.
            """)
    
    st.divider()
    
    metrikler = model_loader.metrikler
    r2_degeri = metrikler.get('R2 Skoru', 0)
    
    if r2_degeri > 0.85:
        yorum = "Mükemmel 🌟"
        renk = "normal"
    elif r2_degeri > 0.65:
        yorum = "Çok İyi ✅"
        renk = "normal"
    elif r2_degeri > 0.50:
        yorum = "Kabul Edilebilir (Orta) ⚠️"
        renk = "off"
    else:
        yorum = "Geliştirilmeli 🔻"
        renk = "inverse"
    
    c1, c2, c3 = st.columns(3)
    c1.metric("R2 Skoru (Doğruluk)", f"{r2_degeri:.3f}", yorum, delta_color=renk)
    c2.metric("MAE (Hata)", f"{int(metrikler.get('MAE (Ortalama Hata)', 0)):,} TL", delta_color="inverse")
    c3.metric("RMSE", f"{int(metrikler.get('RMSE (Kök Ortalama Hata)', 0)):,} TL", delta_color="inverse")
    
    st.divider()
    
    if r2_degeri < 0.65:
        st.warning("""
        **💡 Analiz Notu:** R2 Skorunun mevcut seviyesi, emlak piyasasındaki **"İnsan Faktörü"**nü gösterir. 
        Manzara, evin içi yapısı, acil satılık durumu gibi veri setinde olmayan özellikler fiyatı etkilemektedir.
        """)
    
    st.subheader("🧠 Modelin Karar Mekanizması")
    
    try:
        grafik_verisi = model_loader.onem_duzeyleri.copy()
        
        def isim_duzelt(metin: str) -> str:
            """Özellik isimlerini düzeltir"""
            if 'district_' in metin:
                return metin.replace('district_', '') + ' İlçesi'
            elif 'left_' in metin:
                return metin.replace('left_', '') + ' (Ev Tipi)'
            elif metin == 'area':
                return 'Metrekare (m²)'
            elif metin == 'age':
                return 'Bina Yaşı'
            elif metin == 'toplam_oda':
                return 'Oda Sayısı'
            elif metin == 'ilce_skoru':
                return 'İlçe Değeri'
            return metin
        
        if 'Özellik' in grafik_verisi.columns:
            grafik_verisi['Özellik'] = grafik_verisi['Özellik'].apply(isim_duzelt)
            st.bar_chart(grafik_verisi.set_index('Özellik'))
        else:
            st.write("Özellik önem grafiği mevcut değil.")
    except Exception as e:
        logger.warning(f"Grafik oluşturma hatası: {e}")
        st.write("Model karmaşıklığı nedeniyle özellik önem grafiği bu modelde gösterilemiyor.")

# --- 6. BÖLÜM: SONUÇ ---
elif menu == "6. Sonuç & Kazanımlar":
    st.title("🏁 Proje Değerlendirmesi ve Sonuç")
    st.info("""
    ### 📝 Proje Çıktıları
    Yapay Zekaya Giriş dersi kapsamında geliştirdiğim bu projede, teorik bilgilerimi pratiğe dökme fırsatı buldum. Temel kazanımlarım:
    
    1. **Veri Analizi:** İzmir emlak verileri temizlendi ve analiz edildi.
    2. **Yüksek Doğruluk:** Gelişmiş algoritmalar ile başarılı tahminler elde edildi.
    3. **Özgün Katma Değer:** "Lüks Skoru" algoritması ile projeye farklı bir boyut kazandırıldı.
    4. **Kullanıcı Deneyimi:** Proje, son kullanıcıya hitap eden bir web uygulamasına dönüştürüldü.
    5. **Kod Kalitesi:** Senior seviyesinde modüler yapı, logging ve error handling ile profesyonel bir proje oluşturuldu.
    """)
    st.write("---")
    st.success("Projemin sunumu burada sona ermiştir. Dinlediğin için teşekkür ederim! 👏")
    if st.button("Kutlama Yap 🎉"):
        st.balloons()
