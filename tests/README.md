Testing a package locally
```
pip uninstall bph_api
python3 setup.py sdist
pip install dist/bph_api-x.x.x.tar.gz
```

Upload to pip
```
python3 setup.py sdist bdist_wheel
twine upload dist/*
```

Basic test
```
python3 setup.py test
```

Reset regression test
```
python3 setup.py test --addopts --regtest-reset
```

View regression output
```
python3 setup.py test --addopts --regtest-tee
```
