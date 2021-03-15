# REST API con FLASK y MySQL | ArchLinux

### Crear entorno virtual

#### Instalar paquete Virtualenv

[Documentacion Virtualenv](https://pypi.org/project/virtualenv/)

`$ python3 -m pip install virtualenv`

#### Crear enterno virtual

`$ python3 -m virtualenv venv`

#### Entrar al entorno Virtual

`$ source venv/bin/activate`

___

### Librerias PIP

`$ pip install flask flask_sqlalchemy flask_jwt_extended flask-marshmallow marshmallow-sqlalchemy pymysql`

### Correr la API

`$ python3 src/app.py`

___

### Posibles errores, solucion:

```zsh
❯ python3 src/app.py
Traceback (most recent call last):
  File "/home/user/rest-api-flask/src/app.py", line 51, in <module>
    db.create_all()
  File "/home/user/rest-api-flask/venv/lib/python3.9/site-packages/flask_sqlalchemy/__init__.py", line 1039, in create_all
    self._execute_for_all_tables(app, bind, 'create_all')
  File "/home/user/rest-api-flask/venv/lib/python3.9/site-packages/flask_sqlalchemy/__init__.py", line 1031, in _execute_for_all_tables
    op(bind=self.get_engine(app, bind), **extra)
  File "/home/user/rest-api-flask/venv/lib/python3.9/site-packages/flask_sqlalchemy/__init__.py", line 962, in get_engine
    return connector.get_engine()
  File "/home/user/rest-api-flask/venv/lib/python3.9/site-packages/flask_sqlalchemy/__init__.py", line 555, in get_engine
    options = self.get_options(sa_url, echo)
  File "/home/user/rest-api-flask/venv/lib/python3.9/site-packages/flask_sqlalchemy/__init__.py", line 570, in get_options
    self._sa.apply_driver_hacks(self._app, sa_url, options)
  File "/home/user/rest-api-flask/venv/lib/python3.9/site-packages/flask_sqlalchemy/__init__.py", line 884, in apply_driver_hacks
    sa_url.query.setdefault('charset', 'utf8')
AttributeError: 'sqlalchemy.cimmutabledict.immutabledict' object has no attribute 'setdefault'
```
##### Solucion:

`$ pip install --upgrade 'SQLAlchemy<1.4'`