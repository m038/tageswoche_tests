tests for tageswoche
==============

- [prerequisites](#prerequisites)
- [running tests](#running-tests)
- [running tests on machine without display](#running-tests-on-machine-without-display)

## prerequisites

####  create new virtualenv and enter it:
```sh
$ virtualenv -p python2.7 env
$ source env/bin/activate
```

####  install required packages to it:
```sh
$ pip install -r requirements.txt
```

#### install chrome-driver for testing with google chrome
instructions:
https://code.google.com/p/selenium/wiki/ChromeDriver

download link:
https://code.google.com/p/chromedriver/downloads/list

## running tests

####  run all tests:
```sh
$ nosetests -v
```

####  run particular test:
```sh
$ nosetests -v tests.test_search:SearchTestCase.test_search
```

#### run particular tests from different testcases (by name part):
```sh
$ nosetests -v {tests.test_userspace_unregistered,tests.test_userspace} -m rating
```

### running tests on machine without display
you should install Xvfb
```sh
# apt-get install xvfb
```

create new virtul display:
```sh
$ Xvfb :2 -screen 0 1024x768x24
```

and run tests with other DISPLAY variable:
```sh
$ DISPLAY=:2 nosetests -v
```
