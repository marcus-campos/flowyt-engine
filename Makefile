  
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
	make clean-build && \
	cd orchestrator/ && \
	python installer.py build && \
	mv build ../ && \
	cd .. && \
	mkdir build/orchestryzi/workspaces && \
	cp orchestrator/.env.example.build build/orchestryzi/.env.example

installer_and_zip:
	make clean-build && \
	cd orchestrator/ && \
	python installer.py build && \
	mv build ../ && \
	cd .. && \
	cp -r docs/examples/workspaces build/orchestryzi/workspaces && \
	cp -r docs build/orchestryzi/docs && \
	cp orchestrator/.env.example.build build/orchestryzi/.env.example && \
	cd build/ && \
	zip -r orchestryzi.zip orchestryzi && \
	cd ..

runbuild:
	./build/orchestryzi/app