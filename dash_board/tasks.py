# tasks.py
from celery import shared_task
from import_export.formats.base_formats import CSV
from import_export.results import RowResult
from tablib import Dataset
from .resources import EmployeeResource

@shared_task
def run_employee_import(data, file_name=None):
    resource = EmployeeResource()
    dataset = Dataset().load(data, format='csv')
    result = resource.import_data(dataset, dry_run=False, raise_errors=True, file_name=file_name)
    return {
        "success": resource.row_success,
        "skipped": resource.row_skipped,
        "failed": resource.row_failed,
        "total": len(dataset),
        "row_results": [r.import_type for r in result.rows if isinstance(r, RowResult)]
    }
