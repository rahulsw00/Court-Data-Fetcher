from django.contrib import admin
from myapp.models import CourtQuery, CourtResponse
# Register your models here.

@admin.register(CourtQuery)
class CourtQueryAdmin(admin.ModelAdmin):
    list_display = ('case_type', 'case_number', 'filing_year', 'search_timestamp')
    search_fields = ('case_type', 'case_number')

@admin.register(CourtResponse)
class CourtResponseAdmin(admin.ModelAdmin):
    list_display = ('query', 'http_status', 'is_success', 'response_timestamp')
    list_filter = ('is_success', 'http_status')