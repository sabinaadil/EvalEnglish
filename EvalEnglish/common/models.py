from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
import uuid
import os

def document_upload_path(instance, filename):
    if instance.content_type_id:
        ct = ContentType.objects.get_for_id(instance.content_type_id)
        model_name = ct.model
    else:
        model_name = 'unknown'
    email_folder = instance.uploaded_by.email.replace('@', '_').replace('.', '_')
    return os.path.join('documents', model_name, email_folder, filename)

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_documents'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    file = models.FileField(upload_to=document_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{str(self.file).split('/')[-1]} by {self.uploaded_by.email} for {self.content_type.model}"
