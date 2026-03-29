import os
import re
from dotenv import load_dotenv
from groq import Groq

# Load variables from .env file
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY)

def get_schemes(user_profile):
    language = user_profile.get("language", "english")
    state    = user_profile.get("state", "")
    category = user_profile.get("category", "")
    age      = user_profile.get("age", "")
    problem  = user_profile.get("problem", "")

    if language.lower() == "hindi":
        lang_instruction = "Use very simple Hindi words that a rural citizen can understand."
    else:
        lang_instruction = "Use very simple English. Avoid difficult words."

    prompt = f"""
You are Scheme Sakhi, an AI agent that recommends Indian government schemes.

Your job:
- Read the user profile carefully.
- Find central and state schemes that truly match.
- Return exactly 3 schemes, not more, not less.

User profile:
- State: {state}
- Category: {category}
- Age: {age}
- Main problem or need: {problem}
- Preferred language: {language}

Rules:
- Only suggest real Indian government schemes.
- If you are not confident, return one scheme with name NO_CLEAR_SCHEMES.
- Do NOT invent fake websites.

Output format:

Scheme 1: <scheme name>
Description: <2 lines maximum>
Eligibility: <who can apply>
Apply: <official website like domain.gov.in>

Scheme 2: <scheme name>
Description: <2 lines maximum>
Eligibility: <who can apply>
Apply: <official website like domain.gov.in>

Scheme 3: <scheme name>
Description: <2 lines maximum>
Eligibility: <who can apply>
Apply: <official website like domain.gov.in>

{lang_instruction}
Keep sentences short and clear for rural citizens.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Scheme Sakhi, a helpful AI agent for Indian government schemes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        text = response.choices[0].message.content or ""

        if "NO_CLEAR_SCHEMES" in text:
            return get_fallback(language, category)

        # Make ANY domain looking like a website clickable automatically
        def repl(match):
            url = match.group(0)
            if not url.startswith("http"):
                full_url = "https://" + url
            else:
                full_url = url
            return f'<a href="{full_url}" target="_blank" style="color:#ff9933; text-decoration:none; font-weight:bold;">{url}</a>'
            
        # This regex finds domain names (like pmkisan.gov.in or https://pmkisan.gov.in)
        url_pattern = r"(https?://[^\s]+|[a-zA-Z0-9.-]+\.gov\.in|[a-zA-Z0-9.-]+\.nic\.in|[a-zA-Z0-9.-]+\.co\.in|[a-zA-Z0-9.-]+\.in)"
        text = re.sub(url_pattern, repl, text)

        return text

    except Exception as e:
        print(f"Groq error: {e}")
        return get_fallback(language, category)


def get_fallback(language, category):
    schemes = {
        "farmer": {
            "hindi": """🌾 किसानों के लिए योजनाएं:

Scheme 1: प्रधानमंत्री फसल बीमा योजना (PMFBY)
Description: फसल नुकसान पर बीमा सुरक्षा देती है। प्राकृतिक आपदा में मुआवजा मिलता है।
Eligibility: सभी किसान जो खेती करते हैं
Apply: <a href="https://pmfby.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">pmfby.gov.in</a>

Scheme 2: पीएम किसान सम्मान निधि
Description: हर साल ₹6000 की आर्थिक सहायता तीन किश्तों में मिलती है।
Eligibility: छोटे और सीमांत किसान
Apply: <a href="https://pmkisan.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">pmkisan.gov.in</a>

Scheme 3: किसान क्रेडिट कार्ड (KCC)
Description: कम ब्याज दर पर खेती के लिए लोन। आपातकाल में भी सहायक।
Eligibility: सभी किसान
Apply: नज़दीकी बैंक शाखा में जाएं""",
            "english": """🌾 Schemes for Farmers:

Scheme 1: PM Fasal Bima Yojana (PMFBY)
Description: Crop insurance against natural disasters. Compensation for crop damage.
Eligibility: All farmers engaged in cultivation
Apply: <a href="https://pmfby.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">pmfby.gov.in</a>

Scheme 2: PM Kisan Samman Nidhi
Description: Financial support of Rs 6000 per year in three installments.
Eligibility: Small and marginal farmers
Apply: <a href="https://pmkisan.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">pmkisan.gov.in</a>

Scheme 3: Kisan Credit Card (KCC)
Description: Low interest agricultural loans for farming needs and emergencies.
Eligibility: All farmers
Apply: Visit nearest bank branch"""
        },
        "student": {
            "hindi": """🎓 छात्रों के लिए योजनाएं:

Scheme 1: नेशनल स्कॉलरशिप पोर्टल (NSP)
Description: केंद्र सरकार की सभी छात्रवृत्तियां एक जगह। आवेदन आसान है।
Eligibility: सभी वर्ग के छात्र
Apply: <a href="https://scholarships.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">scholarships.gov.in</a>

