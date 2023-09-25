## Prerequisite

- [virtualenv](https://pypi.org/project/virtualenv/)
- [django](https://pypi.org/project/Django/)
- [pyotp](https://pypi.org/project/pyotp/)
- [qrcode](https://pypi.org/project/qrcode/)
- [pillow](https://pypi.org/project/Pillow/)
- Authenticator App (Google Authenticator/Microsoft Authenticator)

<br>
<hr>

## Project Setup

### Virtual Environment
```python
virtualenv 'env_name'
source 'env_name/bin/activate'
```

### Requirements Installation
```python
pip install -r requirements.txt
```

### Database
```python
python manage.py makemigrations
python manage.py migrate
```
<br>
<hr>

## Project Implementation
```python
python manage.py runserver
```


