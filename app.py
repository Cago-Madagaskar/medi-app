import streamlit as st
from difflib import SequenceMatcher

# Sayfa ayarları
st.set_page_config(page_title="Medi-Bot", page_icon="💊", layout="centered")

# Stil
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 15px;
    }
    .stButton > button {
        background-color: #0098b3;
        color: white;
        padding: 12px 20px;
        border-radius: 10px;
        font-size: 18px;
        margin-top: 20px;
    }
    .stTextInput > div > input {
        padding: 12px;
        border-radius: 10px;
        font-size: 18px;
        border: 1px solid #adacbf;
        margin-top: 20px;
    }
    .stTextInput > div > input:focus {
        border-color: #0098b3;
    }
    .stMarkdown {
        font-size: 18px;
        color: #333;
    }
    .stSuccess {
        color: #0098b3;
        font-weight: bold;
    }
    .stWarning {
        color: #e74c3c;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Hastalık ve çözüm veritabanı
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

# Hastalıklar ve çözümler listeleri
hastaliklar = list(hastalik_cozum_db.keys())
cozumler = list(hastalik_cozum_db.values())

# Başlık ve açıklama
st.title("💊 Medi-Bot")
st.markdown("""
    🔍 **Hastalık Çözüm Asistanı'na** hoş geldiniz. 
    Aşağıya sahip olduğunuz belirtinizi girin, size en yakın hastalığı bulalım ve çözüm önerelim.
""")

# Kullanıcıdan girdiyi al
user_input = st.text_input("📝 **Belirti giriniz:**", placeholder="Örnek: boğazım ağrıyor, midem bulanıyor...")

# SequenceMatcher ile benzerlik hesaplama fonksiyonu
def calculate_similarity(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()

# Buton tıklama durumunda
if st.button("🚀 **Çözüm Bul**"):
    if not user_input.strip():
        st.warning("⚠️ **Lütfen bir belirti girin.**")
    else:
        best_match = None
        highest_similarity = 0

        for hastalik in hastaliklar:
            similarity = calculate_similarity(user_input.lower(), hastalik.lower())
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = hastalik

        if best_match and highest_similarity > 0.4:  
            st.success(f"✅ **En benzer hastalık:** {best_match}")
            st.info(f"💡 **Önerilen çözüm:**\n\n{hastalik_cozum_db[best_match]}")
            st.write(f"🔍 **Benzerlik Skoru:** %{highest_similarity * 100:.2f}")
        else:
            st.warning("⚠️ **Benzer bir hastalık bulunamadı.**")

# Footer
st.markdown("---")
st.caption("🧠 Bu uygulama sadece bilgilendirme amaçlıdır. **Lütfen ciddi durumlar için bir doktora danışın.**")