Scheme 2: पीएम यशस्वी योजना
Description: OBC और EBC छात्रों को उच्च शिक्षा के लिए छात्रवृत्ति।
Eligibility: 9वीं से 12वीं के OBC/EBC छात्र
Apply: <a href="https://yet.nta.ac.in" target="_blank" style="color:#ff9933; font-weight:bold;">yet.nta.ac.in</a>

Scheme 3: केंद्रीय सेक्टर स्कीम
Description: 12वीं में 80% से अधिक अंक लाने वाले छात्रों को सहायता।
Eligibility: 12वीं उत्तीर्ण मेधावी छात्र
Apply: <a href="https://scholarships.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">scholarships.gov.in</a>""",
            "english": """🎓 Schemes for Students:

Scheme 1: National Scholarship Portal (NSP)
Description: All central government scholarships in one place. Easy to apply online.
Eligibility: Students of all categories
Apply: <a href="https://scholarships.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">scholarships.gov.in</a>

Scheme 2: PM YASASVI Scheme
Description: Scholarship for OBC and EBC students for higher education support.
Eligibility: Class 9 to 12 OBC/EBC students
Apply: <a href="https://yet.nta.ac.in" target="_blank" style="color:#ff9933; font-weight:bold;">yet.nta.ac.in</a>

Scheme 3: Central Sector Scheme
Description: Financial support for meritorious students scoring above 80% in Class 12.
Eligibility: Meritorious students after Class 12
Apply: <a href="https://scholarships.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">scholarships.gov.in</a>"""
        },
        "woman": {
            "hindi": """👩 महिलाओं के लिए योजनाएं:

Scheme 1: प्रधानमंत्री मातृ वंदना योजना
Description: पहले बच्चे पर गर्भवती महिलाओं को ₹5000 की सहायता।
Eligibility: पहली बार गर्भवती महिला
Apply: <a href="https://pmmvy.wcd.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">pmmvy.wcd.gov.in</a>

Scheme 2: बेटी बचाओ बेटी पढ़ाओ
Description: बालिकाओं की शिक्षा और सुरक्षा के लिए राष्ट्रीय अभियान।
Eligibility: सभी बालिकाएं
Apply: <a href="https://wcdhry.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">wcdhry.gov.in</a>

Scheme 3: महिला शक्ति केंद्र
Description: ग्रामीण महिलाओं के लिए कौशल विकास और उद्यमिता सहायता।
Eligibility: ग्रामीण क्षेत्र की महिलाएं
Apply: <a href="https://wcd.nic.in" target="_blank" style="color:#ff9933; font-weight:bold;">wcd.nic.in</a>""",
            "english": """👩 Schemes for Women:

Scheme 1: PM Matru Vandana Yojana
Description: Rs 5000 support for first-time pregnant women in installments.
Eligibility: First time pregnant women
Apply: <a href="https://pmmvy.wcd.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">pmmvy.wcd.gov.in</a>

Scheme 2: Beti Bachao Beti Padhao
Description: National campaign for girl child education and protection.
Eligibility: All girl children
Apply: <a href="https://wcdhry.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">wcdhry.gov.in</a>

Scheme 3: Mahila Shakti Kendra
Description: Skill development and entrepreneurship support for rural women.
Eligibility: Rural women
Apply: <a href="https://wcd.nic.in" target="_blank" style="color:#ff9933; font-weight:bold;">wcd.nic.in</a>"""
        },
        "senior citizen": {
            "hindi": """👴 वरिष्ठ नागरिकों के लिए योजनाएं:

Scheme 1: इंदिरा गांधी राष्ट्रीय वृद्धावस्था पेंशन
Description: BPL वरिष्ठ नागरिकों को हर महीने पेंशन सहायता।
Eligibility: 60 वर्ष से अधिक BPL नागरिक
Apply: <a href="https://nsap.nic.in" target="_blank" style="color:#ff9933; font-weight:bold;">nsap.nic.in</a>

Scheme 2: वरिष्ठ पेंशन बीमा योजना (LIC)
Description: LIC द्वारा गारंटीड मासिक पेंशन योजना।
Eligibility: 60 वर्ष से अधिक नागरिक
Apply: <a href="https://licindia.in" target="_blank" style="color:#ff9933; font-weight:bold;">licindia.in</a>

Scheme 3: आयुष्मान भारत योजना
Description: सालाना ₹5 लाख तक का मुफ्त स्वास्थ्य बीमा।
Eligibility: BPL और निम्न आय परिवार
Apply: <a href="https://pmjay.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">pmjay.gov.in</a>""",
            "english": """👴 Schemes for Senior Citizens:

Scheme 1: Indira Gandhi National Old Age Pension
Description: Monthly pension support for BPL senior citizens across India.
Eligibility: BPL citizens above 60 years
Apply: <a href="https://nsap.nic.in" target="_blank" style="color:#ff9933; font-weight:bold;">nsap.nic.in</a>

