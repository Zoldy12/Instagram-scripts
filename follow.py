import time
import random
from playwright.sync_api import sync_playwright

def navigate(page, username):
    max_attempts = 3
    
    for attempt in range(max_attempts):
        try:
            print(f"🔄 Попытка {attempt + 1} перехода на @{username}")
            
            # Очищаем текущую страницу перед новым переходом
            try:
                # Закрываем окно с подписчиками
                page.keyboard.press("Escape")
                time.sleep(1)
            except:
                pass
            
            # Переходим на страницу профиля с обработкой прерываний
            page.goto(f"https://www.instagram.com/{username}/", 
                     wait_until="domcontentloaded",  # Меньше ждем
                     timeout=15000)
            
            # Проверяем, что мы на нужной странице
            current_url = page.url
            expected_url = f"https://www.instagram.com/{username}/"
            
            if expected_url in current_url:
                print(f"✅ Успешно перешли на @{username}")
                return True
            else:
                print(f"⚠️ Перенаправление на: {current_url}")
                
                # Если нас перенаправило, пробуем еще раз
                time.sleep(2)
                continue
                
        except Exception as e:
            error_msg = str(e)
            if "interrupted" in error_msg.lower() or "navigation" in error_msg.lower():
                print(f"🔄 Навигация прервана, пробуем снова...")
                time.sleep(2)
                continue
            else:
                print(f"❌ Ошибка перехода: {error_msg}")
                return False
    
    print(f"🚫 Не удалось перейти на @{username} после {max_attempts} попыток")
    return False



def parc(page, bloger: str, max_follows: int):
        followed_usernames = []
        try:
            # Открываем страницу профиля
            try:
                navigate(page, bloger)
            except Exception as e:
                print(e)
            print(f'✅ Страница {page.title()} открыта')
            
            # Ждем загрузки страницы профиля
            page.wait_for_selector("header section", timeout=10000)
            
            print("⌛ Проверка подписки...")
            try:
                sb_button = page.locator('button:has-text("Подписаться"), button:has-text("Follow")').first
                sb_button.click()
                print(f"📍 Подписка на блогера @{bloger}")
            except Exception as e:
                print("📍 Подписка на блогера уже оформлена")
                
            # Находим и кликаем на ссылку подписчиков
            try:
                followers_link = page.locator("a[href*='followers']").first
                followers_link.click()
                print("✅ Открыта вкладка с подписчиками")
            except:
                page.click("a:has-text('подписчиков')")
                print("✅ Открыта вкладка с подписчиками")
            
            # Ждем появления окна с подписчиками
            page.wait_for_selector('div[role="dialog"]', timeout=10000)
            print("✅ Окно с подписчиками загружено")
            time.sleep(1)
            
            follow_count = 0
            max_follows = max_follows  # Максимальное количество подписок
            scroll_attempts = 0
            max_scroll_attempts = 999 # Максимальное количестро скролов на 1 блогера
            
            while follow_count < max_follows and scroll_attempts < max_scroll_attempts:
                # Ищем все кнопки "Подписаться" и соответствующие элементы с username
                follow_buttons = page.locator('button:has-text("Подписаться"), button:has-text("Follow")')
                button_count = follow_buttons.count()
                
                print(f"🔍 Найдено кнопок 'Подписаться': {button_count}")
                
                # Кликаем на все доступные кнопки подписки и сохраняем username
                for i in range(button_count):
                    if follow_count >= max_follows:
                        break
                        
                    try:
                        button = follow_buttons.nth(i)
                        
                        if button.is_visible():
                            # Находим родительский контейнер с информацией о пользователе
                            user_container = button.locator("xpath=./ancestor::div[contains(@class, 'x1dm5mii') or contains(@class, 'x1iyjqo2')][1]")
                            
                            # Ищем username в контейнере
                            username_element = user_container.locator("a[href*='/'] span").first
                            username = username_element.text_content().strip() if username_element else f"user_{follow_count + 1}"
                            
                            # Кликаем на кнопку подписки
                            if username not in followed_usernames:
                                button.click()
                                follow_count += 1
                                
                                followed_usernames.append(username)
                                print(f"✅ Подписка #{follow_count} на пользователя: @{username}")
                            
                            # Случайная задержка между подписками (типо я не бот, а человек)
                            time.sleep(random.uniform(0.5, 1))
                            
                    except Exception as e:
                        print(f"❌ Ошибка при подписке: {e}")
                        continue
                
                # Прокручиваем список подписчиков для загрузки новых
                try:
                    page.keyboard.press("PageDown", delay=200)
                    scroll_attempts += 1
                    print(f"📜 Прокрутка #{scroll_attempts} выполнена")
                    
                    # Задержка после прокрутки для загрузки новых подписчиков (типо не бот)
                    time.sleep(random.uniform(0.3, 0.5))
                    
                except Exception as e:
                    print(f"❌ Ошибка при прокрутке: {e}")
                    break
            
            # Закрываем окно с подписчиками
            try:
                close_button = page.locator('svg[aria-label="Закрыть"], svg[aria-label="Close"]').first
                close_button.click()
                print("✅ Окно подписчиков закрыто")
            except:
                print("⚠️ Не удалось закрыть окно")
            
        except Exception as e:
            print(f"💥 Критическая ошибка: {e}")
            
        return followed_usernames




