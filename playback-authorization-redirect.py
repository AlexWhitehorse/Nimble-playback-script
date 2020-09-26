#!/usr/bin/python3.6

import socketserver 
import json
from http import server

# IP и Порт сервера
ADDR_THIS_SERVER = '141.105.134.199'
PORT_THIS_SERVER = 8008

# Группы пользователей для которых
# не будет редиректа
ALLOWED_USER_AGENT = [
    "allow_group"
]

# Аддресс потока, на который будут перенаправление
REDIRECT_LOCATION = 'http://google.com'


ANSW_OK = '{"return_code": 200}'
DEBUG = True
# Example of json request
# {"host":"<host>", "url": "<stream URL>", "ip": "<client IP>", "user-agent": "allow_group", "referer": "< Заголовок Referer  >", "session_id": "<идентификатор сеанса Nimble>", "session_type": "<имя протокола>"}

class HTTPHandler(server.BaseHTTPRequestHandler):
    __not_found = "<body>Not found</body>"

    def do_POST(self):
        body = None
        content_length = self.__find_http_header(self.headers, 'Content-Length')

        if content_length:
            body = self.__get_content_request_body(content_length)
            self.____debug_('\n' + body)

        if self.path == '/clientauth':
            if body:
                user_agent = self.__find_elem_in_json(body, 'user-agent')

                if(user_agent):
                    group_user = self.__arr_find_elem(ALLOWED_USER_AGENT, user_agent)    
                    # Если пользователь есть в белом списке
                    # Или перенаправление пользователя на другой поток
                    if(group_user):
                        self.__accept_user()
                    elif(not group_user):
                        self.__deny_user_redirect(REDIRECT_LOCATION)
                else:
                    self.__deny_user_redirect(REDIRECT_LOCATION)

            else:
                self.__send_headers(400)
        else:
            self.__send_headers(404, self.__not_found)


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

    def __str_to_bytrs(self, string):
        return string.encode()

    def __send_headers(self, code, data = False):
        self.send_response(code)
        self.end_headers()
        if data:    
            self.send_header('Content-Length', len(data))
            self.wfile.write(self.__str_to_bytrs(data)) 
        else:
            self.send_header('Content-Length', 0)

    # Отправляет ответ на разрешение подключения к видеопотоку в nimble
    def __accept_user(self):
        answ_body = ANSW_OK
        self.__send_headers(200, answ_body)


    # Отправляет ответ 200 но перенапрявляет на другой поток, указанный в константах
    def __deny_user_redirect(self, redirect_location):
        print('Redirect:', redirect_location)
        redirect_body = '{"return_code":302, "redirect_location":"' + redirect_location + '"}'
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

    def ____debug_(self, message):
        if DEBUG:
            print(message)

        


socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer((ADDR_THIS_SERVER, PORT_THIS_SERVER), HTTPHandler, True)

try:
    print('Server started at', ADDR_THIS_SERVER + ':' + PORT_THIS_SERVER)
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    httpd.socket.close()