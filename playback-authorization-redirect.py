#!/usr/bin/python3.6

import socketserver 
import json
from http import server

ADDR_THIS_SERVER = '141.105.134.199'
PORT_THIS_SERVER = 8008

ALLOWED_USER_AGENT = [
    "allow_group"
]

REDIRECT_LOCATION = 'http://google.com'
ANSW_OK = '{"return_code": 200}'

POST_PATHES = [
    '/clientauth'
]

class HTTPHandler(server.BaseHTTPRequestHandler):
    __not_found = "<body>Not found</body>"

    def do_POST(self):
        print('------Start handle message------')
        body = None
        content_length = self.__find_http_header(self.headers, 'Content-Length')

        if content_length:
           body = self.__get_content_request_body(content_length)

        if self.path == '/clientauth':
            if body:
                user_agent = self.__find_elem_in_json(body, 'user-agent')
                if(user_agent):
                    self.__controller_redirect_by_agents(ALLOWED_USER_AGENT, user_agent, self.__accept_user, self.__deny_user_redirect)     
                    return  
            else:
                self.__send_headers_403()
        else:
            self.__send_headers_404()


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
        body = body_bytes.decode()
        return body
    

    #Находит нужный элемент в json
    def __find_elem_in_json(self, json, target):
        try:
            data = json.loads(json)
            return data.get(target, '')
        except:
            print('-----------WARNING------------')
            print('=====JSON is not parsable=====')
            print('------------------------------')
            return None


    # Добавляет к запросу необходимые заголовки
    # И отправляет ответ сервера 
    def __send_headers_200(self, body):
        self.send_response(200)
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def __send_headers_404(self):
        self.send_response(404)
        self.send_header('Content-Length', len(self.__not_found))
        self.end_headers()
        self.wfile.write(self.__not_found) 

    def __send_headers_403(self):
        self.send_response(403)
        self.send_header('Content-Length', 0)
        self.end_headers()

    # Отправляет ответ на разрешение подключения к видеопотоку в nimble
    def __accept_user(self):
        answ_body = ANSW_OK
        self.__send_headers_200(answ_body)


    # Отправляет ответ 200 но перенапрявляет на другой поток, указанный в константах
    def __deny_user_redirect(self):
        redirect_location = REDIRECT_LOCATION
        print('Redirect:', redirect_location)
        redirect_body = '{"return_code":302, "redirect_location":"' + redirect_location + '"}'
        self.__send_headers_200(redirect_body)


    # Нахождение из мписка разрешенных групп, нужную и принятие соответствующего решения
    def __controller_redirect_by_agents(self, agents, user_ag, if_ok, if_deny):
        for el in agents:
            if el == user_ag:
                if_ok()
            return True
        if_deny()


socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer((ADDR_THIS_SERVER, PORT_THIS_SERVER), HTTPHandler, True)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    httpd.socket.close()