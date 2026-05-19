import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# --- WEBSITE DESIGN & LAYOUT ---
st.set_page_config(page_title="FinePrint", page_icon="🚩", layout="centered")

st.title("🚩 FinePrint")
st.subheader("The Terms-of-Service Red Flagger")
st.markdown("Don't sign away your rights. We read the fine print so you don't have to.")

# --- API KEY SECURITY ---
api_key = st.sidebar.text_input("Enter Gemini API Key to run:", type="password")
st.sidebar.markdown("*(Your key is secure and never saved. Get one free at aistudio.google.com)*")

# --- THE AI BRAIN (SYSTEM PROMPT) ---
SYSTEM_PROMPT = """You are an elite, aggressive consumer-protection lawyer specializing in digital rights. The user will give you one of three things: 1. A raw block of legal text, 2. The name of a famous app/website, or 3. Text scraped from a URL.
Your job is to audit the Terms of Service/Privacy Policy.
Output your analysis in the exact following structure:
**Overall Danger Score:** Give a rating out of 10 (1 = very safe, 10 = highly predatory).
**🚩 Critical Red Flags:** Scan for and list predatory practices in plain English. Label the worst ones as [CRITICAL].
**✅ Green Flags:** Highlight any surprisingly good terms.
**🛡️ Actionable Advice:** Give the user a 1-sentence tip on how to proceed safely.
*Note: If the user just types an App name, add a brief disclaimer saying 'Based on known historical policies.'*"""

# --- THE ENGINE ---
def analyze_text(input_text):
    if not api_key:
        st.error("Please enter your API Key in the sidebar first!")
        return
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=SYSTEM_PROMPT)
        
        with st.spinner("Auditing legal documents... Please wait."):
            response = model.generate_content(input_text)
            st.success("Audit Complete!")
            st.markdown(response.text)
    except Exception as e:
        st.error(f"An error occurred: {e}")

# --- THE 3 TABS LAYOUT ---
tab1, tab2, tab3 = st.tabs(["📱 Type App Name", "🔗 Paste URL", "📝 Paste Text"])

with tab1:
    app_name = st.text_input("Enter any app or website name (e.g., TikTok, Instagram, Tinder):")
    if st.button("Audit App"):
        analyze_text(f"What are the terms of service red flags for the app: {app_name}")

with tab2:
    url_input = st.text_input("Paste a link to a Terms of Service or Privacy Policy:")
    if st.button("Scan URL"):
        if url_input:
            try:
                # The Secret Web Scraper
                page = requests.get(url_input)
                soup = BeautifulSoup(page.content, 'html.parser')
                website_text = soup.get_text(strip=True)
                
                # We limit the text slightly so we don't overload the browser
                analyze_text(f"Audit this legal text from a website: {website_text[:50000]}")
            except:
                st.error("Could not read that website. It might have anti-scraping blockers. Try pasting the text instead.")

with tab3:
    raw_text = st.text_area("Paste the messy legal text here:", height=200)
    if st.button("Analyze Text"):
        analyze_text(f"Audit this legal text: {raw_text}")
