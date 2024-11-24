from django.urls import path
from file_sharing_system.views import signup_page, signin_page, upload_page, list_files_page, download_file

urlpatterns = [
    path('', signin_page, name='signin'),
    path('signup/', signup_page, name='signup'),  # Correct URL for signup
    path('upload/', upload_page, name='upload'),
    path('list_files/', list_files_page, name='list_files'),
    path('download/<str:signed_file_id>/', download_file, name='download_file'),  # Signed URL for downloading
]
