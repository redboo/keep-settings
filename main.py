import os
import shutil

from dotenv import load_dotenv

load_dotenv()

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER = os.getlogin()
HOME = os.path.join("/home", USER)

# Директория хранения всех файлов
DIST_DIR_NAME = os.getenv("DIST", "keep-settings")
DIST = os.path.join(HOME, DIST_DIR_NAME)
# Файлы настроек с путями директорий и файлов
SETTINGS_FILE_NAME = ".keep-settings"
SETTINGS_FILE = os.path.join(DIST, SETTINGS_FILE_NAME)
IGNORE_FILE = os.path.join(DIST, ".keep-settings-ignore")


# Modified Function to ignore patterns while copying.
# Default Python Implementation does not exclude absolute path
# given for files/directories
def ignore_patterns_override(*patterns):
    """Function that can be used as copytree() ignore parameter.
    Patterns is a sequence of glob-style patterns
    that are used to exclude files/directories"""

    def _ignore_patterns(path, names):
        ignored_names = []
        for f in names:
            for pattern in patterns:
                if os.path.abspath(os.path.join(path, f)) == pattern:
                    ignored_names.append(f)
        return set(ignored_names)

    return _ignore_patterns


def init() -> None:
    """Функция инициализации.
    - Создает директорию для хранения данных. По умолчанию `~/keep-settings`
    - Создает файл игнорирования
    - Создает файл настроек и открывает его в текстовом редакторе"""

    confirm = input(f"Create and open {SETTINGS_FILE_NAME}? (y/n) [y]: ")
    if confirm in ["", "y", "yes"]:
        try:
            os.makedirs(DIST, exist_ok=True)
            open(IGNORE_FILE, "a").close()
            open(SETTINGS_FILE, "a").close()
            os.system(f"xdg-open {SETTINGS_FILE}")
        except OSError:
            print("Failed init.")
        else:
            print("Init successfully.")


def prepare_paths(filename: str) -> list[str]:
    # Получение данных из файла с путями
    paths: list[str] = []
    try:
        with open(filename, "r") as lines:
            for line in lines:
                line = line.strip()
                if line == "" or line.startswith("#"):
                    continue
                if line.startswith("~"):
                    line = line.replace("~", HOME)
                if not line.startswith("/"):
                    line = os.path.join(HOME, line)
                paths.append(line)
    except Exception:
        print("Settings file not found.")
        init()

    return paths


def main() -> None:

    COPY = prepare_paths(SETTINGS_FILE)
    IGNORE = prepare_paths(IGNORE_FILE)

    for path in COPY:
        # Проверка существования пути
        if os.path.exists(path):
            # Копирование файлов
            if os.path.isfile(path):
                dirname = os.path.dirname(path)
                if path in IGNORE or dirname in IGNORE:
                    continue
                dstpath = os.path.join(DIST, dirname.lstrip(HOME))
                os.makedirs(dstpath, exist_ok=True)
                shutil.copy2(path, dstpath)
                continue
            # Если путь - директория, то копируем все вложенные файлы
            if os.path.isdir(path):
                shutil.copytree(
                    path,
                    os.path.join(DIST, path.lstrip(HOME)),
                    ignore=ignore_patterns_override(*IGNORE),
                    dirs_exist_ok=True,
                )


# Shell скрипт сервиса, который раз в опрделенное время
# проверяет актуальность файлов

if __name__ == "__main__":
    main()
