from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class SupabaseMediaStorage(S3Boto3Storage):
    bucket_name = 'nismed-room-type-images'
    default_acl = 'public-read'  # or private if needed
    location = 'room_type_images'  # this becomes a folder prefix in your bucket
    file_overwrite = True # Prevent overwriting with same filename

    def url(self, name):
        # Ensure the generated URL uses the proper Supabase public URL structure
        return f"{settings.MEDIA_URL}/{self.location}/{name}"

