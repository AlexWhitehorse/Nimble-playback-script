# IP и Порт сервера
# ADDR_THIS_SERVER = '141.105.134.199'
ADDR_THIS_SERVER = 'localhost'
PORT_THIS_SERVER = 8008

# Группы пользователей для которых
# не будет редиректа
ALLOWED_USER_AGENT = [
    "allow_group"
]

WHITE_LIST_IP = [
    '89.160.200.111',       #   AA home
    '192.168.111.0/24',     #   internal IP Kvant
    '10.10.0.0/16',         #   Local IP Kvant
    '10.4.0.0/16',          #   
    '192.168.2.0/24',       #   
    '78.26.204.85',         #   MS home
    '195.189.196.0/23',     #   Real IP Kvant
    '91.202.108.137'        #   Alex home
]

# Аддресс потока, на который будут перенаправление
REDIRECT_LOCATION = 'https://cdn.kvant.mk.ua/kvanttv/kvant-err/playlist.m3u8'

DEBUG = True
