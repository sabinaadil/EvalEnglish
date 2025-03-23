from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Document
from .serializers import DocumentSerializer


class DocumentUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save(uploaded_by=request.user)
            return Response(DocumentSerializer(document).data, status=201)
        return Response(serializer.errors, status=400)


class MyDocumentsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        documents = Document.objects.filter(uploaded_by=request.user)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)


class DocumentSingleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, doc_id, user):
        try:
            doc = Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            return Response({'error': 'Документ не найден'}, status=404)

        if doc.uploaded_by != user:
            return Response({'error': 'Вы не являетесь владельцем документа'}, status=403)

        return doc

    def get(self, request, doc_id):
        doc = self.get_object(doc_id, request.user)
        if isinstance(doc, Response):
            return doc
        serializer = DocumentSerializer(doc)
        return Response(serializer.data)

    def put(self, request, doc_id):
        doc = self.get_object(doc_id, request.user)
        if isinstance(doc, Response):
            return doc
        serializer = DocumentSerializer(doc, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Документ обновлён', 'document': serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, doc_id):
        doc = self.get_object(doc_id, request.user)
        if isinstance(doc, Response):
            return doc
        doc.delete()
        return Response({'message': 'Документ удалён'})


class ContentTypeListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # content_types = ContentType.objects.filter(app_label__in=[
        #     'courses', 'questions', 'lessons'
        # ])
        content_types = ContentType.objects.all()
        data = [
            {
                "id": ct.id,
                "app_label": ct.app_label,
                "model": ct.model,
                "verbose_name": ct.model_class()._meta.verbose_name.title() if ct.model_class() else None
            }
            for ct in content_types
        ]
        return Response(data)