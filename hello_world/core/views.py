from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import random
import requests


# Web View - Show Homepage
def homepage(request):
    return render(request, "components/homepage.html")

# Web View - Response from Chatbot
def chatbot(request):
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    context = {'chat_history': request.session['chat_history']}

    if request.method == "POST":
        user_input = request.POST.get('message', '').strip()
        # Get the sentiment analysis
        sentiment = sentiment_analysis(user_input)
        print(sentiment, end = '\n\n')

        # Get the MedicalChatbot response
        chatbot = MedicalChatbot()
        chatbot_response = chatbot.get_response(sentiment['sentiment']['polarity'])
        print(chatbot_response, end = '\n\n')

        if chatbot_response:
            chatbot_response_text = chatbot_response['response']
            bot_response = f"Medibot: '{chatbot_response_text}'"
            request.session['chat_history'].append({'user': user_input, 'bot': chatbot_response_text})
            request.session.modified = True
        else:
            bot_response = "Medibot: I'm sorry, I didn't catch that. Could you say it again?"
            request.session['chat_history'].append({'user': user_input, 'bot': bot_response})
            request.session.modified = True

        context['chat_history'] = request.session['chat_history']

    return render(request, 'data_sci/chatbot.html', context)

# API - Sentimental Analysis from AI for Thai
def sentiment_analysis(text):
    # It is possible that the polarity is empty: for example, using only english word
    url = "https://api.aiforthai.in.th/ssense"

    params = {
        'text': text
    }
    
    # Personal API Key
    headers = {
        'Apikey': "X0022EBklsFzlEKaKE1hZ5BM2GzKdotU"
    }

    response = requests.get(url, headers=headers, params=params)

    return response.json()

# API - Web API for Jokes to cheer up
def geek_jokes_api(request):
    response = requests.get('https://geek-jokes.sameerkumar.website/api?format=json')
    return JsonResponse({'response': response.json()})

