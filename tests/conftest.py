# coding: utf8
import os

import pytest

from scrapydweb import create_app
from tests.utils import cst, set_env


# MUST be updated: _SCRAPYD_SERVER and _SCRAPYD_SERVER_AUTH
custom_settings = dict(
    _SCRAPYD_SERVER='127.0.0.1:6800',
    _SCRAPYD_SERVER_AUTH=None,  # Or ('yourusername', 'yourpassword')

    SCRAPYD_LOGS_DIR='',  # For LogParser, defaults to the 'logs' directory that resides in current user directory

    ENABLE_EMAIL=False,  # Whether to execute testcases related to "Email Notice"

    SMTP_SERVER='smtp.qq.com',
    SMTP_PORT=465,
    SMTP_OVER_SSL=True,
    SMTP_CONNECTION_TIMEOUT=10,
    FROM_ADDR='username@qq.com',
    EMAIL_PASSWORD='password',
    TO_ADDRS=['username@qq.com'],

    SMTP_SERVER_='smtp.139.com',  # Used in tests/test_a_factory.py/test_check_email_with_ssl_false()
    SMTP_PORT_=25,
    SMTP_OVER_SSL_=False,
    SMTP_CONNECTION_TIMEOUT_=10,
    FROM_ADDR_='username@139.com',
    EMAIL_PASSWORD_='password',
    TO_ADDRS_=['username@139.com']
)


set_env(custom_settings)


@pytest.fixture
def app():
    config = dict(
        TESTING=True,

        DEFAULT_SETTINGS_PY_PATH='',
        SCRAPYDWEB_SETTINGS_PY_PATH='',
        MAIN_PID=os.getpid(),
        LOGPARSER_PID=0,
        POLL_PID=0,

        SCRAPYD_SERVERS=[custom_settings['_SCRAPYD_SERVER'], 'not-exist:6801'],
        SCRAPYD_SERVERS_AUTHS=[custom_settings['_SCRAPYD_SERVER_AUTH'], ('username', 'password')],
        SCRAPYD_SERVERS_GROUPS=['', 'Scrapyd-group'],
        SCRAPY_PROJECTS_DIR=os.path.join(cst.CWD, 'data'),

        ENABLE_LOGPARSER=False,

        EMAIL_WORKING_DAYS=list(range(1, 8)),
        EMAIL_WORKING_HOURS=list(range(24)),
        VERBOSE=True
    )

    config.update(custom_settings)

    app = create_app(config)

    @app.context_processor
    def inject_variable():
        return dict(
            SCRAPYD_SERVERS=app.config.get('SCRAPYD_SERVERS', []) or ['127.0.0.1:6800'],
            SCRAPYD_SERVERS_AMOUNT=len(app.config.get('SCRAPYD_SERVERS', []) or ['127.0.0.1:6800']),
            SCRAPYD_SERVERS_GROUPS=app.config.get('SCRAPYD_SERVERS_GROUPS', []) or [''],
            SCRAPYD_SERVERS_AUTHS=app.config.get('SCRAPYD_SERVERS_AUTHS', []) or [None],

            DAEMONSTATUS_REFRESH_INTERVAL=app.config.get('DAEMONSTATUS_REFRESH_INTERVAL', 10),
            ENABLE_AUTH=app.config.get('ENABLE_AUTH', False),
            SHOW_SCRAPYD_ITEMS=app.config.get('SHOW_SCRAPYD_ITEMS', True),
        )

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
