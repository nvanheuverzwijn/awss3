all: python_modules

python_modules:
	mkdir python_modules
	pip install -r requirements.txt --target="./python_modules" --ignore-installed

clean:
	rm -rf python_modules
	sudo rm /usr/local/bin/awss3

dev: /usr/local/bin/awss3

/usr/local/bin/awss3:
	sudo ln -s $(realpath ./bin/awss3-dev) /usr/local/bin/awss3
