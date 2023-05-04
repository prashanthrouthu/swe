# Install project dependencies
install:
	pip install -r requirements.txt

# Run project migrations
migrate:
	python3 manage.py migrate

# Start the Django development server
run:
	python3 manage.py runserver

