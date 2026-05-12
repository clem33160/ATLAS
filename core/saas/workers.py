JOBS = {
    "document_import": "pending",
    "ocr": "pending",
    "classification": "pending",
    "indexing": "pending",
    "connector_sync": "pending",
}


def run_job(job_name: str) -> str:
    if job_name not in JOBS:
        raise KeyError("unknown job")
    JOBS[job_name] = "queued"
    return JOBS[job_name]