Scheme 2: Varishtha Pension Bima Yojana (LIC)
Description: Guaranteed monthly pension scheme managed by LIC of India.
Eligibility: Citizens above 60 years
Apply: <a href="https://licindia.in" target="_blank" style="color:#ff9933; font-weight:bold;">licindia.in</a>

Scheme 3: Ayushman Bharat Yojana
Description: Free health insurance up to Rs 5 lakh per year for families.
Eligibility: BPL and low income families
Apply: <a href="https://pmjay.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">pmjay.gov.in</a>"""
        },
        "BPL": {
            "hindi": """🏠 BPL परिवारों के लिए योजनाएं:

Scheme 1: आयुष्मान भारत योजना
Description: ₹5 लाख तक का मुफ्त इलाज सरकारी और निजी अस्पतालों में।
Eligibility: BPL परिवार
Apply: <a href="https://pmjay.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">pmjay.gov.in</a>

Scheme 2: प्रधानमंत्री आवास योजना (ग्रामीण)
Description: गरीब परिवारों को पक्का घर बनाने के लिए सहायता।
Eligibility: BPL और बेघर परिवार
Apply: <a href="https://pmayg.nic.in" target="_blank" style="color:#ff9933; font-weight:bold;">pmayg.nic.in</a>

Scheme 3: उज्ज्वला योजना
Description: BPL महिलाओं को मुफ्त LPG गैस कनेक्शन।
Eligibility: BPL परिवार की महिला
Apply: <a href="https://pmuy.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">pmuy.gov.in</a>""",
            "english": """🏠 Schemes for BPL Families:

Scheme 1: Ayushman Bharat Yojana
Description: Free medical treatment up to Rs 5 lakh at government and private hospitals.
Eligibility: BPL families
Apply: <a href="https://pmjay.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">pmjay.gov.in</a>

Scheme 2: PM Awas Yojana (Gramin)
Description: Financial assistance to build permanent houses for poor families.
Eligibility: BPL and homeless families
Apply: <a href="https://pmayg.nic.in" target="_blank" style="color:#ff9933; font-weight:bold;">pmayg.nic.in</a>

Scheme 3: Ujjwala Yojana
Description: Free LPG gas connection for BPL women to replace traditional fuel.
Eligibility: Women from BPL families
Apply: <a href="https://pmuy.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">pmuy.gov.in</a>"""
        },
        "general": {
            "hindi": """📋 सामान्य नागरिकों के लिए योजनाएं:

Scheme 1: आयुष्मान भारत योजना
Description: ₹5 लाख तक का मुफ्त स्वास्थ्य बीमा।
Eligibility: पात्र परिवार
Apply: <a href="https://pmjay.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">pmjay.gov.in</a>

Scheme 2: अटल पेंशन योजना
Description: असंगठित क्षेत्र के लोगों के लिए पेंशन योजना।
Eligibility: 18-40 वर्ष के नागरिक
Apply: <a href="https://npscra.nsdl.co.in" target="_blank" style="color:#ff9933; font-weight:bold;">npscra.nsdl.co.in</a>

Scheme 3: प्रधानमंत्री जीवन ज्योति बीमा
Description: ₹2 लाख का जीवन बीमा केवल ₹436 प्रति वर्ष में।
Eligibility: 18-50 वर्ष के बैंक खाताधारक
Apply: नज़दीकी बैंक""",
            "english": """📋 Schemes for General Citizens:

Scheme 1: Ayushman Bharat Yojana
Description: Free health insurance up to Rs 5 lakh per year.
Eligibility: Eligible families as per government list
Apply: <a href="https://pmjay.gov.in" target="_blank" style="color:#ff9933; font-weight:bold;">pmjay.gov.in</a>

Scheme 2: Atal Pension Yojana
Description: Pension scheme for workers in unorganized sector.
Eligibility: Citizens between 18-40 years
Apply: <a href="https://npscra.nsdl.co.in" target="_blank" style="color:#ff9933; font-weight:bold;">npscra.nsdl.co.in</a>

Scheme 3: PM Jeevan Jyoti Bima Yojana
Description: Life insurance of Rs 2 lakh at only Rs 436 per year.
Eligibility: Bank account holders between 18-50 years
Apply: Visit nearest bank branch"""
        }
    }

    cat = category.lower()
    if cat not in schemes:
        cat = "general"

    lang   = "hindi" if language.lower() == "hindi" else "english"
    header = "⚠️ AI व्यस्त है। यहाँ प्रासंगिक योजनाएं हैं:\n\n" if lang == "hindi" else "⚠️ AI busy. Here are relevant schemes:\n\n"

    return header + schemes[cat][lang]


if __name__ == "__main__":
    profile = {
        "language": "english",
        "state": "Maharashtra",
        "category": "farmer",
        "age": "45",
        "problem": "Need financial help",
    }
    print(get_schemes(profile))
