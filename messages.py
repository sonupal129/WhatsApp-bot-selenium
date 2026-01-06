
def get_all_message_templates():
    messages = {key: value for key, value in globals().items() if not key.startswith("__") and not callable(value)}
    return messages


LAVANYA_ENGLISH = """Hello {name},

Greetings from LaviPro : Lavanya Enterprises!
Thank you for showing interest in our Electric Insect Killer products on TradeIndia.

We manufacture high-quality, durable, and eco-friendly insect killers designed for homes, offices, restaurants, and outdoor spaces.
** Available in 1 ft, 1.25 ft, 1.5 ft & 2 ft sizes
** Powerful UV Tubes (20W-40W)
** Chemical-Free | Metal Body | 1-Year Warranty
** MOQ: 10 Units | Special prices for bulk orders

You can explore all our products at:
www.lavanyaent.com

Please let us know your requirements or if you would like a quote. We'd love to assist you further!

Thanks & Regards,
Son Pal
+91 8882897947
Lavanya Enterprises | Brand: LaviPro
"""


LAVANYA_HINDI = """नमस्ते {name},

{enquiry_from} पर आपकी इन्क्वारी मिली थी की आप सॉफ्ट टॉयज और बच्चो के स्कूल बैग्स देख रहे हैं।

मैं सोनपाल हूँ, Lavanya Enterprises से, जो कि नई दिल्ली में स्थित है। हम उच्च गुणवत्ता वाले सॉफ्ट टॉयज़, प्लश टॉयज़, और बच्चों के स्कूल बैग्स के निर्माता हैं। 15+ साल के अनुभव के साथ, हम सुनिश्चित करते हैं कि हमारे प्रोडक्ट्स बच्चों को बहुत पसंद आएं!

हम स्टैंडर्ड आइटम्स या कस्टम डिज़ाइन भी बनाते हैं । हमारे प्रोडक्ट्स की कीमतें ₹40 INR से शुरू होती हैं, जो हमारे उत्पादों को किफायती और आकर्षक बनाती हैं।

हमारे प्रोडक्ट्स कैटलॉग को नीचे दिए गए लिंक पर जाकर देख सकते हैं : 

https://drive.google.com/drive/folders/1agZlGtJW84CiZu6kG_xcINo3O_YyAmBg?usp=sharing

आप हमारी वेबसाइट से भी हम से संपर्क कर सकते हैं: 

www.lavanyacrafts.com

आप यहाँ रिप्लाई कर सकते हैं, या मुझे +91 8882897947 पर कॉल/व्हाट्सएप कर सकते हैं।

सोनपाल
Lavanya Enterprises
"""


