from django.core.files.storage import FileSystemStorage
import os

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # If file exists, delete it first
        if self.exists(name):
            os.remove(os.path.join(self.location, name))
        return name
