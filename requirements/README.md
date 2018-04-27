WebMark
======

    MySQL / Python 3 Required

    source workspace/environments/my_env/bin/activate
    sudo apt-get install libmysqlclient-dev
    pip install -r requirements/common.txt
    pip install -r requirements/dev.txt

    /home/username/workspace/environments/my_env/lib/python3.5/site-packages/flask_bootstrap/__init__.py
    update flask-bootstrap-__init__.py -> Upgrade to bootstrap 4

    update /home/username/workspace/environments/my_env/lib/python3.5/site-packages/sqlalchemy/dialects/mysql/base.py
    LINE 1569 update cursor.execute('SELECT @@tx_isolation')
                  -> cursor.execute('SELECT @@transaction_isolation')

    export SECRET_KEY=HELLOWEBMARK-OTC
    export DEV_DATABASE_URL=mysql://root:PASSWORD@localhost:3306/webmark
    export MAIL_SERVER=smtp..com
    export MAIL_PORT=25
    export WEBMARK_MAIL_SENDER=@gmail.com
    export WEBMARK_ADMIN=@gmail.com
    export FLASK_APP=webmark.py
    export FLASK_DEBUG=1

    flask run -h 0.0.0.0 -p 8080

    ----

    Import webmark.sql or:

    flask db init
    flask shell
        db.create_all()
        Role.insert_roles()
        Role.query.all()
    flask db migrate -m 'add benchmarks'
    flask db upgrade

    ----

    REST API
        pip install httpie
        http --auth belem@yourmail.com:password --json GET http://localhost:8080/api/v1/users/1
        http --auth belem@yourmail.com:password --json POST http://localhost:8080/api/v1/tokens/
        http --auth <token>: --json GET http://localhost:8080/api/v1/users/1
        http --auth <token>: --json GET http://localhost:8080/api/v1/comments/
        http --auth <token>: --json GET http://localhost:8080/api/v1/scores/
        http --auth <token>: --json POST http://localhost:8080/api/v1/scores/ < score.json

