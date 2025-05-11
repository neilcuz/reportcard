# Makefile for ReportCard project

.PHONY: run clean-data freeze install lint dev

run:
	source venv/bin/activate && streamlit run main.py

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

clean-data:
	python scripts/clean_schools.py

lint:
	flake8 app scripts main.py

dev:
	source venv/bin/activate && make install && make run

check:
	make lint && make freeze

amend:
	git add .
	git commit --amend --no-edit
	git push --force

commit:
	@if [ -z "$(m)" ]; then \
		echo "❌ Please provide a commit message with: make commit m='your message'"; \
		exit 1; \
	fi
	git add .
	git commit -m "$(m)"
	git push