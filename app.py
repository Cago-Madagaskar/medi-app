import streamlit as st
from difflib import SequenceMatcher

st.set_page_config(page_title="Medi-Bot", page_icon="💊", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #30353d;
        padding: 2rem;
        border-radius: 10px;
    }
    .stButton > button {
        background-color: #0098b3;
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

st.title("💊 Medi-Bot")
st.markdown("🔍 Aşağıya sahip olduğunuz belirtiyi yazınız ")

user_input = st.text_input("📝 Belirti giriniz:", placeholder="örnek: boğazım ağrıyor, midem bulanıyor...")

def calculate_similarity(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()

if st.button("🚀 Çözüm Bul"):
    if not user_input.strip():
        st.warning("⚠️ Lütfen bir belirti giriniz.")
    else:

        best_match = None
        highest_similarity = 0

        for hastalik in hastaliklar:
            similarity = calculate_similarity(user_input.lower(), hastalik.lower())
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = hastalik

        if best_match and highest_similarity > 0.35:  
            st.success(f"✅ En benzer hastalık: **{best_match}**")
            st.info(f"💡 Önerilen çözüm:\n\n{hastalik_cozum_db[best_match]}")
            st.write(f"🔍 Benzerlik Skoru: %{highest_similarity * 100:.2f}")
        else:
            st.warning("⚠️ Benzer bir hastalık bulunamadı.")
    
st.markdown("---")
st.caption("🧠 Bu uygulama sadece bilgilendirme amaçlıdır. Lütfen ciddi komplikasyonlarda bir doktora danışınız.")

