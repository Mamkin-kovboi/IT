import os
import sys
import time
import socket
import subprocess

def wait_for_service(host, port, timeout=15):
    """Функция для ожидания доступности сервиса."""
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=1):
                print(f"{host}:{port} доступен после {time.time() - start_time:.2f} секунд")
                return
        except OSError:
            if (time.time() - start_time) > timeout:
                print(f"Таймаут: не удалось подключиться к {host}:{port} после {timeout} секунд", file=sys.stderr)
                sys.exit(1)
            print(f"Ожидаем, {host}:{port} не доступен...")
            time.sleep(1)

def main():
    # Извлекаем данные из среды
    db_host = os.getenv("DB_HOST", "db")  # db - имя сервиса в docker-compose
    db_port = os.getenv("DB_PORT", "5433")  # Порт PostgreSQL по умолчанию

    # Ждем, пока база данных станет доступна
    wait_for_service(db_host, db_port)

    # Запускаем миграции
    try:
        print("Запуск миграций...")
        subprocess.run(["yoyo-migrations", "migrations"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении миграций: {e.stderr}", file=sys.stderr)
        sys.exit(e.returncode)

    # Запускаем ваше приложение (например, Uvicorn)
    try:
        print("Запуск приложения...")
        subprocess.run(["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app:app"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при запуске приложения: {e.stderr}", file=sys.stderr)
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()