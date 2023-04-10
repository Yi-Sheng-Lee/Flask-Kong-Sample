eval "flask db init"
sleep 3
eval "flask db migrate -m 'INITIABLE'"
sleep 3
eval "flask db upgrade"
sleep 3
eval "python3 start_job.py"
sleep 10
eval "python3 main.py"