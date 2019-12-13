import pip

REQUIRED_PACKAGES = [
	'Django==2.2.7',
	'feedparser',
	'bs4',
	'lxml',
	'sqlparse',
	'fpdf',
]

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])


if __name__ == '__main__':
    for package in REQUIRED_PACKAGES:
    	install(package)