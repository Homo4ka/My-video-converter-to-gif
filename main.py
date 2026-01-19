import os, time, sys, moviepy
from pathlib import Path
from moviepy import VideoFileClip
from PIL import Image

def clear_screen():
    """Очистка экрана консоли"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Отображение заголовка программы"""
    print("=" * 50)
    print("      КОНВЕРТЕР ВИДЕО В GIF")
    print("=" * 50)
    print()

def convert_vid_to_gif(input_path, output_path, fps=10, resize=None):
    """Конвертирует одно видео в GIF
    
    Args:
        input_path: путь к входному видео файлу
        output_path: путь для сохранения GIF
        fps: кадров в секунду (по умолчанию 10)
        resize: кортеж (ширина, высота) для изменения размера"""
    try:
        print(f"Начинаю конвертацию: {Path(input_path).name}")
        print(f"Выходной файл: {Path(output_path).name}")
        
        #загружаем видео
        clip = VideoFileClip(input_path)
        
        #изменяем размер когда требуется
        if resize:
            clip = clip.resize(resize)
        
        #сохраняем как GIF
        clip.write_gif(output_path, fps=fps)
        
        print(f"✓ Успешно конвертировано: {Path(output_path).name}")
        print(f"Размер файла: {os.path.getsize(output_path) / 1024:.2f} КБ")
        return True
        
    except Exception as e:
        print(f"✗ Ошибка при конвертации: {e}")
        return False
    finally:
        if 'clip' in locals():
            clip.close()

def convert_single_video():
    """Меню для конвертации одного видео"""
    clear_screen()
    display_header()
    print("РЕЖИМ: Конвертация одного видео")
    print("-" * 30)
    
    #ввод пути к файлу
    while True:
        video_path = input("Введите путь к видеофайлу(ctrl + c для выхода из программы): ").strip()
        
        if not os.path.exists(video_path):
            print("Файл не найден! Попробуйте снова")
            continue
            
        if not video_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
            print("Поддерживаемые форматы: .mp4, .avi, .mov, .mkv, .webm")
            continue
        break
    
    #ввод имени выходного файла
    default_name = Path(video_path).stem + ".gif"
    output_name = input(f"Имя выходного файла [{default_name}]: ").strip()
    if not output_name:
        output_name = default_name
    
    #настройки конвертации
    print("\nНастройки конвертации:")
    print("1. Стандартные (FPS: 10, без изменения размера)")
    print("2. Высокое качество (FPS: 15)")
    print("3. Пользовательские настройки")
    
    choice = input("Выберите вариант [1]: ").strip() or "1"
    
    fps = 10
    resize = None
    
    if choice == "2":
        fps = 15
    elif choice == "3":
        try:
            fps = int(input("FPS (рекомендуется 5-15): ").strip() or "10")
            resize_choice = input("Изменить размер? (y/n) [n]: ").strip().lower()
            if resize_choice == 'y':
                width = int(input("Ширина (в пикселях): "))
                height = int(input("Высота (в пикселях): "))
                resize = (width, height)
        except ValueError:
            print("Неверный ввод, использую стандартные настройки")
    
    #конвертация
    print("\n" + "=" * 30)
    print("Начинаю конвертацию...")
    
    try:
        convert_vid_to_gif(video_path, output_name, fps, resize)
    except KeyboardInterrupt:
        print("\nКонвертация прервана пользователем")
    
    input("\nНажмите Enter чтобы вернуться в меню...")

