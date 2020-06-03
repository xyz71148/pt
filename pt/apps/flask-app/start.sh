export
gunicorn --chdir ${PWD} server:create_app -w 3 --threads 3 -b 0.0.0.0:${PORT}