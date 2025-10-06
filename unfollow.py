import os
import time
import random
from playwright.sync_api import sync_playwright

def unfollow_user(page, username):
        """Основная функция для отписки от пользователя"""
        try:
            # Переходим на страницу пользователя
            if not navigate(page, username):
                print(f"❌ Не удалось перейти на страницу @{username}")
                return False
            
            # Ждем загрузки страницы
            try:
                page.wait_for_selector("header section", timeout=10000)
                print(f"✅ Страница @{username} загружена")
            except:
                print(f"⚠️ Страница @{username} загружена частично")
            
            # Пробуем отписаться
            unfollow_success = unfollow_user_process(page, username)
            
            if unfollow_success:
                print(f"🎉 Успешно отписались от @{username}")
                return True
            else:
                print(f"❌ Не удалось отписаться от @{username}")
            
        except Exception as e:
            print(f"💥 Критическая ошибка: {e}")


def unfollow_user_process(page, username):
    """Процесс отписки от пользователя"""
    
    # Сначала проверяем текущее состояние подписки
    subscription_state = check_subscription_state(page, username)
    print(f"📊 Текущее состояние подписки: {subscription_state}")
    
    if subscription_state == "not_following":
        print(f"ℹ️ Вы не подписаны на @{username}")
        return True
    
    elif subscription_state == "following":
        return handle_following_state(page, username)
    
    elif subscription_state == "requested":
        return handle_requested_state(page, username)
    
    else:
        print(f"❌ Неизвестное состояние подписки: {subscription_state}")
        return False

def check_subscription_state(page, username):
    """Проверяет текущее состояние подписки"""
    try:
        # Даем время для загрузки страницы
        time.sleep(2)
        
        # 1. Проверяем кнопку "Подписки" / "Following"
        try:
            following_selectors = [
                "button:has-text('Подписки')",
                "button:has-text('Following')",
                "//button[contains(text(), 'Подписки')]",
                "//button[contains(text(), 'Following')]"
            ]
            
            for selector in following_selectors:
                try:
                    if selector.startswith('//'):
                        if page.locator(selector).first.is_visible(timeout=2000):
                            return "following"
                    else:
                        if page.locator(selector).first.is_visible(timeout=2000):
                            return "following"
                except:
                    continue
        except Exception as e:
            print(f"⚠️ Ошибка при поиске кнопки 'Подписки': {e}")

        # 2. Проверяем кнопку "Запрос отправлен" / "Requested"
        try:
            requested_selectors = [
                "button:has-text('Запрос отправлен')",
                "button:has-text('Requested')",
                "//button[contains(text(), 'Запрос отправлен')]",
                "//button[contains(text(), 'Requested')]"
            ]
            
            for selector in requested_selectors:
                try:
                    if selector.startswith('//'):
                        if page.locator(selector).first.is_visible(timeout=2000):
                            return "requested"
                    else:
                        if page.locator(selector).first.is_visible(timeout=2000):
                            return "requested"
                except:
                    continue
        except Exception as e:
            print(f"⚠️ Ошибка при поиске кнопки 'Запрос отправлен': {e}")

        # 3. Проверяем кнопку "Подписаться" / "Follow"
        try:
            follow_selectors = [
                "button:has-text('Подписаться')",
                "button:has-text('Follow')",
                "//button[contains(text(), 'Подписаться')]",
                "//button[contains(text(), 'Follow')]"
            ]
            
            for selector in follow_selectors:
                try:
                    if selector.startswith('//'):
                        if page.locator(selector).first.is_visible(timeout=2000):
                            return "not_following"
                    else:
                        if page.locator(selector).first.is_visible(timeout=2000):
                            return "not_following"
                except:
                    continue
        except Exception as e:
            print(f"⚠️ Ошибка при поиске кнопки 'Подписаться': {e}")

        # 4. Альтернативный способ - ищем любую кнопку в заголовке и анализируем текст
        try:
            header_buttons = page.locator("header button, section button, div[role='button']")
            button_count = header_buttons.count()
            
            for i in range(min(button_count, 5)):  # Проверяем первые 5 кнопок
                try:
                    button = header_buttons.nth(i)
                    if button.is_visible(timeout=1000):
                        button_text = button.text_content(timeout=1000)
                        if button_text:
                            text_lower = button_text.strip().lower()
                            
                            if any(word in text_lower for word in ["подписки", "following"]):
                                return "following"
                            elif any(word in text_lower for word in ["запрос", "requested"]):
                                return "requested"
                            elif any(word in text_lower for word in ["подписаться", "follow"]):
                                return "not_following"
                except:
                    continue
        except Exception as e:
            print(f"⚠️ Ошибка при анализе кнопок заголовка: {e}")

        return "unknown"
        
    except Exception as e:
        print(f"❌ Ошибка при проверке состояния подписки: {e}")
        return "unknown"


