# Задание 5<br><br>

### Условие
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки `socket` в Python.

#### Задание:
Сервер должен:

1. Принять и записать информацию о дисциплине и оценке по дисциплине.
2. Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

---

### Код

#### Сервер
##### `http_server.py`
```python
import socket
import threading

from request import Request
from course import Course


class MyHTTPServer:
    sock = None
    courses: list[Course] = []
    start_id: int = 0

    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name
        self.address = (host, port)

    def serve_forever(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.address)
        self.sock.listen(5)
        print('Serving HTTP on {}'.format(self.address))

        while True:
            client_socket, client_address = self.sock.accept()
            print("Got connection from", client_address)
            threading.Thread(target=self.serve_client, args=(client_socket,)).start()

    def serve_client(self, client_socket):
        data = client_socket.recv(1024)
        data_decoded = data.decode()
        print(f"Received:\n{data_decoded}")
        request = Request(data_decoded)
        self.handle_request(request, client_socket)

    def handle_request(self, request: Request, client_socket):
        if request.method == "GET" and request.path == "/courses":
            self.handle_get(client_socket)
        elif request.method == "POST" and request.path == "/courses":
            self.handle_post(client_socket, request)
        else:
            self.send_response(client_socket, "", 404)

    @staticmethod
    def send_response(client_socket, body, status_code):
        status_messages = {
            200: "200 OK",
            201: "201 Created",
            400: "400 Bad Request",
            404: "404 Not Found"
        }

        status_message = status_messages.get(status_code, "500 Internal Server Error")
        status_line = f'HTTP/1.1 {status_message}\r\n'
        headers = f'Content-Type: text/html; charset=utf-8\r\nContent-Length: {len(body)}\r\n\r\n'
        response = status_line + headers + body
        client_socket.sendall(response.encode())
        print(f"Sent:\n{response}")

    def handle_get(self, client_socket):
        if self.courses:
            html = "<html><body><h1>Courses and Grades</h1><ul>"
            for course in self.courses:
                html += f"<li>{course.name}: {str(course.grade)}</li>"
            html += "</ul></body></html>"
            self.send_response(client_socket, html, 200)
        else:
            self.send_response(client_socket, "<html><body><h1>No courses found!</h1></body></html>", 404)

    def handle_post(self, client_socket, request):
        try:
            course_name, grade = self.extract_parameters(request)
            if course_name and grade:
                course = Course(self.start_id, course_name, grade)
                self.courses.append(course)
                body, status_code = "OK", 201
            else:
                body, status_code = "Invalid data", 400
            self.send_response(client_socket, body, status_code)
        except Exception as e:
            self.send_response(client_socket, f"<html><body><h1>{e}</h1></body></html>", 500)

    @staticmethod
    def extract_parameters(request):
        params = dict(pair.split("=") for pair in request.body.split("&"))
        course = params.get("course_name", "")
        grade = params.get("grade", "")
        return course, int(grade)


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 2024
    name = "My first HTTPServer"
    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
```

##### `request.py`
```python
from functools import lru_cache
from urllib.parse import urlparse, parse_qs


class Request:
    def __init__(self, data):
        self.method, self.target, self.version = self.parse_request(data)
        self.headers = self.parse_headers(data)
        self.body = self.parse_body(data)

    @property
    def path(self):
        return self.url.path

    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)

    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.target)

    @staticmethod
    def parse_request(data):
        line = ''
        i = 0
        while '\r\n' not in line:
            line += data[i]
            i += 1
        request_line = line.replace('\r\n', '').split()
        method = request_line[0]
        url = request_line[1]
        version = request_line[2]
        return method, url, version

    @staticmethod
    def parse_headers(data):
        headers = {}
        lines = data.split('\r\n')[1:-2]
        for line in lines:
            header, value = line.split(': ')
            headers[header] = value
        return headers

    @staticmethod
    def parse_body(data):
        body = data.split('\r\n\r\n')[1]
        return body
```

##### `course.py`
```python
from dataclasses import dataclass


@dataclass
class Course:
    id: int
    name: str
    grade: int
```