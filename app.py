import streamlit as st
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher

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
    "tansiyon": "Çok tuz tüketme, bol su al.",
    "mide ağrısı": "Yavaş yemek ye, ağır yiyeceklerden kaçın.",
    "kas çekmesi": "Gergin kasları rahatlatacak masajlar yap.",
    "diyabet": "Şeker seviyeni izleyip sağlıklı beslenmeye özen göster."
}

hastaliklar = list(hastalik_cozum_db.keys())
cozumler = list(hastalik_cozum_db.values())

# Başlık ve açıklama
st.title("💊 Hastalık Belirtisi Çözüm Asistanı")
st.markdown("🔍 Aşağıya bir belirti yaz, sana en yakın hastalığı bulalım ve çözüm önerelim.")

# Giriş
user_input = st.text_input("📝 Belirti giriniz:", placeholder="örnek: boğazım ağrıyor, midem bulanıyor...")

# Benzerlik hesaplama fonksiyonu (Türkçe kelimeleri karşılaştır)
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Buton
if st.button("🚀 Çözüm Bul"):
    if not user_input.strip():
        st.warning("⚠️ Lütfen bir belirti girin.")
    else:
        # Hastalıkları ve çözümleri birleştiriyoruz
        hastalik_aciklama = [f"{hastalik}: {cozum}" for hastalik, cozum in zip(hastaliklar, cozumler)]
        hastalik_aciklama.append(user_input)

        # TF-IDF ile eşleşme
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(hastalik_aciklama)
        cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

        # Benzerlik skorunu al
        most_similar_index = np.argmax(cosine_similarities)
        en_benzer_hastalik = hastaliklar[most_similar_index]
        cozum = cozumler[most_similar_index]
        skor = float(np.max(cosine_similarities)) * 100

        # Benzerlik oranını daha doğru almak için SequenceMatcher ile de karşılaştırma yapalım
        similarity_score = similar(user_input, en_benzer_hastalik) * 100

        # Sonuç göster
        st.success(f"✅ En benzer hastalık: **{en_benzer_hastalik}**")
        st.info(f"💡 Önerilen çözüm:\n\n{cozum}")
        st.caption(f"Güven skoru: %{skor:.2f}")
        st.caption(f"Benzerlik oranı (kelime düzeltme ile): %{similarity_score:.2f}")


# Footer
st.markdown("---")
st.caption("🧠 Bu uygulama tıbbı açıdan doğru bilgilerden oluşmaktadır ama ciddi komplikasyonlarda lütfen bir doktara danışınız.")
