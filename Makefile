test:
	python -m unittest administrator.test.tests

run_server:
	gunicorn administrator:app -b localhost:8000

debug_server:
	gunicorn administrator:app --debug -b localhost:8000
