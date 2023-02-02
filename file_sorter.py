from os import listdir, makedirs, rmdir, rename
from os.path import isdir, isfile, splitext, basename, exists
import shutil




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
    ('ZIP', 'GZ', 'TAR'): 'archives',
    ('DOC', 'DOCX', 'TXT', 'XLSX', 'XLS', 'PPTX'): 'documents',
    ('DJVU', 'DJV', 'PDF'): 'books'
    }


def create_folders(path):
    exts = set()
    for item in listdir(path):
        exts.add(splitext(item)[1].lstrip('.').upper())
    for ext in exts:
        for key in FOLDERS.keys():
            if ext in key:
                if not exists("/".join([path, FOLDERS[key]])):
                    makedirs("/".join([path, FOLDERS[key]]))


def move_file(path, file_name_ext):
    file_name, file_ext = splitext("/".join([path, file_name_ext]))
    file_ext = file_ext.lstrip('.').upper()

    for key in FOLDERS.keys():
        if file_ext in key:
            shutil.move("/".join([path, file_name_ext]),\
                        "/".join([path, FOLDERS[key]]))


def normalise_file_name(path, old_name_ext):
    old_name_ext = basename('/'.join([path, old_name_ext]))
    old_name, ext = splitext(old_name_ext)
    new_name = normalize(old_name)
    new_name_ext = "".join([new_name, ext])
    rename("/".join([path, old_name_ext]), "/".join([path, new_name_ext]))


def remove_empty_folder(path):
    dir = listdir(path)
    if len(dir) == 0:
        rmdir(path)
        return True
    return False


def sort_dir(path):
    for item in listdir(path):
        if isdir("/".join([path, item])) and\
                item not in FOLDERS.values():
            sort_dir("/".join([path, item]))
        else:
            create_folders(path)
            for item in listdir(path):
                if isfile("/".join([path, item])):
                    normalise_file_name(path, item)
            for item in listdir(path):
                if isfile("/".join([path, item])):
                    move_file(path, item)


sort_dir('d:/Different/Garbage')