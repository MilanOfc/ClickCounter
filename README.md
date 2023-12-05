# ClickCounter

## Общее описание программы
Программа сокращает ссылки с помощью сервиса bitly, если ввести уже сокращённую ссылку - выдает количество переходов по ней

## Требования
Python 3 должен быть уже установлен, с помощью pip устанавливаем зависимости

    python -m pip install -r requirements.txt

## Переменные окружения
Для корректной работы программы необходим token.

    echo BITLY_TOKEN='%Ваш_Токен%' >> .env

### Как получить?
Зарегистрироваться на [сайте](https://app.bitly.com/bbt2/) и получить [токен](https://app.bitly.com/settings/api/)
Полная [документация сервиса](https://dev.bitly.com/docs/getting-started/authentication/)

## Запуск

    python clickcounter.py %Ваша_Ссылка%

### Пример вывода программы
![Пример вывода](img.png)

