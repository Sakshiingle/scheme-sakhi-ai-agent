from dotenv import load_dotenv
from google import genai

# Load variables from .env file
load_dotenv()

API_KEY = "GEMINI_API_KEY"
client = genai.Client(api_key=API_KEY)


def get_schemes(language, state, category, age, problem):

    if language.lower() == "hindi":
        lang_instruction = (
            "Reply in simple Hindi language that a rural Indian can understand."
        )
    else:
        lang_instruction = "Reply in simple English language."

    prompt = f"""
You are Scheme Sakhi, a helpful AI agent that helps 
Indian citizens find government schemes they qualify for.

User Details:
- State: {state}
- Category: {category}
- Age: {age} years
- Problem or Need: {problem}

Based on these details, suggest TOP 3 most relevant 
Indian government schemes (central or state level).

For each scheme provide:
1. Scheme Name
2. Simple description in 2 lines
3. Who can apply
4. Official website or how to apply

{lang_instruction}
Keep language simple for rural citizens.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text

    except Exception:
        # Any quota / network / API error → fallback
        return get_fallback(language, category)


def get_fallback(language, category):

    schemes = {
        "farmer": {
            "hindi": """🌾 किसानों के लिए योजनाएं:

1. प्रधानमंत्री फसल बीमा योजना (PMFBY)
   - फसल नुकसान पर बीमा सुरक्षा
   - पात्रता: सभी किसान
   - आवेदन: pmfby.gov.in

2. पीएम किसान सम्मान निधि
   - हर साल ₹6000 की सहायता
   - पात्रता: छोटे और सीमांत किसान
   - आवेदन: pmkisan.gov.in

3. किसान क्रेडिट कार्ड (KCC)
   - कम ब्याज पर खेती लोन
   - पात्रता: सभी किसान
   - आवेदन: नज़दीकी बैंक शाखा""",
            "english": """🌾 Schemes for Farmers:

1. PM Fasal Bima Yojana (PMFBY)
   - Crop insurance against natural disasters
   - Eligibility: All farmers
   - Apply at: pmfby.gov.in

2. PM Kisan Samman Nidhi
   - Rs 6000 per year financial support
   - Eligibility: Small and marginal farmers
   - Apply at: pmkisan.gov.in

3. Kisan Credit Card (KCC)
   - Low interest agricultural loans
   - Eligibility: All farmers
   - Apply at: Nearest bank branch""",
        },
        "student": {
            "hindi": """🎓 छात्रों के लिए योजनाएं:

1. नेशनल स्कॉलरशिप पोर्टल (NSP)
   - केंद्र सरकार की छात्रवृत्ति
   - पात्रता: सभी वर्ग के छात्र
   - आवेदन: scholarships.gov.in

2. पीएम यशस्वी योजना
   - OBC/EBC छात्रों को स्कॉलरशिप
   - पात्रता: 9वीं से 12वीं के छात्र
   - आवेदन: yet.nta.ac.in

3. केंद्रीय सेक्टर स्कीम
   - उच्च शिक्षा के लिए छात्रवृत्ति
   - पात्रता: 12वीं में 80% से अधिक
   - आवेदन: scholarships.gov.in""",
            "english": """🎓 Schemes for Students:

1. National Scholarship Portal (NSP)
   - Central government scholarships
   - Eligibility: Students of all categories
   - Apply at: scholarships.gov.in

2. PM YASASVI Scheme
   - Scholarship for OBC/EBC students
   - Eligibility: Class 9 to 12 students
   - Apply at: yet.nta.ac.in

3. Central Sector Scheme
   - Scholarship for higher education
   - Eligibility: Above 80% in Class 12
   - Apply at: scholarships.gov.in""",
        },
        "woman": {
            "hindi": """👩 महिलाओं के लिए योजनाएं:

1. प्रधानमंत्री मातृ वंदना योजना
   - गर्भवती महिलाओं को ₹5000 सहायता
   - पात्रता: पहले बच्चे की गर्भवती महिला
   - आवेदन: pmmvy.wcd.gov.in

2. बेटी बचाओ बेटी पढ़ाओ
   - बालिका शिक्षा और सुरक्षा
   - पात्रता: सभी बालिकाएं
   - आवेदन: wcdhry.gov.in

3. महिला शक्ति केंद्र
   - महिला उद्यमिता और कौशल विकास
   - पात्रता: ग्रामीण महिलाएं
   - आवेदन: wcd.nic.in""",
            "english": """👩 Schemes for Women:

1. PM Matru Vandana Yojana
   - Rs 5000 support for pregnant women
   - Eligibility: First time pregnant women
   - Apply at: pmmvy.wcd.gov.in

2. Beti Bachao Beti Padhao
   - Girl child education and protection
   - Eligibility: All girl children
   - Apply at: wcdhry.gov.in

3. Mahila Shakti Kendra
   - Women entrepreneurship and skill dev
   - Eligibility: Rural women
   - Apply at: wcd.nic.in""",
        },
        "senior citizen": {
            "hindi": """👴 वरिष्ठ नागरिकों के लिए योजनाएं:

1. इंदिरा गांधी राष्ट्रीय वृद्धावस्था पेंशन
   - हर महीने पेंशन सहायता
   - पात्रता: 60 वर्ष से अधिक BPL नागरिक
   - आवेदन: nsap.nic.in

2. वरिष्ठ पेंशन बीमा योजना
   - गारंटीड पेंशन योजना
   - पात्रता: 60 वर्ष से अधिक
   - आवेदन: licindia.in

3. राष्ट्रीय स्वास्थ्य बीमा योजना
   - मुफ्त स्वास्थ्य बीमा
   - पात्रता: BPL परिवार
   - आवेदन: nha.gov.in""",
            "english": """👴 Schemes for Senior Citizens:

1. Indira Gandhi National Old Age Pension
   - Monthly pension assistance
   - Eligibility: BPL citizens above 60 years
   - Apply at: nsap.nic.in

2. Varishtha Pension Bima Yojana
   - Guaranteed pension scheme
   - Eligibility: Above 60 years
   - Apply at: licindia.in

3. National Health Insurance Scheme
   - Free health insurance coverage
   - Eligibility: BPL families
   - Apply at: nha.gov.in""",
        },
    }

    cat = category.lower()
    if cat not in schemes:
        cat = "farmer"

    lang = "hindi" if language.lower() == "hindi" else "english"

    if lang == "hindi":
        header = "⚠️ अभी AI व्यस्त है। यहाँ प्रासंगिक योजनाएं हैं:\n\n"
    else:
        header = "⚠️ AI busy. Here are relevant schemes:\n\n"

    return header + schemes[cat][lang]


if __name__ == "__main__":
    print("Testing Scheme Sakhi Agent...")
    print("-" * 50)

    result = get_schemes(
        language="hindi",
        state="Maharashtra",
        category="farmer",
        age="45",
        problem="Need financial help after crop damage",
    )
    print(result)
    print("\n" + "=" * 50 + "\n")

    result = get_schemes(
        language="english",
        state="Delhi",
        category="student",
        age="20",
        problem="Need scholarship for college",
    )
    print(result)
