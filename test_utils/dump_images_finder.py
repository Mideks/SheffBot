import os
from collections import defaultdict

from tinydb import TinyDB, Query

db = TinyDB('../recipes/info.json')

Film = Query()
result = [d['photo'] for d in db.all()]


def find_dump_images(directory):
    dump_images = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename not in result:
            dump_images.append(file_path)
    return dump_images


# Specify the directory to search
directory = "../recipes/photos"

# Find all dump images in the specified directory
dump_images = find_dump_images(directory)

# Print the paths of the dump images
for dump_image in dump_images:
    print(f"Dump image found: {dump_image}")