def main(all_data):
    # Список для хранения никнеймов пользователей
    followed_usernames = []
    
    with sync_playwright() as pl:
        browser = pl.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_default_timeout(10000)
        
        try:
            # Открываем страницу профиля
            page.goto(f"https://www.instagram.com/zoldy_12/", wait_until='load')
            
            # Принимаем cookies
            cookie_selectors = [
                "button._a9--._a9_1",
                "button[type='button']:has-text('Разрешить')",
                "button:has-text('Разрешить')",
                "button:has-text('Allow All')",
                "button:has-text('Accept All')",
                "button._a9--",
                "//button[contains(text(), 'Разрешить')]",
                "//button[contains(text(), 'Allow')]",
                "//button[contains(text(), 'Accept')]"
            ]
            
            cookie_accepted = False
            for selector in cookie_selectors:
                try:
                    page.wait_for_selector(selector, timeout=5000)
                    page.click(selector)
                    print(f"✅ Cookies приняты с селектором: {selector}")
                    cookie_accepted = True
                    break
                except:
                    continue
                
                
            signin_selectors = [
                "a[role='link']:has-text('Войти')",
            ]
            
            for selector in signin_selectors:
                button = page.locator(selector).first      
                button.click()
                print("✅ Нажали на кнопку 'Войти'")
                
        except Exception as e:
            print(f"💥 Критическая ошибка: {e}")
            
        entery_check = input('Авторизуйся и нажми Enter для запуска')
        start_time = round(time.time())
        
        for data in all_data:
            followed_usernames.append(parc(page, data[0], int(data[1])))
            time.sleep(1)
        
        
        # Выводим результаты
        cnt = 0
        for users in followed_usernames:
            for user in users:
                cnt+=1
        print("\n" + "="*50)
        print("📊 ОТЧЕТ О ПОДПИСКАХ")
        print("="*50)
        print(f"Всего подписок выполнено: {cnt}")
        print("\nСписок подписок:")
        print("-" * 20)
        
        for i, usernames in enumerate(followed_usernames, 1):
            print(f"{i:2d})")
            for g, username in enumerate(usernames, 1):
                print(f"  {g:2d}. {username}")
        
        # Сохраняем в файл
        try:
            with open("followed_users.txt", "a", encoding="utf-8") as f:
                for usernames in followed_usernames:
                    for username in usernames:
                        f.write(f"{username}\n")
            print(f"\n💾 Список сохранен в файл: followed_users.txt")
        except Exception as e:
            print(f"❌ Ошибка при сохранении в файл: {e}")
        
        #Расчёт времени выполнения
        end_time = round(time.time())
        hours = (end_time - start_time) // 3600
        minutes = ((end_time - start_time) - hours * 3600) // 60
        seconds = (end_time - start_time) - hours * 3600 - minutes * 60
        if hours:
            total_time = f"{hours}ч. {minutes}мин. {seconds}с."
        elif minutes:
            total_time = f"{minutes}мин. {seconds}с."
        else:
            total_time = f"{seconds}с."
        print(f"⌚ Время выполнения работы: {total_time}")
        
        # Пауза для проверки результата
        _ = input('Нажми Enter, чтобы закрыть окно и завершить выполнение.')
        
        browser.close()
    
    return followed_usernames

# Запускаем функцию
if __name__ == '__main__':
    with open("blogers.txt", "r", encoding="utf-8") as file:
        all_data = []
        for stroka in file:
            stroka = stroka[:-1]
            data = stroka.split(' ')
            if stroka == 'en':
                break
            all_data.append(data)
    main(all_data)
    