def handle_following_state(page, username):
    """Обрабатывает состояние когда подписан на пользователя"""
    print(f"🔄 Обрабатываем отписку от @{username} (статус: Подписки)")
    
    try:
        # Нажимаем на кнопку "Подписки" / "Following"
        following_selectors = [
            "button:has-text('Подписки')",
            "button:has-text('Following')",
            "//button[contains(text(), 'Подписки')]",
            "//button[contains(text(), 'Following')]"
        ]
        
        for selector in following_selectors:
            try:
                if selector.startswith('//'):
                    button = page.locator(selector).first
                else:
                    button = page.locator(selector).first
                
                if button.is_visible(timeout=5000):
                    button.click()
                    print("✅ Нажали на кнопку состояния подписки")
                    time.sleep(2)
                    
                    # Теперь ищем кнопку "Отменить подписку" / "Unfollow"
                    return confirm_unfollow(page, username)
                    
            except:
                continue
        
        print("❌ Не удалось найти кнопку состояния подписки")
        return False
            
    except Exception as e:
        print(f"❌ Ошибка при обработке состояния 'Подписки': {e}")
        return False

def handle_requested_state(page, username):
    """Обрабатывает состояние когда запрос отправлен"""
    print(f"🔄 Обрабатываем отмену запроса подписки @{username} (статус: Запрос отправлен)")
    
    try:
        # Нажимаем на кнопку "Запрос отправлен" / "Requested"
        requested_selectors = [
            "button:has-text('Запрос отправлен')",
            "button:has-text('Requested')",
            "//button[contains(text(), 'Запрос отправлен')]",
            "//button[contains(text(), 'Requested')]"
        ]
        
        for selector in requested_selectors:
            try:
                if selector.startswith('//'):
                    button = page.locator(selector).first
                else:
                    button = page.locator(selector).first
                
                if button.is_visible(timeout=5000):
                    button.click()
                    print("✅ Нажали на кнопку 'Запрос отправлен'")
                    time.sleep(2)
                    
                    # Теперь ищем кнопку "Отменить запрос" / "Cancel Request"
                    return confirm_cancel_request(page, username)
                    
            except:
                continue
        
        print("❌ Не удалось найти кнопку 'Запрос отправлен'")
        return False
            
    except Exception as e:
        print(f"❌ Ошибка при обработке состояния 'Запрос отправлен': {e}")
        return False

def confirm_unfollow(page, username):
    """Подтверждает отписку от пользователя"""
    print(f"🔍 Ищем кнопку подтверждения отписки...")
    
    try:
        # Ищем кнопку "Отменить подписку" / "Unfollow"
        unfollow_selectors = [
            "button:has-text('Отменить подписку')",
            "button:has-text('Unfollow')",
            "button:has-text('Отписаться')",
            "div[role='button']:has-text('Отменить подписку')",
            "div[role='button']:has-text('Unfollow')",
            "//button[contains(text(), 'Отменить подписку')]",
            "//button[contains(text(), 'Unfollow')]"
        ]
        
        for selector in unfollow_selectors:
            try:
                if selector.startswith('//'):
                    unfollow_button = page.locator(selector).first
                else:
                    unfollow_button = page.locator(selector).first
                    
                if unfollow_button.is_visible(timeout=3000):
                    unfollow_button.click()
                    print("✅ Нажали на кнопку подтверждения отписки")
                    
                    # Ждем изменения состояния
                    time.sleep(3)
                    
                    # Проверяем что отписка прошла успешно
                    if verify_unfollow_success(page, username):
                        print(f"✅ Проверено")
                        return True
                    else:
                        print(f"⚠️ Не удалось подтвердить отписку от @{username}")
                        return False
                        
            except:
                continue
        
        print("❌ Не удалось найти кнопку подтверждения отписки")
        return False
        
    except Exception as e:
        print(f"❌ Ошибка при подтверждении отписки: {e}")
        return False

