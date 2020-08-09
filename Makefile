  
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
	python ./flowyt/app.py

prepare_build:
	mkdir build/flowyt/bin && \
	mkdir build/flowyt/bin/lib && \
	cp .wsgi.build build/flowyt/bin/wsgi.py && \
	mv build/flowyt/lib/library.zip build/flowyt/bin/lib && \
	mv build/flowyt/lib/apps build/flowyt/bin && \
	mv build/flowyt/lib/engine build/flowyt/bin && \
	mv build/flowyt/lib/flowyt build/flowyt/bin && \
	mv build/flowyt/lib/utils build/flowyt/bin && \
	mv build/flowyt/app build/flowyt/bin && \
	mv build/flowyt/cli build/flowyt/bin && \
	rm -rf build/flowyt/lib

installer:
	make clean-build && \
	cd flowyt/ && \
	python installer.py build && \
	mv build ../ && \
	cd .. && \
	mkdir build/flowyt/workspaces && \
	cp .env.example.build build/flowyt/.env.example && \
	make prepare_build

installer_and_zip:
	make clean-build && \
	cd flowyt/ && \
	python installer.py build && \
	mv build ../ && \
	cd .. && \
	make prepare_build && \
	cp -r docs/examples/workspaces build/flowyt/workspaces && \
	cp -r docs build/flowyt/docs && \
	cp .env.example.build build/flowyt/.env.example && \
	cd build/ && \
	zip -r flowyt.zip flowyt && \
	cd ..

runbuild:
	./build/flowyt/flowyt

copydocs:
	cp -r docs/* ../flowyt-engine-demo