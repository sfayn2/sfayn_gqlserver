
import os
from uuid import uuid4

def path_and_rename(instance, filename):
    ext = filename.split('.')[-1]
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(instance._meta.model_name, filename)
