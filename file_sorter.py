import shutil
import sys
from pathlib import Path


from normaliser import normalise


""" =============== Таблиця відаовідності папок і розширень ================"""


EXT_FOLDER = {
    ("MP3", "OGG", "WAV", "AMR"): "audio",
    ("AVI", "MP4", "MOV", "MKV"): "video",
    ("JPEG", "PNG", "JPG", "SVG"): "images",
    ("DOC", "DOCX", "TXT", "XLSX", "XLS", "PPTX"): "documents",
    ("DJVU", "DJV", "PDF"): "books",
}

ARCHIVES = ("ZIP", "GZ", "TAR", "7Z")

EXT_FOLDER[ARCHIVES] = "archives"

FOLDERS = EXT_FOLDER.values()

EXTS = EXT_FOLDER.keys()


""" ============================= Функці =================================="""


def create_folders(path):
    """Функція створює у КАТАЛОЗІ папки відповідно до їх розширення."""

    the_path = Path(path)

    files_exts = set()

    for item in the_path.iterdir():

        if item.is_file():

            files_exts.add(item.suffix.lstrip(".").upper())

    for ext in files_exts:

        for key in EXTS:

            if ext in key:

                cathegory_path = Path(the_path.joinpath(EXT_FOLDER[key]))

                cathegory_path.mkdir(exist_ok=True)


def move_file(file):
    """Функція переміщує файли до відповідних каталогів."""

    the_path = Path(file)

    ext = the_path.suffix.lstrip(".").upper()

    name = the_path.name

    path = the_path.parent

    for key in EXTS:

        if ext in key:

            shutil.move(file, Path(path).joinpath(EXT_FOLDER[key]))

            if ext in ARCHIVES:

                unpack(
                    Path(path).joinpath(EXT_FOLDER[key], name),
                    Path(path).joinpath(EXT_FOLDER[key], file.stem),
                )


def normalise_file_name(file):
    """Функція перейменовує файли з використанням функції normalise"""

    the_path = Path(file)

    normalised_name = normalise(the_path.stem)

    new_file_path = the_path.parent.joinpath(
        "".join([normalised_name, the_path.suffix])
    )

    the_path.rename(new_file_path)

    return new_file_path


def sort_dir(path):
    """Функція фасує файли по відповідним папкам."""

    the_path = Path(path)

    if not any(the_path.iterdir()):

        the_path.rmdir()

    else:

        for item in the_path.iterdir():

            if item.is_dir() and item.name not in FOLDERS:

                sort_dir(the_path.joinpath(item.name))

            else:

                create_folders(path)

                for item in the_path.iterdir():

                    if item.is_file():

                        move_file(normalise_file_name(item))


def unpack(archive_path, path_to_unpack):
    """Розраковувач файлів."""

    try:

        shutil.unpack_archive(archive_path, path_to_unpack)

    except OSError:

        print(f"Unsupported file format {archive_path}")


""" ======================== Основна програма =============================="""


if __name__ == "__main__":

    try:

        PATH = Path(sys.argv[1])

    except IndexError:

        print(f'usage: {Path(__file__).name} indir')

        sys.exit(0)

    if PATH.is_dir():

        agreement = input(
            f"WARNING! Are you sure you want to sort the files in CATALOG {PATH}? (y/n): "
        )

        if agreement in ("y", "Y", "yes", "Yes", "YES"):

            sort_dir(PATH)

            input("Operation completed successfully! Press a any key")

        else:

            print("Operation approved!")

    else:

        print(f"Sorry, {PATH.name} is a file. You cannot process the file!")






