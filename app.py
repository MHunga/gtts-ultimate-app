import streamlit as st
from gtts import gTTS
import gtts.lang
import io

# Cấu hình trang Web
st.set_page_config(page_title="Ultimate TTS Studio", page_icon="🎙️", layout="centered")

st.title("🎙️ Ultimate TTS Studio")
st.markdown("Dự án sử dụng **mọi tính năng** của thư viện `gTTS` trong Python.")

# ---------------------------------------------------------
# TÍNH NĂNG 1: LẤY TẤT CẢ NGÔN NGỮ HỖ TRỢ (tts_langs)
# ---------------------------------------------------------
@st.cache_data
def get_languages():
    return gtts.lang.tts_langs()

supported_langs = get_languages()
# Tạo list hiển thị kiểu: "vi - Vietnamese", "en - English"
lang_options = [f"{code} - {name}" for code, name in supported_langs.items()]

# ---------------------------------------------------------
# GIAO DIỆN NGƯỜI DÙNG (UI)
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    # Chọn ngôn ngữ
    selected_lang = st.selectbox("🌐 Chọn Ngôn ngữ:", lang_options, index=lang_options.index("vi - Vietnamese"))
    lang_code = selected_lang.split(" - ")[0]

with col2:
    # ---------------------------------------------------------
    # TÍNH NĂNG 2: ĐỔI ACCENT/GIỌNG ĐỌC QUA TLD (Top-level domain)
    # Tính năng này đặc biệt hiệu quả với tiếng Anh, Tây Ban Nha...
    # ---------------------------------------------------------
    tld_dict = {
        "Mỹ (Mặc định - com)": "com",
        "Anh Quốc (co.uk)": "co.uk",
        "Úc (com.au)": "com.au",
        "Ấn Độ (co.in)": "co.in",
        "Canada (ca)": "ca",
        "Nigeria (com.ng)": "com.ng"
    }
    
    if lang_code == 'en':
        selected_tld_key = st.selectbox("🗣️ Chọn Accent (Chỉ cho tiếng Anh):", list(tld_dict.keys()))
        tld_code = tld_dict[selected_tld_key]
    else:
        st.info("Tính năng Accent (TLD) hoạt động rõ nhất với tiếng Anh (en).")
        tld_code = "com" # Mặc định

# ---------------------------------------------------------
# TÍNH NĂNG 3: ĐIỀU CHỈNH TỐC ĐỘ ĐỌC (slow)
# ---------------------------------------------------------
is_slow = st.checkbox("🐢 Đọc chậm (Slow mode)")

# Nhập văn bản
text_input = st.text_area("📝 Nhập văn bản cần chuyển thành giọng nói:", height=150, 
                          placeholder="Nhập một đoạn văn bản dài vào đây. gTTS sẽ tự động chia nhỏ (tokenize) để đọc mượt mà...")

# Nút xử lý
if st.button("🚀 Tạo Giọng Nói", use_container_width=True):
    if not text_input.strip():
        st.warning("Vui lòng nhập văn bản trước!")
    else:
        with st.spinner("Đang tạo âm thanh..."):
            try:
                # ---------------------------------------------------------
                # TÍNH NĂNG 4 & 5: KHỞI TẠO gTTS VỚI MỌI THAM SỐ 
                # (Text dài được gTTS tự động xử lý bằng Tokenizer bên dưới)
                # ---------------------------------------------------------
                tts = gTTS(
                    text=text_input, 
                    lang=lang_code, 
                    tld=tld_code, 
                    slow=is_slow
                )
                
                # ---------------------------------------------------------
                # TÍNH NĂNG 6: GHI RA BYTE STREAM (write_to_fp)
                # Giúp Web App không bị đầy ổ cứng do sinh ra quá nhiều file mp3
                # ---------------------------------------------------------
                audio_bytes_io = io.BytesIO()
                tts.write_to_fp(audio_bytes_io)
                
                # Đưa con trỏ file về đầu để đọc
                audio_bytes_io.seek(0)
                
                st.success("Tạo thành công!")
                
                # Phát âm thanh trực tiếp trên web
                st.audio(audio_bytes_io, format='audio/mp3')
                
                # Nút tải xuống
                st.download_button(
                    label="💾 Tải file MP3 xuống",
                    data=audio_bytes_io,
                    file_name="gTTS_output.mp3",
                    mime="audio/mp3"
                )
            except Exception as e:
                st.error(f"Đã xảy ra lỗi: {e}")

st.markdown("---")
st.caption("Được xây dựng bằng Python, gTTS và Streamlit.")