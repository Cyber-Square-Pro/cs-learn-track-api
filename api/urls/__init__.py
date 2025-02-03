from .authentication import urlpatterns as auth_urls
from .data_retriever import urlpatterns as data_retriever_urls
from .registration import urlpatterns as registration_urls
from .testing import urlpatterns as testing_urls
from .data_deleter import urlpatterns as data_deleter_urls

urlpatterns = [
    *auth_urls,
    *data_retriever_urls,
    *registration_urls,
    *testing_urls,
    *data_deleter_urls
]
