from django.urls import path
from .views import *
urlpatterns = [
    path('branch/', BranchesListCreateView.as_view(), name='branch_list_create'),
    path('branch/<int:pk>', BranchesListUpdateDeleteRetriveView.as_view(), name='branch_update_delete'),
    path('branch/<int:pk>/workers/', WorkersByBranchListView.as_view(), name='branch-workers-list'),
    
    path('worker/', WorkersListCreateView.as_view(), name='_list_create'),
    path('worker/<int:pk>', WorkersListUpdateDeleteRetriveView.as_view(), name='_update_delete'),
    path('worker/<str:phone_number>', WorkersListRetriveView.as_view(), name='worker_check'),
    path('worker/id/<int:id_tg>', WorkersListByID.as_view(), name='worker_check_by_id'),
    
    path('check/', CheckListCreateView.as_view(), name='check_list_create'),
    path('edited_checks/', EditedTextsCheck.as_view(), name='edited_checks'),
    
    path('doc/', DocListCreateView.as_view(), name='doc_list_create'),

    path('worker_filter/', WorkersSummaryView.as_view(), name='checks-by-date'),
    path('branch_filter/', BranchesSummaryView.as_view(), name='branch_filter'),
]
