from django.urls import path
from .api import (DocumentUploadAPIView, MyDocumentsListAPIView, DocumentSingleAPIView, ContentTypeListAPIView)

urlpatterns = [
    # document
    path('documents/upload/', DocumentUploadAPIView.as_view(), name='document-upload'),
    path('documents/my/', MyDocumentsListAPIView.as_view(), name='my-documents'),
    path('documents/<uuid:doc_id>/', DocumentSingleAPIView.as_view(), name='document-detail'),

    # content-type
    path('content-types/', ContentTypeListAPIView.as_view(), name='content-types'),
]
