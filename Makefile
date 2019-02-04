install:
	pip3 install virtualenv
	virtualenv -p python3 venv
	source venv/bin/activate
	deactivate

freeze:
	pip3 freeze > requirements.txt

modules:
	pip3 install -r requirements.txt

start:
	python main.py

up:
	docker-compose up -d

down:
	docker-compose down
