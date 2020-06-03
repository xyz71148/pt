export
gunicorn --chdir ${PWD} server:app -w 3 --threads 3 -b 0.0.0.0:${PORT}