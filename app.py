import streamlit as st
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sayfa ayarları
st.set_page_config(page_title="Hastalık Çözüm Asistanı", page_icon="💊", layout="centered")

# Stil
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 16px;
        border-radius: 10px;
        font-size: 16px;
        margin-top: 10px;
    }
    .stTextInput > div > input {
        padding: 10px;
        border-radius: 8px;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Veri tabanı
hastalik_cozum_db = {
    "soğuk algınlığı": "Bol su iç, dinlen, vitamin C al.",
    "baş ağrısı": "Yeterli uyku al, bol su iç, sakinleşmek için derin nefes al.",
    "mide bulantısı": "Hafif yiyecekler ye, sıvı alımını artır.",
    "kas ağrısı": "Ilımlı egzersiz yap, sıcak kompres uygulayabilirsin.",
    "yüksek ateş": "Ateşi düşürmek için hafif ateş düşürücü ilaçlar kullanabilirsin.",
    "öksürük": "Balmumu ve sıcak su içmeyi deneyebilirsin.",
    "grip": "İstirahat et, bol sıvı al ve sıcak içecekler tüket.",
    "boğaz ağrısı": "Sıcak tuzlu su ile gargara yap, dinlen.",
    "burun tıkanıklığı": "Burun spreyi kullan veya buruna tuzlu su çek.",
    "tansiyon": "Çok tuz tüketme, bol su al."
}

hastaliklar = list(hastalik_cozum_db.keys())
cozumler = list(hastalik_cozum_db.values())

# Başlık ve açıklama
st.title("💊 Hastalık Belirtisi Çözüm Asistanı")
st.markdown("🔍 Aşağıya bir belirti yaz, sana en yakın hastalığı bulalım ve çözüm önerelim.")

# Giriş
user_input = st.text_input("📝 Belirti giriniz:", placeholder="örnek: boğazım ağrıyor, midem bulanıyor...")

# Buton
if st.button("🚀 Çözüm Bul"):
    if not user_input.strip():
        st.warning("⚠️ Lütfen bir belirti girin.")
    else:
        # TF-IDF ile eşleşme
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(hastaliklar + [user_input])
        cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
        most_similar_index = np.argmax(cosine_similarities)
        en_benzer_hastalik = hastaliklar[most_similar_index]
        cozum = cozumler[most_similar_index]

        # Sonuç göster
        st.success(f"✅ En benzer hastalık: **{en_benzer_hastalik}**")
        st.info(f"💡 Önerilen çözüm:\n\n{cozum}")

# Footer
st.markdown("---")
st.caption("🧠 Bu uygulama sadece bilgilendirme amaçlıdır. Ciddi durumlarda bir sağlık profesyoneline danışın.")
