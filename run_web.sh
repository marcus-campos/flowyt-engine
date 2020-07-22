# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn wsgi:app \
    --name worker_engine \
    --workers 5 \
    --log-level=info \
    --chdir=orchestrator/ \
    --bind=0.0.0.0:80