from oslo_config import cfg
from oslo_log import log as logging

from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean
from flask_assets import ManageAssets

from jmilkfansblog import create_app
from jmilkfansblog.db.sqlalchemy import models
from jmilkfansblog.extensions import assets_env
from jmilkfansblog.i18n import _LI
from jmilkfansblog.common import config


CONF = cfg.CONF

LOG = logging.getLogger(__name__)

# Create thr app instance via Factory Method
app = create_app(config.__name__ + '.Config')

# Init manager object via app object
manager = Manager(app)

# Init migrate object via app and db object
migrate = Migrate(app, models.db)

# Create the new application manage commands as below
# Start the flask web server
manager.add_command("server", Server(host=CONF.host, port=CONF.server_port))
# Manage database migrate
manager.add_command("db", MigrateCommand)
# Show all mapper of route url
manager.add_command("show-urls", ShowUrls())
# Clean alll the file of .pyc and .pyo
manager.add_command("clean", Clean())
# Pack the static file
manager.add_command('assets', ManageAssets(assets_env))


@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    return dict(app=app,
                db=models.db,
                User=models.User,
                Post=models.Post,
                Comment=models.Comment,
                Tag=models.Tag,
                Role=models.Role,
                BrowseVolume=models.BrowseVolume,
                Reminder=models.Reminder,
                Server=Server)


def main():
    LOG.info(_LI('Running jmilkfansblog manager.'))
    manager.run()
