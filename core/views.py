from rest_framework import generics, filters
from .models import *
from .serializers import *

from datetime import datetime, timedelta
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.permissions import IsAdminUser

from rest_framework.response import Response
from rest_framework.views import APIView
from pprint import pprint

class BranchesListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = Branches.objects.all()
    serializer_class = BranchSerializer

class BranchesListUpdateDeleteRetriveView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = Branches.objects.all()
    serializer_class = BranchSerializer

class WorkersListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = Workers.objects.all()
    serializer_class = WorkerSerializer

class WorkersListUpdateDeleteRetriveView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = Workers.objects.all()
    serializer_class = WorkerSerializer

class WorkersListRetriveView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = Workers.objects.all()
    serializer_class = WorkerSerializer
    lookup_field = 'phone_number'

class WorkersListByID(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = Workers.objects.all()
    serializer_class = WorkerSerializer
    lookup_field = 'id_tg'

class CheckListCreateView(generics.ListCreateAPIView):
    serializer_class = CheksSerializer

    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'worker': ['exact'],  # Use 'exact' lookup for worker foreign key
        'branch': ['exact'],  # You can also specify 'exact' lookup for branch if needed
    }

    def list(self, request):
        date_filter = self.request.query_params.get('date', None)
        regular = self.request.query_params.get('specific', None)
        start_date = None
        end_date = None

        if regular:
            try:
                # Try parsing the date_filter as %Y-%m-%d
                start_date = datetime.strptime(regular, '%Y-%m-%d')
                end_date = start_date + timedelta(days=1) - timedelta(seconds=1)
            except ValueError:
                try:
                    # Try parsing the date_filter as %Y-%m
                    start_date = datetime.strptime(regular, '%Y-%m')
                    end_date = datetime(year=start_date.year, month=start_date.month + 1, day=1) - timedelta(days=1)
                except ValueError:
                    try:
                        # Try parsing the date_filter as %Y
                        current_month = datetime.now().month
                        current_day = datetime.now().day
                        start_date = datetime.strptime(regular, '%Y')
                        end_date = datetime(year=start_date.year, month=current_month, day=current_day)
                    except ValueError:
                        pass

        if date_filter == '1day':
            start_date = datetime.now() - timedelta(days=1)
        elif date_filter == '1month':
            start_date = datetime.now() - timedelta(days=30)  # Approximation for 1 month
        elif date_filter == '1year':
            start_date = datetime.now() - timedelta(days=365)  # Approximation for 1 year
        elif date_filter == 'custom':
            s_date = self.request.query_params.get('from', None)
            e_date = self.request.query_params.get('to', None)
            
            start_date = datetime.strptime(s_date, '%Y-%m-%d')
            end_date = datetime.strptime(e_date, '%Y-%m-%d')

        elif date_filter == 'check_num':
            check_num = self.request.query_params.get('check_num', None)
            if check_num:
                queryset = Checks.objects.filter(check_num=check_num)
                return queryset
        elif date_filter == 'all':
            return Checks.objects.all()
 
        else:
            try:
                keys = list(self.request.query_params.keys())
                if keys[0] not in ['worker', 'branch', 'regular']:
                    return Checks.objects.none()
                else:
                    pass
            except:
                return Checks.objects.none()

        queryset = Checks.objects.all()

        if start_date and end_date:
            queryset = queryset.filter(date__date__gte=start_date, date__date__lte=end_date)
        elif start_date:
            queryset = queryset.filter(date__gte=start_date)
        
        total_checks = queryset.count()
        total_check_sum = queryset.aggregate(Sum('sum'))['sum__sum']

        b = {'total_checks': total_checks, 'total_sum': total_check_sum}

        a=CheksSerializer(queryset, many=True).data

        data = {
            'list': a,
            'sum': b, 
        }

        return Response(data)

class DocListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    serializer_class = DocsSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['worker', 'branch']  # Add any additional filtering fields you need

    def get_queryset(self):
        date_filter = self.request.query_params.get('date_filter', None)
        start_date = None
        end_date = None

        if date_filter == '1day':
            start_date = datetime.now() - timedelta(days=1)
        elif date_filter == '1month':
            start_date = datetime.now() - timedelta(days=30)  # Approximation for 1 month
        elif date_filter == '1year':
            start_date = datetime.now() - timedelta(days=365)  # Approximation for 1 year
        elif date_filter == 'custom':
            start_date = self.request.query_params.get('start_date', None)
            end_date = self.request.query_params.get('end_date', None)
        elif date_filter == 'specific_day':
            specific_day = self.request.query_params.get('specific_day', None)
            if specific_day:
                start_date = datetime.strptime(specific_day, '%Y-%m-%d')
                end_date = start_date + timedelta(days=1) - timedelta(seconds=1)
        
        elif date_filter == 'specific_month':
            specific_month = self.request.query_params.get('specific_month', None)
            if specific_month:
                # Assume the current day
                current_day = datetime.now().day
                start_date = datetime.strptime(specific_month, '%Y-%m')
                end_date = datetime(year=start_date.year, month=start_date.month + 1, day=1) - timedelta(days=1)
        
        elif date_filter == 'specific_year':
            specific_year = self.request.query_params.get('specific_year', None)
            if specific_year:
                # Assume the current month and day
                current_month = datetime.now().month
                current_day = datetime.now().day
                start_date = datetime.strptime(specific_year, '%Y')
                end_date = datetime(year=start_date.year, month=current_month, day=current_day)
            
        elif date_filter == 'doc_num':
            doc_num = self.request.query_params.get('doc_num', None)
            if doc_num:
                queryset = Docs.objects.filter(doc_num=doc_num)
                return queryset
        elif date_filter == 'all':
            return Docs.objects.all()
        else:
            try:
                keys = list(self.request.query_params.keys())
                if keys[0] not in ['worker', 'branch']:
                    return Docs.objects.none()
                else:
                    pass
            except:
                return Docs.objects.none()

        queryset = Docs.objects.all()
        if start_date and end_date:
            queryset = queryset.filter(date__date__gte=start_date, date__date__lte=end_date)
        elif start_date:
            queryset = queryset.filter(date__gte=start_date)

        return queryset

class WorkersByBranchListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = WorkerSerializer

    def get_queryset(self):
        branch_id = self.kwargs['pk']  # Get the branch_id from URL parameter
        queryset = Workers.objects.filter(branch_id=branch_id)
        return queryset
    
class WorkersSummaryView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        date_filter = request.query_params.get('date', None)
        start_date = request.query_params.get('from', None)
        end_date = request.query_params.get('to', None)
        branches = request.query_params.get('branch', None)

        selected_date = None
        if date_filter:
            try:
                # Parse the date filter as %Y-%m-%d
                selected_date = datetime.strptime(date_filter, '%Y-%m-%d')
            except:
                try:
                    # Parse the date filter as %Y-%m-%d
                    selected_date = datetime.strptime(date_filter, '%Y-%m')
                except:
                    try:
                        # Parse the date filter as %Y-%m-%d
                        selected_date = datetime.strptime(date_filter, '%Y')
                    except ValueError:
                        # Handle invalid date format
                        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
        else:
            pass
        # Get all workers
        if branches != 'null':
            workers = Workers.objects.filter(branch_id=branches)
        else:
            workers = Workers.objects.all()
        summary_data = []

        for worker in workers:
            # Filter checks for the worker on the specified date
            if selected_date:
                worker_checks = Checks.objects.filter(worker=worker, date__date=selected_date.date())

            else:
                s_date = datetime.strptime(start_date, '%Y-%m-%d')
                e_date = datetime.strptime(end_date, '%Y-%m-%d')
                worker_checks = Checks.objects.filter(worker=worker, date__date__gte=s_date, date__date__lte=e_date)
                
            total_checks = worker_checks.count()
            total_check_sum = worker_checks.aggregate(Sum('sum'))['sum__sum']
            data = {
                'id': worker.id,
                'name': worker.name,
                'total_checks': total_checks,
                'total_check_sum': total_check_sum,
                'branch_name': BranchSerializer(worker.branch).data['name']
            }
            summary_data.append(data)
        return Response(summary_data, status=200)
