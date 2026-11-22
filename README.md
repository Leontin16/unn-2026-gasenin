# unn-2026-gasenin

Учебный Telegram-эхо-бот. На входящее текстовое сообщение бот отвечает тем же текстом. Стикеры, файлы, голосовые сообщения, видеокружки и остальные нетекстовые сообщения игнорируются.

## Архитектура

- `bot/messenger.py` — интерфейс `Messenger`. Компоненты приложения зависят от интерфейса, а не от Telegram-клиента.
- `bot/telegram_messenger.py` — реализация интерфейса через Telegram Bot API.
- `bot/long_polling.py` — long polling: получение обновлений, управление `offset` и передача обновлений диспетчеру.
- `bot/dispatcher.py` — диспетчер, который последовательно вызывает обработчики.
- `bot/handler.py` — базовый интерфейс обработчика и статусы цепочки.
- `bot/handlers/message_text.py` — эхо текстовых сообщений. После успешной отправки ответа печатает точку в терминал.
- `tests/` — тесты long polling, dispatcher и handler.

## Переменные окружения

Обязательны две переменные:

- `TELEGRAM_TOKEN` — токен от BotFather.
- `TELEGRAM_BASE_URL` — адрес Telegram Bot API, например `https://api.telegram.org`.

Токен не хранится в исходном коде и не добавляется в Git.

## Запуск локально (Ubuntu)

```bash
sudo apt update
sudo apt install -y python3 python3-venv make
make install

read -rsp "Telegram token: " TELEGRAM_TOKEN
echo
export TELEGRAM_TOKEN
export TELEGRAM_BASE_URL="https://api.telegram.org"

python3 -m bot
```

Остановка — `Ctrl+C`. В терминале печатается точка за каждый успешно отправленный эхо-ответ.

## Проверки

```bash
make test          # тесты
make format-check  # проверка форматирования
make format        # исправление форматирования
make lint-check    # проверка Ruff
make lint          # автоисправление замечаний Ruff
make type-check    # проверка типов Mypy
make check         # все проверки сразу
```

## Docker

```bash
docker build -t unn-2026-gasenin-bot .
docker run --rm \
  -e TELEGRAM_TOKEN="$TELEGRAM_TOKEN" \
  -e TELEGRAM_BASE_URL="https://api.telegram.org" \
  unn-2026-gasenin-bot
```

## GitHub Actions и GHCR

Pull request проверяет форматирование, линтер, типы, тесты и сборку Docker-образа. После push/merge в ветку `master` workflow публикует образ в GitHub Container Registry:

```text
ghcr.io/<github-user>/unn-2026-gasenin:latest
```

После первой публикации откройте Package settings на GitHub и установите видимость пакета `Public`, если тестирующая система должна скачивать образ без авторизации.
