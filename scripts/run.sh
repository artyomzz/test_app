#!/bin/bash

alembic upgrade head
while [ $? -ne 0 ]; do
    echo "Failed to run migrations. Trying again in 10 seconds..."
    sleep 10
    alembic upgrade head
done
gunicorn src.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
