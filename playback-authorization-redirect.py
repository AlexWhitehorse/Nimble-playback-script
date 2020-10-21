#!/usr/bin/python3.6

import socketserver 
import json
from http import server
from Ip_addresses import IPv4_ip

# IP и Порт сервера
ADDR_THIS_SERVER = '141.105.134.199'
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

def makeWhiteList_ip_objects():
    WL = []
    for ip in WHITE_LIST_IP:
        ipv4_ip = IPv4_ip(ip)
        WL.append(ipv4_ip)
    return WL

WHITE_LIST = makeWhiteList_ip_objects()
ANSW_OK = '{"return_code": 200}'
DEBUG = True
# Example of json request
# {"host":"<host>", "url": "<stream URL>", "ip": "<client IP>", "user-agent": "allow_group", "referer": "< Заголовок Referer  >", "session_id": "<идентификатор сеанса Nimble>", "session_type": "<имя протокола>"}


class HTTPHandler(server.BaseHTTPRequestHandler):
    __not_found = "<body>Not found</body>"

    def do_POST(self):
        timeout = 1
        body = None
        content_length = self.__find_http_header(self.headers, 'Content-Length')

        if content_length:
            body = self.__get_content_request_body(content_length)
            self.____debug_('\n' + body)

        if self.path == '/clientauth':
            if body:
                # white_list = 
                host = self.__find_elem_in_json(body, 'host')
                user_ip = self.__find_elem_in_json(body, 'ip')
                stream_url = self.__find_elem_in_json(body, 'url')
                user_agent = self.__find_elem_in_json(body, 'user-agent')
                group_user = None

                if(user_agent):
                    group_user = self.__arr_find_elem(ALLOWED_USER_AGENT, user_agent)   

                # Если пользователь есть в белом списке user_agent
                if(group_user and user_agent):
                    self.__accept_user()
                    
                # Если пользователь есть в белом списке IP
                elif self.__compare_ip(user_ip, WHITE_LIST):
                    print('User accepted')
                    self.__accept_user()



                elif(not group_user):
                    self.__deny_user_redirect(host, stream_url, REDIRECT_LOCATION)
                # else:
                #     self.__deny_user_redirect(host, stream_url, REDIRECT_LOCATION)

            else:
                self.__send_headers(400)
        else:
            self.__send_headers(404, self.__not_found)

    # Get handler
    def do_GET(self):
        self.send_response(400)
        self.end_headers()


    # Нахождение заголовка зароса
    def __find_http_header(self, all_headers, target_header):
        find = None
        for el in all_headers:
            if el == target_header:
                return all_headers[el]
        return find


    #Получение данных тела запроса и конвертация из байт 
    def __get_content_request_body(self, len_content):
        body_bytes = self.rfile.read(int(len_content))
        data = body_bytes.decode()
        return data
    

    #Находит нужный элемент в json
    def __find_elem_in_json(self, data, target):
        try:
            data = json.loads(data)
            return data.get(target, '')
        except json.decoder.JSONDecodeError:
            print('\n-----------WARNING------------')
            print('=====JSON is not parsable=====\n')
            print('JSON: ', data)
            print('------------------------------')
            return None

    def __str_to_bytes(self, string):
        return string.encode()

    def __send_headers(self, code, data = False):
        self.send_response(code)
        if data:    
            self.send_header('Content-Length', len(data))  
            self.end_headers()
            self.wfile.write(self.__str_to_bytes(data)) 
            self.____debug_(data)
        else:
            self.send_header('Content-Length', 0)
            self.end_headers()

    # Отправляет ответ на разрешение подключения к видеопотоку в nimble
    def __accept_user(self):
        answ_body = ANSW_OK
        self.__send_headers(200, answ_body)


    # Отправляет ответ 200 но перенапрявляет на другой поток, указанный в константах
    def __deny_user_redirect(self, host, url_s, playlist):
        # redirect_location = 'http://' + host + url_s[:url_s.rfind('/') + 1] + playlist
        redirect_body = '{"return_code":302, "redirect_location":"' + playlist + '"}'
        self.__send_headers(200, redirect_body)


    # Нахождение из мписка разрешенных групп, нужную и принятие соответствующего решения
    def __controller_redirect_by_agents(self, agents, user_ag, if_ok):
        for el in agents:
            if el == user_ag:
                if_ok()
                return True
        return False

    def __arr_find_elem(self, arr, element):
        for el in arr:
            if el == element:
                return True
        return False

    def __compare_ip(self, ip_user, ip_objects):
        for x in ip_objects:
            ip_obj = x
            if ip_obj.is_in_range(ip_user):
                return True
        return False

    def ____debug_(self, message):
        if DEBUG:
            print(message)

        


socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer((ADDR_THIS_SERVER, PORT_THIS_SERVER), HTTPHandler, True)

try:
    print('Server started at', ADDR_THIS_SERVER + ':' + str(PORT_THIS_SERVER))
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    httpd.socket.close()

# print(WHITE_LIST)