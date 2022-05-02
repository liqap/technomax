from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pydrive.auth import GoogleAuth
import telebot
from telebot import types
import config
import os.path
from google.oauth2 import service_account
from datetime import date
from pydrive.drive import GoogleDrive

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = '1FwH6is-lnO8i8N3bVbJXcELRPq9gwkMK8CUIAueIH-Y'
SAMPLE_RANGE_NAME = 'Sheet1'

service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()

bot = telebot.TeleBot('5019727632:AAHy_ZgLpqi6uyM7gmtgSmwi5met3zTOeJ4') 


name = ''
project = ''
agregat = ''
uzel = ''
detail = ''
problem = ''
offer = ''


@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	btn1 = types.KeyboardButton("Создать новую заявку") 
	markup.add(btn1)
	bot.send_message(message.chat.id, text = 'Добро пожаловать в бота обратной связи ⚙️TECHNOMAX!'.format(message.from_user), reply_markup=markup)
	
@bot.message_handler(content_types=['text'])
def first(message):
	if message.text == 'Создать новую заявку':
		delete = types.ReplyKeyboardRemove()
		bot.send_message(message.from_user.id, 'Как Вас зовут?', reply_markup=delete)
		bot.register_next_step_handler(message, get_name)
def get_name(message):
	global name 
	name = message.text 
	bot.send_message(message.from_user.id, 'Какой проект?')
	bot.register_next_step_handler(message, get_project)
def get_project(message):
	global project
	project = message.text 
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	one = types.KeyboardButton("Печь ручная")
	a = types.KeyboardButton("ЛОС")
	b = types.KeyboardButton("АХПП")
	c = types.KeyboardButton("МПП")
	d = types.KeyboardButton("Конвейер")
	e = types.KeyboardButton("Ручная TC")
	f = types.KeyboardButton("Кабина TMX")
	g = types.KeyboardButton("Кабина Q-MAX")
	h = types.KeyboardButton("Вытяжной шкаф AVF")
	i = types.KeyboardButton("ЦПП")
	j = types.KeyboardButton("Жидкая кабина")
	k = types.KeyboardButton("Жидкий грунт")
	l = types.KeyboardButton("Печь автоматическая")
	markup.add(one, a, b, c, d, e, f, g, h, i, j, k, l)

	bot.send_message(message.from_user.id, 'Выберите агрегат'.format(message.from_user), reply_markup=markup)
	bot.register_next_step_handler(message, get_agregat)
def get_agregat(message):
	global agregat
	agregat = message.text
	delete = types.ReplyKeyboardRemove()

	bot.send_message(message.from_user.id, 'Укажите узел', reply_markup=delete)
	bot.register_next_step_handler(message, get_uzel)
def get_uzel(message):
	global uzel
	uzel = message.text 

	bot.send_message(message.from_user.id, 'Укажите конкретную деталь, или изделие')
	bot.register_next_step_handler(message, get_detail)
def get_detail(message):
	global detail
	detail = message.text 

	bot.send_message(message.from_user.id, 'В чем суть проблемы?')
	bot.register_next_step_handler(message, get_problem)
def get_problem(message):
	global problem
	problem = message.text

	bot.send_message(message.from_user.id, 'Какие предложения на будущее?')
	bot.register_next_step_handler(message, get_offer)
def get_offer(message):
	global offer
	offer = message.text 
	
	bot.send_message(message.from_user.id, 'Пожалуйста, пришлите фото')
	bot.register_next_step_handler(message, get_photo)
def get_photo(message):
	global photo

	photo = message.photo

	idd = str(message.from_user.id)

	bot.forward_message(chat_id = '@technomaxzayavki', from_chat_id = message.chat.id, message_id = message.id)
	bot.send_message(chat_id = '@technomaxzayavki', text='⬆️ Заявка номер #' + idd)






	
	today = str(date.today())
	result = service.get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range = SAMPLE_RANGE_NAME).execute()
	data_from_sheet = result.get('values', [])

	range_ = 'Sheet1!A2:J2'

	array = {'values': [[today, name, project, agregat, uzel, detail, problem, offer, idd], []]}

	response = service.append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_, valueInputOption='USER_ENTERED', body=array).execute()



bot.polling(none_stop = True, interval = 0)






