from django.db import models
from myapp.api import ApiResult, ApiErrorResult, ApiTimeoutResult


# Create your models here.
class AiAnalysisLogManager(models.Manager):
    def create_log(self, api_result: ApiResult | ApiErrorResult | ApiTimeoutResult) -> 'AiAnalysisLog':
        match api_result:
            case ApiResult():
                return self.create(
                    image_path=api_result.image_path,
                    success=api_result.success,
                    message=api_result.message,
                    clazz=api_result.clazz,
                    confidence=api_result.confidence,
                    request_timestamp=api_result.request_timestamp,
                    response_timestamp=api_result.response_timestamp,
                )
            case ApiErrorResult():
                return self.create(
                    image_path=api_result.image_path,
                    success=False,
                    message='API Error: HTTP response code {}'.format(api_result.response_code),
                    request_timestamp=api_result.request_timestamp,
                    response_timestamp=api_result.response_timestamp,
                )
            case ApiTimeoutResult():
                return self.create(
                    image_path=api_result.image_path,
                    success=False,
                    message='API timed out',
                    request_timestamp=api_result.request_timestamp,
                    response_timestamp=api_result.response_timestamp,
                )


class AiAnalysisLog(models.Model):
    image_path = models.CharField(max_length=255, null=True)
    success = models.BooleanField(null=False)
    message = models.CharField(max_length=255, null=True)
    clazz = models.IntegerField(db_column='class', null=True)
    confidence = models.DecimalField(max_digits=5, decimal_places=4, null=True)
    request_timestamp = models.DateTimeField(null=True)
    response_timestamp = models.DateTimeField(null=True)
    objects = AiAnalysisLogManager()

    class Meta:
        db_table = 'ai_analysis_log'
