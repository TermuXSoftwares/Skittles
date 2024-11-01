import random
import requests
import aiohttp
import asyncio
from colorama import Fore, init

# Инициализация colorama
init(autoreset=True)

def rainbow_text(text):
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    return ''.join(f"{colors[i % len(colors)]}{char}" for i, char in enumerate(text))

def search_by_number(phone_number):
    url = f"http://num.voxlink.ru/get/?num={phone_number}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(rainbow_text(f"Код: {data.get('code', '')}"))
        print(rainbow_text(f"Номер: {data.get('num', '')}"))
        print(rainbow_text(f"Весь номер: +7{data.get('full_num', '')}"))
        print(rainbow_text(f"Оператор: {data.get('operator', '')}"))
        print(rainbow_text(f"Регион: {data.get('region', '')}"))
    else:
        print(rainbow_text("Ошибка при получении данных по номеру."))

def search_by_ip(ip_address):
    url = f"http://ipwho.is/{ip_address}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('success', True):
            print(rainbow_text(f"IP: {data.get('ip', '')}"))
            print(rainbow_text(f"Страна: {data.get('country', '')}"))
            print(rainbow_text(f"Регион: {data.get('region', '')}"))
            print(rainbow_text(f"Город: {data.get('city', '')}"))
            print(rainbow_text(f"Широта: {data.get('latitude', '')}"))
            print(rainbow_text(f"Долгота: {data.get('longitude', '')}"))
        else:
            print(rainbow_text("Ошибка: Неверный IP-адрес."))
    else:
        print(rainbow_text("Ошибка при получении данных по IP."))

def search_social_media(phone_number):
    print(rainbow_text("Социальные сети:"))
    print(rainbow_text(f"WhatsApp: https://wa.me/{phone_number}"))
    print(rainbow_text(f"Telegram: https://t.me/{phone_number}"))

def osint_google(query):
    print(rainbow_text("Результаты поиска в Google:"))
    print(rainbow_text(f"https://www.google.com/search?q={query}"))

def osint_yandex(query):
    print(rainbow_text("Результаты поиска в Яндекс:"))
    print(rainbow_text(f"https://yandex.ru/search/?text={query}"))

def osint_nickname(nickname):
    print(rainbow_text("Результаты поиска по никнейму:"))
    print(rainbow_text(f"VK: https://vk.com/{nickname}"))
    print(rainbow_text(f"Tumblr: https://{nickname}.tumblr.com"))
    print(rainbow_text(f"Youtube: https://www.youtube.com/{nickname}"))
    print(rainbow_text(f"Snapchat: https://www.snapchat.com/add/{nickname}"))
    print(rainbow_text(f"LiveJournal: https://{nickname}.livejournal.com"))
    print(rainbow_text(f"Pikabu: https://pikabu.ru/@{nickname}"))
    print(rainbow_text(f"Picsart: https://picsart.com/u/{nickname}"))

