from .configs import celery_app

@celery_app.task(name="test_celery")
def test_celery():
    return "Hello World!"
