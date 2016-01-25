# EVENTEX

Sistema de Eventos encomendado pela Morena.

[![Build Status](https://travis-ci.org/jvrmoreira/eventex-jvictor.svg?branch=master)](https://travis-ci.org/jvrmoreira/eventex-jvictor)
[![Code Climate](https://codeclimate.com/repos/56a2cc42a29fe6008f004b03/badges/4265fb10a822de425057/gpa.svg)](https://codeclimate.com/repos/56a2cc42a29fe6008f004b03/feed)

## Como desenvolver?

1. Clone o repositório.
2. Crie um virtualenv com Python 3.5.
3. Ative o virtualenv.
4. Instale as dependências.
5. Configure a instância com o .env.
6. Execute os testes.

```console
git clone git@github.com:jvrmoreira/eventex-jvictor.git wttd
cd wttd
python -m venv .wttd
source .wttd/bin/activate
pip install -r requirements-dev.txt
cp contrib/env-sample .env
python manage.py test
```

## Como fazer o deploy?

1. Crie uma instância no heroku.
2. Envie as configurações para o heroku.
3. Defina uma SECRET_KEY para a instância.
4. Defina DEBUG = False.
5. Configure o serviço de Email.
6. Envie o código para o heroku.

```console
heroku create MINHA_INSTANCIA
heroku config:push
heroku config:set SECRET_KEY= python contrib/secret_gen.py
heroku config:set DEBUG=False
# configura o email
git push heroku master --force
```