def convert_multiple_videos():
    """Меню для конвертации нескольких видео"""
    clear_screen()
    display_header()
    print("РЕЖИМ: Пакетная конвертация видео")
    print("-" * 30)
    
    #выбор папки или файлов
    print("Выберите способ:")
    print("1. Конвертировать все видео в папке")
    print("2. Выбрать несколько файлов")
    
    mode = input("Ваш выбор [1]: ").strip() or "1"
    
    video_files = []
    
    if mode == "1":
        #все видео в папке
        folder_path = input("Введите путь к папке(ctrl + c для выхода из программы): ").strip()
        
        if not os.path.exists(folder_path):
            print("Папка не найдена!")
            input("\nНажмите Enter чтобы вернуться...")
            return
            
        #собираем все видео файлы
        video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.webm')
        for file in os.listdir(folder_path):
            if file.lower().endswith(video_extensions):
                video_files.append(os.path.join(folder_path, file))
                
    elif mode == "2":
        #ручной выбор файлов
        print("\nВведите пути к файлам (по одному, пустая строка для завершения):")
        while True:
            file_path = input(f"Файл {len(video_files) + 1}: ").strip()
            
            if not file_path:
                break
                
            if not os.path.exists(file_path):
                print("Файл не найден!")
                continue
                
            video_files.append(file_path)
    
    if not video_files:
        print("Не найдено видео файлов для конвертации!")
        input("\nНажмите Enter чтобы вернуться...")
        return
    
    #настройки конвертации
    print(f"\nНайдено {len(video_files)} видео файлов")
    print("\nНастройки конвертации для всех файлов:")
    fps = input("FPS (по умолчанию 10): ").strip()
    fps = int(fps) if fps.isdigit() else 10
    
    resize_choice = input("Изменить размер всех GIF? (y/n) [n]: ").strip().lower()
    resize = None
    if resize_choice == 'y':
        try:
            width = int(input("Ширина (в пикселях): "))
            height = int(input("Высота (в пикселях): "))
            resize = (width, height)
        except ValueError:
            print("Неверный ввод, размер не изменен")
    
    #папка для сохранения
    output_dir = input("Папка для сохранения [gif_output]: ").strip()
    output_dir = output_dir if output_dir else "gif_output"
    os.makedirs(output_dir, exist_ok=True)
    
    #конвертация
    print("\n" + "=" * 30)
    print("Начинаю пакетную конвертацию...")
    
    success_count = 0
    for i, video_path in enumerate(video_files, 1):
        print(f"\n[{i}/{len(video_files)}] Конвертирую: {Path(video_path).name}")
        
        output_name = os.path.join(output_dir, Path(video_path).stem + ".gif")
        
        if convert_vid_to_gif(video_path, output_name, fps, resize):
            success_count += 1
    
    print(f"\n" + "=" * 30)
    print(f"Готово! Успешно конвертировано: {success_count}/{len(video_files)}")
    print(f"Файлы сохранены в: {os.path.abspath(output_dir)}")
    
    input("\nНажмите Enter чтобы вернуться в меню...")

def display_help():
    """Отображение справки"""
    clear_screen()
    display_header()
    print("СПРАВКА")
    print("-" * 30)
    print("\nРекомендации:")
    print("• FPS (кадры в секунду):")
    print("  - 5-8: маленький размер файла")
    print("  - 10-12: оптимально для большинства видео")
    print("  - 15+: высокое качество, большие файлы")
    print("\n• Размер изображения:")
    print("  - Стандартный размер для соцсетей: 480x270")
    print("  - Для сохранения качества: оригинальный размер")
    print("  - Меньший размер = меньший файл")
    print("\n• Поддерживаемые форматы видео:")
    print("  MP4, AVI, MOV, MKV, WebM")
    print("\n• Требования:")
    print("  - Установленный FFmpeg")
    print("  - Достаточно места на диске")
    
    input("\nНажмите Enter чтобы вернуться в меню...")

def main_menu():
    """Главное меню программы"""
    while True:
        clear_screen()
        display_header()
        
        print("ГЛАВНОЕ МЕНЮ:")
        print("1. Конвертировать одно видео")
        print("2. Конвертировать несколько видео")
        print("3. Справка и рекомендации")
        print("4. Выход")
        print()
        
        choice = input("Выберите действие (1-4): ").strip()
        
        if choice == "1":
            convert_single_video()
        elif choice == "2":
            convert_multiple_videos()
        elif choice == "3":
            display_help()
        elif choice == "4":
            print("\nДо свидания!")
            sys.exit(0)
        else:
            print("\nНеверный выбор! Попробуйте снова.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nПрограмма завершена пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        sys.exit(1)