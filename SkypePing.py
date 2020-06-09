from skpy import SkypeEventLoop, SkypeNewMessageEvent, Skype, SkypePresenceEvent
import requests
from datetime import date
import datetime
import json
from googletrans import Translator
import wikipedia
import random
import feedparser
from gtts import gTTS
import os
from googletrans.constants import DEFAULT_USER_AGENT, LANGCODES, LANGUAGES, SPECIAL_CASES
import time
from env import UP

Skype(UP['u'], UP['p'], "token")

wikipedia.set_lang("vi")
translator = Translator()
l = ''


def getHeadlines(rss_url):
    headlines = []
    feed = feedparser.parse(rss_url)
    for newsitem in feed['items']:
        headlines.append(newsitem['title'])
    return headlines


class SkypePing(SkypeEventLoop):
    def onEvent(self, event):
        if isinstance(event, SkypeNewMessageEvent) and not event.msg.userId == self.userId:
            l = event
            msg = event.msg.content.lower()
            if "8:live:supermariogalaxy282" in msg:
                event.msg.chat.sendMsg(
                    'Đừng ping em mk, có j mình inbox riêng nha')
                event.msg.chat.sendMsg('hihi ....')
            key = msg.split(' ')[0]
            if key != "umaru":
                return
            if key in "tắt đi":
                ck = True

                return
            if "umaru ngu" in msg:
                event.msg.chat.sendMsg('Ngu cái dm màyyy ..')

                # image_url = 'https://media1.tenor.com/images/2e547c50d6aa40150207b4961316d978/tenor.gif'
                # img_data = requests.get(image_url).content
                # img_name = 'umaru.png'
                # with open(img_name, 'wb') as handler:
                #     handler.write(img_data)

                # event.msg.chat.sendFile(open(img_name, "rb"), '', 'image')
                # event.msg.chat.setTyping(active=True)

                # event.msg.chat.setTyping(active=True)
                event.msg.chat.sendMsg(
                    'Đấy là nếu là người ta sẽ nói như thế.')
                event.msg.chat.sendMsg(
                    'Còn em thì ko dám, a Dương oánh chết ...')
            if "lên nhạc" in msg:
                # print(msg)
                search = msg.split('umaru lên nhạc')[1].strip().lower()
                header = {
                    "x-rapidapi-key": "dc451b9bf1msh0ddb2bcf20dfa99p1842e2jsnaf778e768354"
                }
                musicString = requests.get(
                    'https://deezerdevs-deezer.p.rapidapi.com/search?q=' + search, headers=header).content.decode('utf-8')

                music = json.loads(musicString)['data']
                if len(music) == 0:
                    event.msg.chat.sendMsg(
                        'Umaru bài j cũng biết. Chỉ có bài này là không biết ...')
                    return
                # item = random.choice(music)
                item = ''
                for x in music:
                    if search in x['title'].strip().lower():
                        item = x
                        break
                if item == '':
                    event.msg.chat.sendMsg(
                        'Em tìm hổng ra bài này. Hic hic ...')
                    return
                    # print(index['preview'])
                audio_url = item.get('preview')
                audio_data = requests.get(audio_url).content
                audio_name = search + '.mp3'

                artist_name = item['artist']['name']
                with open(audio_name, 'wb') as handler:
                    handler.write(audio_data)

                image_url = item['artist']['picture_medium']
                img_data = requests.get(image_url).content
                img_name = search + '.png'
                with open(img_name, 'wb') as handler:
                    handler.write(img_data)

                event.msg.chat.sendMsg(artist_name)
                event.msg.chat.sendFile(
                    open(img_name, "rb"), img_name, 'image')
                event.msg.chat.sendFile(
                    open(audio_name, "rb"), audio_name, False, True)
                os.remove(img_name)
                os.remove(audio_name)

                # print(music)
                # with open('music.txt', 'wb') as handler:
                #     handler.write('music.txt')
                # list = []
                # for x in music:
                #     list.append(x['title'])
                # print(list)

            if "trans list" in msg:
                event.msg.chat.sendMsg(LANGUAGES)
            if "trans to" in msg:
                text1 = event.msg.content.split('to')[1]
                text = text1.split(':')
                dest_lang = text[0].strip()
                src_content = text[1].strip()
                trans = translator.translate(src_content, dest=dest_lang)
                dest_lang_label = LANGUAGES.get(dest_lang)
                src_lang_label = LANGUAGES.get(trans.get('src'))
                dest_content = trans.get('result')

                sendText = '{}:  {} \n{}:  {}'.format(
                    src_lang_label, src_content, dest_lang_label, dest_content)
                tts = gTTS(dest_content, lang=dest_lang)
                tts.save('speak_dest.mp3')
                tts = gTTS(src_content, lang=trans.get('src'))
                tts.save('speak_src.mp3')
                try:
                    event.msg.chat.sendMsg(sendText)
                    event.msg.chat.sendFile(
                        open("speak_dest.mp3", "rb"), dest_content, False, True)
                    event.msg.chat.sendFile(
                        open("speak_src.mp3", "rb"), src_content, False, True)
                    os.remove("speak_dest.mp3")
                    os.remove("speak_src.mp3")
                except:
                    event.msg.chat.sendMsg('?')
            if "speak:" in msg:
                text = event.msg.content.split(':')
                try:
                    tts = gTTS(text[1].strip())
                    tts.save('speak.mp3')
                    event.msg.chat.sendFile(
                        open("speak.mp3", "rb"), "click to listen", False, True)
                    # os.remove("speak.mp3")
                except:
                    event.msg.chat.sendMsg('?')
            if "đọc:" in msg:
                text = event.msg.content.split(':')
                try:
                    tts = gTTS(text[1].strip(), lang='vi')
                    tts.save('speak.mp3')
                    event.msg.chat.sendFile(
                        open("speak.mp3", "rb"), "speak.mp3", False, True)
                    os.remove("speak.mp3")
                except:
                    event.msg.chat.sendMsg('?')
            if "new word" in msg:
                input_file = open('data.json', encoding='utf-8')
                json_array = json.load(input_file)
                item = random.choice(json_array)
                event.msg.chat.sendMsg(item.get('en') + ': ' + item.get('vi'))
                try:
                    tts = gTTS(item.get('en'))
                    tts.save('speak.mp3')
                    event.msg.chat.sendFile(
                        open("speak.mp3", "rb"), "speak.mp3", False, True)
                    os.remove("speak.mp3")
                except:
                    event.msg.chat.sendMsg('?')
            if "toeic" in msg:
                input_file = open('ToeicPart1.json', encoding='utf-8')
                json_array = json.load(input_file)
                item = random.choice(json_array)

                image_url = item.get('image')
                img_data = requests.get(image_url).content
                img_name = 'toeic_part1_' + item.get('question_id') + '.png'
                with open(img_name, 'wb') as handler:
                    handler.write(img_data)

                audio_url = item.get('audio')
                audio_data = requests.get(audio_url).content
                audio_name = 'toeic_part1_' + item.get('question_id') + '.mp3'
                with open(audio_name, 'wb') as handler:
                    handler.write(audio_data)

                event.msg.chat.sendMsg(
                    '[Part 1] Question #' + item.get('question_id'))
                event.msg.chat.sendFile(
                    open(img_name, "rb"), img_name, "image")
                event.msg.chat.sendFile(
                    open(audio_name, "rb"), audio_name, False, True)

                event.msg.chat.sendMsg('The answer is ...')
                event.msg.chat.sendMsg(
                    '.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.')
                event.msg.chat.sendMsg(
                    item.get('answerCorrect') + ': ' + item.get('questionContent'))
                os.remove(audio_name)
                os.remove(img_name)

                #  tts = gTTS(item.get('en'))
                #                     tts.save('speak.mp3')
                #                     event.msg.chat.sendFile(
                #                         open("speak.mp3", "rb"), "speak.mp3", False, True)
                #                     os.remove("speak.mp3")
                # event.msg.chat.sendMsg(item.get('en') + ': ' + item.get('vi'))
                # try:
                #   tts = gTTS(item.get('en'))
                #   tts.save('speak.mp3')
                #   event.msg.chat.sendFile(open("speak.mp3", "rb"), "speak.mp3", False, True)
                #   os.remove("speak.mp3")
                # except:
                #   event.msg.chat.sendMsg('?')
