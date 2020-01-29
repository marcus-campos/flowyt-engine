  
clean: clean-eggs clean-build
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@find . -iname '*~' -delete
	@find . -iname '*.swp' -delete
	@find . -iname '__pycache__' -delete

clean-eggs:
	@find . -name '*.egg' -print0|xargs -0 rm -rf --
	@rm -rf .eggs/

clean-build:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

black:
	pipenv run black .

pip-install:
	pipenv install --dev

runserver:
	python ./orchestrator/app.py

installer:
	rm -rf build/ && cd orchestrator/ && python installer.py build && mv build ../ && cd .. && cp -r workspaces build/orchestryzi && cp orchestrator/.env.example.build build/orchestryzi/.env.example

installer_and_zip:
	rm -rf build/ && cd orchestrator/ && python installer.py build && mv build ../ && cd .. && cp -r workspaces build/orchestryzi && cp orchestrator/.env.example.build build/orchestryzi/.env.example && zip -r build/orchestryzi.zip build/orchestryzi

runbuild:
	./build/orchestryzi/app