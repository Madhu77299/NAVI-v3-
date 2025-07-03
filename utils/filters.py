def filter_jobs(jobs, keywords):
    filtered = []
    for job in jobs:
        if any(keyword.lower() in job["title"].lower() for keyword in keywords):
            filtered.append(job)
    return filtered