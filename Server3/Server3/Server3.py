import socket

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind(
    ("127.0.0.1", 1234)
)

server.listen(10)
print("server working...")

socket_client, address = server.accept()
socket_client.send("You are connected".encode("utf-8"))

list_users = [("qwerty", 123), ("юзер", 456), ("логин", 789)]


def is_error(num):
    if num == 0:
        print(0)
        socket_client.send("Нет ошибки".encode("utf-8"))
    elif num == 1:
        print(1)
        socket_client.send("Ошибка авторизации".encode("utf-8"))
    elif num == 2:
        print(2)
        socket_client.send("Не указаны коэффициенты".encode("utf-8"))
    elif num == 3:
        print(3)
        socket_client.send("Синтаксичекая ошибка".encode("utf-8"))
    elif num == 4:
        print(4)
        socket_client.send("Неверный логин или пароль".encode("utf-8"))
    elif num == 5:
        socket_client.send("Необходимо авторизоваться".encode("utf-8"))


def login(user, password):
    for i in list_users:
        u = i[0]
        p = i[1]
        if (str(u) == str(user)) & (str(p) == str(password)):
            return True
    return False


def isdigit(a, b, c):
    try:
        int(a)
        int(b)
        int(c)
        return 0
    except ValueError:
        return 3


def solve(a, b, c):
    D = b ** 2 - 4 * a * c
    if D < 0:
        return ""
    elif a == 0:
        return "a=0"
    else:
        x1 = round((-b + D ** 0.5) / (2 * a), 2)
        x2 = round((-b - D ** 0.5) / (2 * a), 2)
        return [x1, x2]


auth = False

while auth is False:
    log = socket_client.recv(1024)
    log = log.decode("utf-8")
    data = log.split(' ')[0]
    try:
        if data == "LOGIN":
            user = log.split(' ')[1]
            password = log.split(' ')[2]
            auth = login(user, password)
            if auth is False:
                is_error(4)
            else:
                auth = True
                socket_client.send("Вы авторизованы".encode("utf-8"))
        else:
            is_error(5)
    except BaseException:
        is_error(1)

a = b = c = 0
x = ""

while True:
    s = socket_client.recv(1024)
    s = s.decode("utf-8")
    data = s.split(' ')[0]
    try:
        if data == "STORE":
            a = s.split(' ')[1]
            b = s.split(' ')[2]
            c = s.split(' ')[3]
            if isdigit(a, b, c) == 3:
                is_error(3)
            else:
                is_error(0)
                a = int(a)
                b = int(b)
                c = int(c)

        elif data == "SOLVE":
            if s == "SOLVE":
                x = solve(a, b, c)
            else:
                A = s.split(' ')[1]
                B = s.split(' ')[2]
                C = s.split(' ')[3]
                if isdigit(A, B, C) == 3:
                    is_error(3)
                else:
                    A = int(A)
                    B = int(B)
                    C = int(C)
                x = solve(A, B, C)

            if x == "":
                msg = "Уравнение не имеет корней"
            elif x == "a=0":
                msg = "a=0, запишите новые коэффициенты"
            else:
                x1 = x[0]
                x2 = x[1]
                msg = ""
                if x1 == x2:
                    msg = "Квадратное уравнение имеет одно решение: x = " + str(x1)
                else:
                    msg = "Квадратное уравнение имеет два корня: x1 = " + str(x1) + " , x2 = " + str(x2)
            socket_client.send(msg.encode("utf-8"))
        else:
            is_error(3)

    except BaseException:
        is_error(2)
    if s == "exit":
        print("user disconnected")

