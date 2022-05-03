# Keep settings

## Описание

Скрипт для копирования файлов, например, настроек системы. Скрипт можно запустить в виде автоматического сервиса копирования файлов.

## Настройка скрипта

Создайте директорию назначения автоматически (по умолчанию `~/keep-settings`), запустив команду:

```sh
/usr/bin/python3 /path/to/keep-settings/main.py
```

Или вручную:

- создайте директорию назначения и укажите ее название в `.env` файле (пример `example.env`)
- создайте файлы `.keep-settings` и `.keep-settings-ignore`

Укажите пути файлов и папок в `.keep-settings`, которые требуется сохранить:

```txt
# Строки начинающиеся с `#` игнорируются
/home/user/.local/share/fonts
.bash_aliases
~/.config/flameshot/flameshot.ini
```

Для исключения файлов и папок используйте файл `.keep-settings-ignore`. Заполнение файла аналогично `.keep-settings`.

## Использование

Запустите скрипт:

```sh
/usr/bin/python3 /path/to/keep-settings/main.py
```
