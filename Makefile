rundev:
	uv run flask run --debug

reload:
	start cmd /k browser-sync 'http://127.0.0.1:5000' --files .

makemigrations:
	uv run alembic revision --autogenerate -m $(m)

migrate:
	uv run alembic upgrade head

sass:
	sass --watch ./static/styles.scss ./static/styles.css