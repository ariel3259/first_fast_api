current_date_time=$(date +"%D %T")
alembic revision --autogenerate -m "$current_date_time"