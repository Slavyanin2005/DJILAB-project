import os

from django.conf import settings
from django.utils.text import slugify
from minio import Minio
from minio.error import S3Error

# Инициализация клиента MinIO
# settings.MINIO_URL обычно http://minio:9000, нам нужен только хост
minio_host = settings.MINIO_URL.replace("http://", "").replace("https://", "")

minio_client = Minio(
    minio_host,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False,  # Для локальной разработки
)


def init_bucket():
    """Проверяет существование бакета, если нет - создает."""
    try:
        if not minio_client.bucket_exists(settings.MINIO_BUCKET):
            minio_client.make_bucket(settings.MINIO_BUCKET)
            print(f"Бакет {settings.MINIO_BUCKET} создан.")
        else:
            print(f"Бакет {settings.MINIO_BUCKET} уже существует.")
    except S3Error as e:
        print(f"Ошибка MinIO: {e}")


def generate_unique_filename(original_filename, service_name):
    """Генерирует уникальное имя файла на латинице."""
    # Преобразуем название услуги в транслит/латиницу для пути
    safe_name = slugify(service_name)
    if not safe_name:
        safe_name = "file"

    # Получаем расширение
    _, ext = os.path.splitext(original_filename)
    # Формируем новое имя (можно добавить uuid для уникальности, но по ТЗ нужно просто латиницу)
    # Для простоты используем timestamp или просто имя,
    # но для уникальности лучше добавить немного рандома или использовать id услуги, если он есть.
    # Пока сделаем простое уникальное имя.
    import uuid

    unique_name = f"{safe_name}_{uuid.uuid4().hex}{ext}"
    return unique_name


def upload_to_minio(file_obj, object_name):
    """Загружает файл в MinIO."""
    try:
        minio_client.put_object(
            settings.MINIO_BUCKET,
            object_name,
            file_obj,
            length=file_obj.size,
            content_type=file_obj.content_type,
        )
        return object_name
    except S3Error as e:
        print(f"Ошибка загрузки: {e}")
        return None


def delete_from_minio(object_name):
    """Удаляет файл из MinIO."""
    try:
        minio_client.remove_object(settings.MINIO_BUCKET, object_name)
        return True
    except S3Error as e:
        print(f"Ошибка удаления: {e}")
        return False