# CHATBOT CLASS 
class MedicalChatbot:
    def __init__(self):
        self.chatbot_response_thai = {
            "polarity-neg": [
                "การรู้สถานการณ์ว่าคุณต้องเผชิญกับการตรวจพบโรคเบาหวานนั้นเป็นสิ่งที่น่าเป็นห่วง แต่อย่างไรก็ตาม ยังมีความหวังอยู่ การจัดการโรคเบาหวานเกี่ยวข้องกับการรักษาอาหาร การออกกำลังกาย และบางครั้งอาจต้องใช้ยาและคุณหมอเป็นคนที่สำคัญในการกำหนดแผนที่เหมาะสมกับคุณ",
                "การปฏิบัติตามอาหารสำหรับผู้ป่วยโรคเบาหวานอาจจะยาก โดยเฉพาะในช่วงเริ่มต้น ไม่เป็นไรที่คุณรู้สึกตกใจ การเปลี่ยนแปลงเล็กน้อยที่เป็นความก้าวหน้าบางอย่างบางครั้งก็ดีกว่าการเปลี่ยนแปลงอย่างกระทันหรือเฉียบขาด คิดอาจพิจารณาปรึกษาโซนติวาห์ที่สามารถช่วยให้คุณสร้างแผนอาหารที่เป็นไปได้และที่ทำให้คุณรู้สึกสบายมากขึ้น จำไว้ว่าทุกขั้นตอนเล็กๆ น้อยๆ ก็มีความสำคัญ",
                "ความจริงคือในขณะนี้ยังไม่มีทางรักษาโรคเบาหวานได้ และการรู้สึกเศร้าก็เป็นสิ่งที่อยู่ในกรอบ อย่างไรก็ตาม การจัดการอย่างมีประสิทธิภาพสามารถนำมาสู่คุณภาพชีวิตที่ดีมาก มีหลายทรัพยากรและชุมชนที่ให้การสนับสนุนให้บรรเทาโรคนี้ และการวิจัยต่อเนื่องก็ยังคงพัฒนาด้านการดูแลโรคเบาหวานอยู่"
                "ฉันเข้าใจว่าการจัดการโรคเบาหวานนั้นยาก จำไว้ว่าคุณสามารถมีวันที่ห่วงใยได้ การดำเนินการอย่างละเอียดยิบๆ จะช่วยให้คุณดีขึ้นมาก",
                "การรู้สึกว่ากับงงๆ ก็เป็นสิ่งธรรมดา มาเริ่มต้นด้วยเป้าหมายขนาดเล็กที่สามารถทำได้ ทุกการกระทำที่เป็นบวก ไม่ว่าจะเล็กหรือใหญ่ก็มีความสำคัญ",
                "การรู้สึกท้อใจก็เป็นสิ่งธรรมดา การจัดการโรคเบาหวานเป็นการเดินทาง และการขอความช่วยเหลือก็เป็นสิ่งที่ดี คุณไม่ได้อยู่คนเดียวในสิ่งนี้",
                "การจัดการโรคเบาหวานสามารถที่จะท้าทายได้ จำไว้ว่าการดูแลสุขภาพจิตใจของคุณเป็นสิ่งที่สำคัญด้วย การค้นหาการสนับสนุนจากเพื่อน ครอบครัว หรือผู้เชี่ยวชาญอาจจะเป็นมีประโยชน์อย่างมาก"
            ],
            "polarity-pos": [
                "นี่คือทัศนคติที่ดีมาก! การจัดการโรคเบาหวานอย่างประสบความสำเร็จเกี่ยวข้องกับการรักษาอาหารที่ดี การออกกำลังกายอย่างเป็นประจำ และการตรวจสอบระดับน้ำตาลในเลือดของคุณอย่างสม่ำเสมอ ขึ้นอยู่กับสถานการณ์ของคุณ การใช้ยาอาจจะเป็นสิ่งที่จำเป็นด้วย สำคัญอย่างยิ่งที่คุณจะต้องนัดหมายกับแพทย์ของคุณเป็นประจำเพื่อปรับแผนตามความจำเป็น",
                "เป็นข่าวดีที่คุณกำลังออกกำลังกายอย่างสม่ำเสมอ! การออกกำลังกายเป็นส่วนสำคัญในการจัดการโรคเบาหวาน มันสามารถช่วยควบคุมระดับน้ำตาลในเลือด ลดความเสี่ยงต่อโรคหัวใจและลดความเสี่ยงต่อระบบหัวใจและหลอดเลือด และปรับปรุงความรู้สึกสุขภาพทั่วไป รักษาความพยายามดีๆ และตรวจสอบว่าร่างกายของคุณตอบสนองอย่างไรต่อการออกกำลังกายชนิดต่างๆ",
                "เป็นข่าวดีที่คุณสนใจเทคโนโลยีล่าสุด! มีความคืบหน้าต่อเนื่องในการดูแลโรคเบาหวาน รวมถึงอุปกรณ์ตรวจวัดระดับน้ำตาลในเลือดอย่างต่อเนื่อง ปั๊มอินซูลินอัจฉริยะ และแอพพลิเคชันที่ช่วยติดตามและจัดการระดับน้ำตาลในเลือดของคุณ อุปกรณ์เหล่านี้สามารถทำให้การจัดการโรคเบาหวานเป็นเรื่องที่มีประสิทธิภาพและไม่รบกวนมาก"
                "ทัศนคติที่เป็นบวกของคุณนั้นน่าชื่นชม! การรับมืออย่างมีสติช่วยมากในการจัดการโรคเบาหวานอย่างมีประสิทธิภาพ",
                "ดีมากที่คุณมีทัศนคติที่ดี! การยอมรับวิถีชีวิตที่ดีสามารถทำให้คุณรู้สึกมีอำนาจและมีประโยชน์ต่อการจัดการโรคเบาหวาน",
                "ความกระตือรือร้นของคุณนั้นร่าเริง! จำไว้ว่าทุกครั้งที่คุณตัดสินใจที่ดีเพิ่มขึ้นแล้วคุณก็ได้ใกล้สุขภาพมากขึ้นอีกหนึ่งขั้น",
                "รักสิ่งดีๆ และพลังบวกของคุณนั้นยอดเยี่ยม! ยินดีที่คุณกำลังรับผิดชอบสุขภาพของคุณอย่างดี ขอให้คุณดำเนินการดีต่อไป!"
            ],
            "polarity-none": [
                "ฉันไม่แน่ใจว่าฉันเข้าใจความกังวลของคุณอย่างครบถ้วนหรือไม่ คุณสามารถบอกฉันเพิ่มเติมเกี่ยวกับสิ่งที่คุณรู้สึกหรือคิดอยู่ได้ไหม?",
                "ดูเหมือนว่าคุณอาจมีความรู้สึกผสมผสานเกี่ยวกับนี้ ฉันอยู่ที่นี่เพื่อช่วยเท่าที่จะสามารถ กรุณาติดต่อให้ข้อมูลเพิ่มเติม",
                "ฉันต้องการให้การสนับสนุนที่ดีที่สุดที่ฉันสามารถ แต่ฉันไม่รู้เรื่องอย่างสิ้นเชิงเกี่ยวกับสถานการณ์ของคุณ คุณยินดีที่จะอธิบายเพิ่มเติมหน่อยหรือไม่?",
                "ข้อความของคุณสำคัญสำหรับฉัน แต่ฉันมีความยุ่งยากในการเข้าใจ คุณสามารถให้บางบางบริบทหรือรายละเอียดเพิ่มเติมได้ไหม?",
                "ฉันรู้สึกว่าเป็นปัญหาที่ซับซ้อนสำหรับคุณ ฉันอยู่ที่นี่เพื่อช่วย กรุณาแบ่งปันข้อมูลเพิ่มเติมเพื่อให้ฉันเข้าใจมากขึ้น",
                "ฉันรู้สึกว่ามีสิ่งมากมายเกิดขึ้น หากคุณสามารถให้ข้อมูลเพิ่มเติม ฉันจะทำที่ดีที่สุดในการช่วยคุณ"
            ]
        }
        self.response_length_thai = len(self.chatbot_response_thai['polarity-neg'])

    def get_response(self, polarity: str):

        polarity = polarity.lower().strip()

        if polarity == 'positive':
            query = f'polarity-pos'
        elif polarity == 'negative':
            query = f'polarity-neg'
        else: 
            query = f'polarity-none'

        random_index = random.randint(0, self.response_length_thai - 1)
        if polarity == 'positive':
            chatbot_defalut_res = f"{self.chatbot_response_thai[query][random_index]}"
            response = requests.get('http://localhost:8000/jokes').json()
            print(response)
            jokes = response['response']['joke']
            final_response = chatbot_defalut_res + "\nHere are some jokes to cheer you up:\n" + jokes 
            context =  {
                'polarity': polarity,
                'response': final_response,
            }
        else:
            context =  {
                'polarity': polarity,
                'response': self.chatbot_response_thai[query][random_index]
            }

        return context