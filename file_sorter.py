from os import listdir, makedirs, rmdir, rename
from os.path import isdir, isfile, splitext, basename, exists
import shutil
import sys


"""
Скрипт приймає один аргумент при запуску — це ім'я папки,
в якій він буде проводити сортування.
Допустимо файл з програмою називається
sort.py, тоді, щоб відсортувати папку /user/Desktop/Мотлох,
треба запустити скрипт командою python sort.py /user/Desktop/Мотлох

В результатах роботи повинні бути:

Список файлів в кожній категорії (музика, відео, фото и ін.)
Перелік усіх відомих скрипту розширень, які зустрічаються в цільовій папці.
Перелік всіх розширень, які скрипту невідомі.
Після необхідно додати функції, які будуть
відповідати за обробку кожного типу файлів.

Крім того, всі файли та папки треба перейменувати,
видалив із назви всі символи, що призводять до проблем.
Для цього треба застосувати до імен файлів функцію normalize.
Слід розуміти, що перейменувати файли треба так,
щоб не змінити розширень файлів.

Функція normalize:

Проводить транслітерацію кирилічного алфавіту на латинський.
Замінює всі символи крім латинських літер, цифр на '_'.
Вимоги до функції normalize:

приймає на вхід рядок та повертає рядок;
проводить транслітерацію кирилічних символів на латиницю;
замінює всі символи, крім літер латинського алфавіту та цифр, на символ '_';
транслітерація може не відповідати стандарту, але бути читабельною;
великі літери залишаються великими,
а маленькі — маленькими після транслітерації.

"""


PATH = sys.argv[1]

TRANS = {'а': 'a',
 'А': 'A',
 'б': 'b',
 'Б': 'B',
 'в': 'v',
 'В': 'V',
 'г': 'g',
 'Г': 'G',
 'д': 'd',
 'Д': 'D',
 'е': 'e',
 'Е': 'E',
 'ё': 'e',
 'Ё': 'E',
 'ж': 'j',
 'Ж': 'J',
 'з': 'z',
 'З': 'Z',
 'и': 'i',
 'И': 'I',
 'й': 'j',
 'Й': 'J',
 'к': 'k',
 'К': 'K',
 'л': 'l',
 'Л': 'L',
 'м': 'm',
 'М': 'M',
 'н': 'n',
 'Н': 'N',
 'о': 'o',
 'О': 'O',
 'п': 'p',
 'П': 'P',
 'р': 'r',
 'Р': 'R',
 'с': 's',
 'С': 'S',
 'т': 't',
 'Т': 'T',
 'у': 'u',
 'У': 'U',
 'ф': 'f',
 'Ф': 'F',
 'х': 'h',
 'Х': 'H',
 'ц': 'ts',
 'Ц': 'TS',
 'ч': 'ch',
 'Ч': 'CH',
 'ш': 'sh',
 'Ш': 'SH',
 'щ': 'sch',
 'Щ': 'SCH',
 'ъ': '',
 'Ъ': '',
 'ы': 'y',
 'Ы': 'Y',
 'ь': '',
 'Ь': '',
 'э': 'e',
 'Э': 'E',
 'ю': 'yu',
 'Ю': 'YU',
 'я': 'ya',
 'Я': 'YA',
 'є': 'je',
 'Є': 'JE',
 'і': 'i',
 'І': 'I',
 'ї': 'ji',
 'Ї': 'JI',
 'ґ': 'g',
 'Ґ': 'G'}

# https://www.w3schools.com/charsets/ref_utf_cyrillic.asp
LATIN_CODES = tuple(range(65, 91)) + tuple(range(97, 123))
CYR_CODES = tuple(range(1024, 1280))
OTHER_SYMBOLS = tuple(str(x) for x in range(0, 10)) + tuple()


def normalize(file_name):
    """Функція normalize - проводить транслітерацію кирилічного алфавіту.

    - Приймає на вхід рядок - ім'я файлу (без розширення) та повертає
    нормалізований рядок.
    - Танслітерує кирилчну назву в латиницю:
      -- транслітерація може не відповідати стандарту, але бути читабельною;
      -- великі літери залишаються великими;
      -- маленькі залишаються маленькими після транслітерації.
    - Замінює всі символи крім латинських літер, цифр на '_'.

    """

    trans = ""  # ініціалізаці

    for letter in file_name:
        if ord(letter) in LATIN_CODES or letter in OTHER_SYMBOLS:
            trans += letter
        elif ord(letter) in CYR_CODES:
            trans += TRANS.get(letter)
        else:
            trans += '_'

    return trans


