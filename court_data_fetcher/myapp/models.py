from django.db import models

class CourtQuery(models.Model):
    case_type = models.CharField(max_length=100)
    case_number = models.CharField(max_length=100)
    filing_year = models.IntegerField()
    search_timestamp = models.DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.case_type}/{self.case_number} ({self.filing_year})"

class CourtResponse(models.Model):
    query = models.ForeignKey(CourtQuery, on_delete=models.CASCADE, related_name='responses')
    raw_response = models.TextField()
    response_timestamp = models.DateTimeField(auto_now_add=True)
    http_status = models.IntegerField()
    is_success = models.BooleanField(default=False)

    def __str__(self):
        return f"Response to {self.query} ({self.http_status})"