from rest_framework import serializers
from .models import *
from django.db.models import Count, Sum

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = '__all__'

class WorkerSerializer(serializers.ModelSerializer):
    branch_name = serializers.ReadOnlyField(source='branch.name')  # Add this field to get the branch name
    total_checks = serializers.SerializerMethodField() # Add this field to get the total checks
    total_check_sum = serializers.SerializerMethodField() # Add this field to get the total sum
    class Meta:
        model = Workers
        fields = ['id', 'name', 'phone_number', 'branch', 'branch_name', 'id_tg', 'total_checks', 'total_check_sum']

    def get_total_checks(self, obj):
        return obj.checks_set.count()  # Count the number of checks related to the worker
    def get_total_check_sum(self, obj):
        return obj.checks_set.aggregate(Sum('sum'))['sum__sum']  # Sum the 'sum' field of related checks

class CheksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checks
        fields = '__all__'
    
class DocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docs
        fields = '__all__'