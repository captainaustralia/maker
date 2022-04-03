import os


def get_file_path(obj, fname):
    return os.path.join(
        'media',
        obj.company.name,
        fname
    )