def reporter_tg():
    text = input(rainbow_text("Введите текст жалобы: "))
    num_complaints = input(rainbow_text("Введите количество жалоб для отправки: "))
    if num_complaints.isdigit():
        num_complaints = int(num_complaints)
    else:
        print(rainbow_text("Ошибка: Введите целое число."))
        return

    print()

    with open('num.txt', 'r') as num_file:
        contacts = num_file.read().splitlines()

    with open('ua.txt', 'r') as ua_file:
        ua_list = ua_file.read().splitlines()

    url = 'https://telegram.org/support'
    yukino = 0
    success_count = 0
    failure_count = 0
    max_retries = 3

    async def send_complaint(session, text, contact, ua_list):
        nonlocal yukino, success_count, failure_count

        headers = {
            'User -Agent': random.choice(ua_list)
        }
        payload = {
            'text': text,
            'contact': contact
        }

        for attempt in range(max_retries):
            try:
                async with session.post(url, data=payload, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        yukino += 1
                        success_count += 1
                        print(rainbow_text(f"Жалоба успешно отправлена: {yukino}"))
                        return
            except aiohttp.ClientError:
                pass
            except asyncio.TimeoutError:
                pass

        failure_count += 1
        print(rainbow_text("Не удалось отправить жалобу после нескольких попыток"))

    async def run_tasks(num_complaints, text):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(num_complaints):
                chosen_contact = random.choice(contacts)
                tasks.append(send_complaint(session, text, chosen_contact, ua_list))
            await asyncio.gather(*tasks)

    asyncio.run(run_tasks(num_complaints, text))
    print()

    print(rainbow_text(f"Успешно отправлено жалоб: {success_count}"))
    print(rainbow_text(f"Не удалось отправить жалоб: {failure_count}"))
    print()

def main():
    while True:
        print(rainbow_text('''
           ▄████████    ▄█   ▄█▄  ▄█      ███         ███      ▄█          ▄████████    ▄████████ 
          ███    ███   ███ ▄███▀ ███  ▀█████████▄ ▀█████████▄ ███         ███    ███   ███    ███ 
          ███    █▀    ███▐██▀   ███▌    ▀███▀▀██    ▀███▀▀██ ███         ███    █▀    ███    █▀  
          ███         ▄█████▀    ███▌     ███   ▀     ███   ▀ ███        ▄███▄▄▄       ███        
        ▀███████████ ▀▀█████▄    ███▌     ███         ███     ███       ▀▀███▀▀▀     ▀███████████ 
                 ███   ███▐██▄   ███      ███         ███     ███         ███    █▄           ███ 
           ▄█    ███   ███ ▀███▄ ███      ███         ███     ███▌    ▄   ███    ███    ▄█    ███ 
         ▄████████▀    ███   ▀█▀ █▀      ▄████▀      ▄████▀   █████▄▄██   ██████████  ▄████████▀  
                       ▀                                      ▀                                   
                                        Автор: @SkittlesSoftwares
'''))
        print(rainbow_text("                    [Поиск]                      [Осинт]                      [Снос]      "))
        print(rainbow_text("              ┌──────────────────┐	   ┌─────────────────┐         ┌──────────────────┐"))
        print(rainbow_text("              │1. Поиск по Номеру│	   │4. Осинт Гугл    │         │7. Снос Сайт ТГ   │"))
        print(rainbow_text("              │2. Поиск по Айпи  │	   │5. Осинт Яндекс  │         │8. Автор          │"))
        print(rainbow_text("              │3. Поиск Соцсетей │	   │6. Осинт Никнейм │         │9. Выход          │"))
        print(rainbow_text("              └──────────────────┘	   └─────────────────┘         └──────────────────┘"))
        print("ㅤ")
        choice = input(rainbow_text("Ваш выбор >>> "))
        
        if choice == '1':
            phone_number = input(rainbow_text("Введите номер телефона: "))
            search_by_number(phone_number)
        elif choice == '2':
            ip_address = input(rainbow_text("Введите IP-адрес: "))
            search_by_ip(ip_address)
        elif choice == '3':
            phone_number = input(rainbow_text("Введите номер телефона для поиска в соцсетях: "))
            search_social_media(phone_number)
        elif choice == '4':
            query = input(rainbow_text("Введите номер, никнейм или юзернейм для поиска в Google: "))
            osint_google(query)
        elif choice == '5':
            query = input(rainbow_text("Введите номер, никнейм или юзернейм для поиска в Яндекс: "))
            osint_yandex(query)
        elif choice == '6':
            nickname = input(rainbow_text("Введите никнейм для поиска: "))
            osint_nickname(nickname)
        elif choice == '7':
              reporter_tg()
        elif choice == '8':
              print(rainbow_text("Автор: "))
        elif choice == '9':
            print(rainbow_text("Выход из программы."))
            break
        else:
            print(rainbow_text("Неверный выбор. Пожалуйста, попробуйте снова."))

if __name__ == "__main__":
    main()