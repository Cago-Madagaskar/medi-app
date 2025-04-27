import streamlit as st
from difflib import SequenceMatcher

st.set_page_config(page_title="Medi-Bot", page_icon="💊", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #30353d;
        color: white;
    }
    .main {
        background-color: #30353d;
        padding: 2rem;
        border-radius: 15px;
        color: white;
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
        background-color: #3b3f4a;
        color: white;
        border: 1px solid #adacbf;
        margin-top: 20px;
    }
    .stTextInput > div > input:focus {
        border-color: #6e6e73;
    }
    .stMarkdown, .stSuccess, .stWarning, .stInfo, .stCaption {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Hastalık veritabanı
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

st.title("💊 Medi-Bot")
st.markdown("""
    🔍 **Hastalık Çözüm Asistanı'na** hoş geldiniz. 
    Aşağıya sahip olduğunuz belirtinizi girin, size en yakın hastalığı bulalım ve çözüm önerelim.
""")

user_input = st.text_input("📝 **Belirti giriniz:**", placeholder="Örnek: boğazım ağrıyor, midem bulanıyor...")

def calculate_similarity(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()

if st.button("🚀 **Çözüm Bul**"):
    if not user_input.strip():
        st.warning("⚠️ **Lütfen bir belirti girin.**")
    else:
        best_match = None
        highest_similarity = 0

        for hastalik in hastaliklar:
            if hastalik in user_input.lower():
                best_match = hastalik
                highest_similarity = 1.0
                break  
            else:
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

st.markdown("---")
st.caption("🧠 Bu uygulama sadece bilgilendirme amaçlıdır. **Ciddi durumlarda lütfen doktora danışınız.**")

