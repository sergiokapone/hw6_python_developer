import shutil
import sys
from pathlib import Path


from normaliser import normalise

EXT_FOLDER = {
    ("mp3", "ogg", "waw", "amr"): "audio",
    ("avi", "mp4", "mov", "mkv", "flv"): "video",
    ("jpeg", "png", "jpg", "svg"): "images",
    ("doc", "docx", "txt", "xlsx", "xls", "pptx"): "documents",
    ("djvu", "djv", "pdf", 'tiff'): "books",
    ("zip", "gz", "tar", "7z"): "archives",
    ("tex", "cls", "sty"): "LaTeX"
}

""" ============================= Функці =================================="""


def get_file_cathegory(file: str):
    """Функція повертає нвзву каталогу у відповідності до імені віхудного файлу."""

    the_path = Path(file)

    ext = the_path.suffix.lstrip(".")

    for exts in EXT_FOLDER.keys():
        if ext in exts:
            return EXT_FOLDER[exts]
    return None


def create_cathegory_folders(path: str):
    """Функція створює каталог категорії відповідно до файлу в сортованому каталозі."""

    the_path = Path(path)

    known_ext, unknown_ext = set(), set()

    cathegories = set()

    for file in the_path.glob("**/*.*"):

        cattheory = get_file_cathegory(file)

        if cattheory:
            cathegories.add(cattheory)
            known_ext.add(file.suffix)
            cathegory_path = Path(the_path.joinpath(get_file_cathegory(file)))
            cathegory_path.mkdir(exist_ok=True)

        else:
            unknown_ext.add(file.suffix)

    return tuple(cathegories), tuple(known_ext), tuple(unknown_ext)


def normalise_file_name(file: str):
    """Функція перейменовує файли з використанням функції normalise."""

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

    main_path = Path(ROOT)

    if not any(the_path.iterdir()):

        the_path.rmdir()

    else:

        for item in the_path.iterdir():

            cathegory = get_file_cathegory(item)

            if item.is_dir() and item.name not in EXT_FOLDER.values():

                sort_dir(the_path.joinpath(item.name))

            else:

                if item.is_file() and cathegory:

                    try:

                        shutil.move(
                            normalise_file_name(item),
                            main_path.joinpath(cathegory),
                        )

                        if cathegory == "archives":

                            unpack(
                                main_path.joinpath(cathegory, item.name),
                                main_path.joinpath(cathegory, item.stem),
                            )

                    except shutil.Error:

                        print("File exist")


def unpack(archive_path, path_to_unpack):
    """Розраковувач файлів."""

    try:

        shutil.unpack_archive(archive_path, path_to_unpack)

    except OSError:

        print(f"Unsupported file format {archive_path}")


def remove_empty(path):

    the_path = Path(path)

    count_removed = []

    if not any(the_path.iterdir()):

        the_path.rmdir()

    else:

        for item in the_path.iterdir():

            if item.is_dir():

                remove_empty(the_path.joinpath(item.name))

                count_removed.append(the_path.joinpath(item.name))

    return count_removed


""" ======================== Основна програма =============================="""


if __name__ == "__main__":

    try:

        ROOT = sys.argv[1]

        cathegories, known_exts, unknown_exts = create_cathegory_folders(ROOT)

        print("-------------------")
        print("Known extensions:")
        print("-------------------")

        for ext in known_exts:

            print(ext)

        print("-------------------")
        print("Unknown extensions:")
        print("-------------------")

        for ext in unknown_exts:

            print(ext)

        print("-------------------")
        print("Files in folders:")
        print("-------------------")

        sort_dir(ROOT)

        for value in cathegories:

            num_of_files = len(
                [
                    file
                    for file in Path(ROOT).joinpath(value).iterdir()
                    if file.is_file()
                ]
            )

            print(f"Cathegory {value} contain {num_of_files} files")

        remove_empty(ROOT)

    except IndexError:

        print("noup")
