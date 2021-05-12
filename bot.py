import json
import os
import telebot
import wolframalpha
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

my_secret = os.environ['api_key']
my_secret1 = os.environ['api_key1']
my_secret2 = os.environ['api_key2']
bot=telebot.TeleBot(my_secret)
client=wolframalpha.Client(my_secret1)
authenticator = IAMAuthenticator(my_secret2)

visual_recognition = VisualRecognitionV3(
    version='2018-03-19',
    authenticator=authenticator)

visual_recognition.set_service_url('https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/80c78105-880f-4bb7-b79c-93764795ee73') 
@bot.message_handler()
def greet(message):
  txt=message.text
  if txt.startswith("https")==True:
    print(message.text)
    try:
      classes = visual_recognition.classify(url=txt).get_result()	
      data=json.dumps(classes,indent=4)
      data2=json.loads(data)
      query=data2["images"][0]['classifiers'][0]["classes"]
      
      ls=[]
      for i in query:
          
          ls.append(i['class'])
          ls.append(i['score'])
      
      ps= ' '.join(map(str, ls))
      bot.send_message(message.chat.id,ps)
    except:
      bot.send_message(message.chat.id,"sorry Image Recognition will only work on images")

  else:
    try:
      query=message.text
      res=client.query(query)
      output=next(res.results).text
      print(output)
    except:
      output="sorry"
    
    bot.send_message(message.chat.id,output)
bot.polling()