def confirm_cancel_request(page, username):
    """Подтверждает отмену запроса подписки"""
    print(f"🔍 Ищем кнопку отмены запроса...")
    
    try:
        # Ищем кнопку "Отменить запрос" / "Cancel Request"
        cancel_selectors = [
            "button:has-text('Отменить подписку')",
            "button:has-text('Cancel Request')",
            "div[role='button']:has-text('Отменить подписку')",
            "div[role='button']:has-text('Cancel Request')",
            "//button[contains(text(), 'Отменить запрос')]",
            "//button[contains(text(), 'Cancel Request')]"
        ]
        
        for selector in cancel_selectors:
            try:
                if selector.startswith('//'):
                    cancel_button = page.locator(selector).first
                else:
                    cancel_button = page.locator(selector).first
                    
                if cancel_button.is_visible(timeout=3000):
                    cancel_button.click()
                    print("✅ Нажали на кнопку 'Отменить запрос'")
                    
                    # Ждем изменения состояния
                    time.sleep(3)
                    
                    # Проверяем что отмена прошла успешно
                    if verify_cancel_success(page, username):
                        print(f"✅ Успешно отменили запрос подписки @{username}")
                        return True
                    else:
                        print(f"⚠️ Не удалось подтвердить отмену запроса @{username}")
                        return False
                        
            except:
                continue
        
        print("❌ Не удалось найти кнопку отмены запроса")
        return False
        
    except Exception as e:
        print(f"❌ Ошибка при отмене запроса: {e}")
        return False

def verify_unfollow_success(page, username):
    """Проверяет что отписка прошла успешно"""
    try:
        # Ждем появления кнопки "Подписаться"
        time.sleep(2)
        
        follow_selectors = [
            "button:has-text('Подписаться')",
            "button:has-text('Follow')",
            "//button[contains(text(), 'Подписаться')]",
            "//button[contains(text(), 'Follow')]"
        ]
        
        for selector in follow_selectors:
            try:
                if page.locator(selector).first.is_visible(timeout=3000):
                    return True
            except:
                continue
        
        # Альтернативная проверка - состояние изменилось
        current_state = check_subscription_state(page, username)
        if current_state == "not_following":
            return True
            
        return False
        
    except:
        return False

def verify_cancel_success(page, username):
    """Проверяет что отмена запроса прошла успешно"""
    try:
        # Ждем появления кнопки "Подписаться"
        time.sleep(2)
        
        follow_selectors = [
            "button:has-text('Подписаться')",
            "button:has-text('Follow')",
            "//button[contains(text(), 'Подписаться')]",
            "//button[contains(text(), 'Follow')]"
        ]
        
        for selector in follow_selectors:
            try:
                if page.locator(selector).first.is_visible(timeout=3000):
                    return True
            except:
                continue
        
        # Альтернативная проверка
        current_state = check_subscription_state(page, username)
        if current_state == "not_following":
            return True
            
        return False
        
    except:
        return False

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


def main():
    with sync_playwright() as pl:
        unfollowed_users = []
        
        browser = pl.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_default_timeout(30000)
        
        try:
            # Открываем страницу профиля
            page.goto(f"https://www.instagram.com/chebotarev.nikita/", wait_until='load')
            
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
    
        with open("followed_users.txt", "r", encoding="utf-8") as file:
            all_data = []
            for stroka in file:
                stroka = stroka[:-1]
                all_data.append(stroka)
            
            for user in all_data:
                if unfollow_user(page, user):
                    unfollowed_users.append(user)
                time.sleep(0.5)

        print("\n" + "="*50)
        print("📊 ОТЧЕТ ОБ ОТПИСКАХ")
        print("="*50)
        print(f"Всего отписок выполнено: {len(unfollowed_users)}")
        print("\nСписок отписок:")
        print("-" * 20)

        for i, usernames in enumerate(unfollowed_users, 1):
            print(f"{i:2d}. {usernames}")
        
        try:  
            os.remove("followed_users.txt")
            print('✅ Файл с подписчиками удалён')
        except Exception as e:
            print(f"🗑 Ошибка удаления: {e}")
            print("❌ Не удалось удалить файл")
            
        # Расчёт времени выполнения
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
        
        # Завершение
        close = input('Для завершения нажми Enter')
        browser.close()

# Запускаем программу
if __name__ == "__main__":
    main()