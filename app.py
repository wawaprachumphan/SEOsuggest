import streamlit as st
import google.generativeai as genai
from docx import Document
from dotenv import load_dotenv
import os

# โหลด API Key จากไฟล์ .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ ไม่พบ API Key กรุณาตั้งค่า GEMINI_API_KEY ในไฟล์ .env")
    st.stop()

genai.configure(api_key=api_key)

# อ่านเนื้อหาจากไฟล์ .docx
def read_docx(file):
    doc = Document(file)
    full_text = [para.text for para in doc.paragraphs]
    return "\n".join(full_text)

# ขอคำแนะนำ SEO จาก Gemini
def get_seo_suggestions(content):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    prompt = f"""
Please read the following content and suggest SEO improvements.
Your response should include:
- Suggested keywords
- Meta description
- Title tag suggestion
- Readability tips
- Structure (e.g., use of headings)

Content:
{content}
"""
    response = model.generate_content(prompt)
    return response.text

# UI
st.set_page_config(page_title="Gemini SEO Suggestor", layout="centered")
st.title("📄🔍 SEO Suggestion จาก Gemini 1.5 Flash")

# ตัวเลือกวิธีป้อนเนื้อหา
option = st.radio("เลือกวิธีการใส่เนื้อหา:", ["📤 อัปโหลดไฟล์ .docx", "⌨️ พิมพ์หรือวางเนื้อหา"])

text = ""

# ถ้าเลือกอัปโหลดไฟล์
if option == "📤 อัปโหลดไฟล์ .docx":
    uploaded_file = st.file_uploader("อัปโหลดไฟล์ .docx", type=["docx"])
    if uploaded_file is not None:
        with st.spinner("กำลังอ่านเนื้อหาจากไฟล์..."):
            try:
                text = read_docx(uploaded_file)
                st.success("โหลดเนื้อหาสำเร็จ ✅")
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")

# ถ้าเลือกพิมพ์หรือวางเนื้อหา
elif option == "⌨️ พิมพ์หรือวางเนื้อหา":
    text = st.text_area("ใส่เนื้อหาที่นี่:", "", height=300)

# แสดงกล่องและปุ่มวิเคราะห์
if text:
    st.text_area("📄 เนื้อหาที่จะวิเคราะห์:", text, height=300)
    if st.button("ขอคำแนะนำ SEO จาก Gemini"):
        with st.spinner("กำลังวิเคราะห์ด้วย Gemini 1.5 Flash..."):
            try:
                suggestions = get_seo_suggestions(text)
                st.subheader("📌 คำแนะนำ SEO")
                st.markdown(suggestions)
            except Exception as e:
                st.error(f"❌ เกิดข้อผิดพลาดจาก Gemini API: {e}")