FOLDERS = {
    ('MP3', 'OGG', 'WAV', 'AMR'): 'audio',
    ('AVI', 'MP4', 'MOV', 'MKV'): 'video',
    ('JPEG', 'PNG', 'JPG', 'SVG'): 'images',
    ('DOC', 'DOCX', 'TXT', 'XLSX', 'XLS', 'PPTX'): 'documents',
    ('DJVU', 'DJV', 'PDF'): 'books'
    }

ARCHIVES = ('ZIP', 'GZ', 'TAR', '7Z')
FOLDERS[ARCHIVES] = 'archives'


def full_path(path, item):
    """Функція приймає шлях до файлу чи папки і об'єднує їх у повний шлях.

    """

    return "/".join([path, item])


def separate_file_name_ext(path, item):
    """Функція повертає ім'я та розширення файлу (у верхньому регістрі).

    На вхід подається шлях до файлу, та його ім'я зрозширенням.
    Якщо на вхід подається імя папки, то повертає кортеж двох порожніх рядків.
    """

    full_item_path = full_path(path, item)

    if isfile(full_item_path):
        name, ext = splitext(basename(full_item_path))
        return name, ext.lstrip('.').upper()
    return "", ""


def create_folders(path):
    """Функція створює у КАТАЛОЗІ папки відповідно до їх розширення.

    Приймає шлях до КАТАЛОГУ.

    Дані про відповідність розширення і каталогу
    знаходяться в словнику FOLDERS.
    """

    exts = set()
    for item in listdir(path):
        file_ext = separate_file_name_ext(path, item)[1]
        exts.add(file_ext)

    for ext in exts:
        for key in FOLDERS.keys():
            if ext in key:
                if not exists(full_path(path, FOLDERS[key])):
                    makedirs(full_path(path, FOLDERS[key]))


def move_file(path, file_name_ext):
    """Функція переміщує файли до відповідних каталогів.

    Приймає шлях до КАТАЛОГУ і та ім'я файлу з розширенням.

    Дані про відповідність розширення і каталогу
    знаходяться в словнику FOLDERS.
    """

    file_name, file_ext = separate_file_name_ext(path, file_name_ext)
    full_path_to_file = full_path(path, file_name_ext)
    for key in FOLDERS.keys():
        if file_ext in key:
            shutil.move(full_path_to_file,
                        full_path(path, FOLDERS[key]))
            if file_ext in ARCHIVES:
                full_path_to_arj_file = full_path(path, FOLDERS[key])
                unpack(
                       full_path(full_path_to_arj_file, file_name_ext),
                       full_path(full_path_to_arj_file, file_name)
                        )


def normalise_file_name(path, old_name_ext):
    """Функція перейменовує файли відповідно до таблиці транслітерації TRANS.

    Приймає шлях до файлу та його ім'я з розширенням.

    """
    old_name, ext = separate_file_name_ext(path, old_name_ext)
    new_name = normalize(old_name)
    new_name_ext = ".".join([new_name, ext.lower()])
    full_path_old_name_file = full_path(path, old_name_ext)
    full_path_new_name_file = full_path(path, new_name_ext)
    rename(full_path_old_name_file, full_path_new_name_file)


def sort_dir(path):
    """Функція фасує файли по відповідним папкам.

    Приймає шлях до КАТАЛОГУ.

    """
    if len(listdir(path)) == 0:
        rmdir(path)
    else:
        for item in listdir(path):
            if isdir(full_path(path, item)) and\
                    item not in FOLDERS.values():
                sort_dir(full_path(path, item))
            else:
                create_folders(path)
                for item in listdir(path):
                    if isfile(full_path(path, item)):
                        normalise_file_name(path, item)
                        move_file(path, item)


def unpack(archive_path, path_to_unpack):
    """Розраковувач файлів.

    """
    try:
        shutil.unpack_archive(archive_path, path_to_unpack)
    except (OSError, IOError):
        print(f"Unsupported file format {archive_path}")


if __name__ == '__main__':
    path = PATH
    agrreemetnt = input(
        f'УВАГА! Ви впевнені, що шочере сортувати файли в КАТАЛОЗІ {path}? (y/n):'
        )
    if agrreemetnt in ('y', 'Y', 'н', 'Н'):
        sort_dir(path)
        input('Операція успішно завершена! Натисніть довільну клавішу')
    else:
        print('Операція відмінена!')
