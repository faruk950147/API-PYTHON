from rest_framework.pagination import PageNumberPagination

class CoursePagination(PageNumberPagination):
    page_size = 3                # default items per page
    page_size_query_param = 'page_size'  # user want page size change 
    max_page_size = 20           # maximum limit