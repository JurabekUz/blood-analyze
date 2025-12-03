
CELERY_BEAT_SCHEDULE = {
    'clean-unused-media-daily': {
        'task': 'mediafiles.tasks.clean_unused_media',
        'schedule': 60 * 60 * 24,  # 24 hours
    },
}
