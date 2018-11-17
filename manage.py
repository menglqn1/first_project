from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from info import create_app, db
from info import models

app = create_app('development')

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)