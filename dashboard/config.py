import sys
import os
import logging

from configparser import ConfigParser, NoOptionError


LOG_FORMAT = "%(asctime)s: %(levelname)s %(filename)s in %(funcName)s: %(message)s"
DEFAULT_CONFIG_PATH = "/etc/dashboard.cfg"
DEFAULT_CONFIG = """\
[ws]
protocol=http
host=0.0.0.0
port=3031
workers=2
threads=1
logfile=
debug=False

[es]
host=localhost
port=9700
index_name=titles

[ui]
pagination_per_page=15
"""

# Environment variables to file properties mapping
CONFIG_ENV_TO_FILE = dict(
    WS_PROTOCOL=("ws", "protocol"),
    WS_HOST=("ws", "host"),
    WS_PORT=("ws", "port"),
    WS_WORKERS=("ws", "workers"),
    WS_THREADS=("ws", "threads"),
    WS_LOGFILE=("ws", "logfile"),
    WS_DEBUG=("ws", "debug"),
    ES_HOST=("es", "host"),
    ES_PORT=("es", "port"),
    ES_INDEX_NAME=("es", "index_name"),
    UI_PAGINATION_PER_PAGE=("ui", "pagination_per_page"),
)


class Config(ConfigParser):
    def __init__(self, *args, **kwargs):
        ConfigParser.__init__(self, *args, **kwargs)
        self.read_string(DEFAULT_CONFIG)

    def read_string(self, string):
        """
        Read configuration from a string.
        """
        super().read_string(string)


class ConfigError(Exception):
    pass


def configure_logging():
    logging.basicConfig(format=LOG_FORMAT, stream=sys.stdout, level=logging.ERROR)


def override_config_from_env(config):
    for var_env, var_file in CONFIG_ENV_TO_FILE.items():
        if var_env in os.environ:
            config.set(var_file[0], var_file[1], os.environ.get(var_env))
            logging.warning(
                "Config overwrote {0}.{1} with {2}".format(
                    var_file[0], var_file[1], var_env
                )
            )


configure_logging()

conf = Config()

if "DASHBOARD_CONFIG" in os.environ and os.path.isfile(
    os.environ.get("DASHBOARD_CONFIG")
):
    config_path = os.path.abspath(os.environ.get("DASHBOARD_CONFIG"))
    logging.info("Reading the config from " + config_path)
    conf.read(config_path)
elif os.path.exists(DEFAULT_CONFIG_PATH):
    logging.info("Reading the config from " + DEFAULT_CONFIG_PATH)
    conf.read(DEFAULT_CONFIG_PATH)
else:
    logging.warning("Reading the config from default")
override_config_from_env(conf)


def get(section, key, **kwars):
    try:
        return conf.get(section, key)
    except NoOptionError as e:
        raise ConfigError(e)


def getboolean(section, key, **kwargs):
    return conf.getboolean(section, key, **kwargs)


def getint(section, key, **kwargs):
    return conf.getint(section, key, **kwargs)


def getfloat(section, key, **kwargs):
    return conf.getfloat(section, key, **kwargs)


def set(section, key, value):
    return conf.set(section, key, value=value)
