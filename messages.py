
def get_all_message_templates():
    messages = {key: value for key, value in globals().items() if not key.startswith("__") and not callable(value)}
    return messages


LAVANYA_ENGLISH = """Hello {name},

We received your inquiry on {enquiry_from} that you are looking for soft toys and kids school bags.

I am Sonpal from Lavanya Enterprises, based in New Delhi. We are a manufacturer of high quality soft toys, plush toys, and kids school bags. With 15+ years of experience, we make sure that our products are loved by kids!

We also manufacture standard items or custom designs. Our product prices start from ₹40 INR, which makes our products affordable and attractive.

Our products catalogue can be viewed by visiting the link given below:

https://drive.google.com/drive/folders/1agZlGtJW84CiZu6kG_xcINo3O_YyAmBg?usp=sharing

You can also contact us from our website:

www.lavanyacrafts.com

You can reply here, or call/whatsapp me on +91 8882897947.

Sonpal
Lavanya Enterprises
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


