#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')  

#先设定环境变量FLASK_COVERAGE后，脚本重启。再次运行时，脚本顶端的代码发现已经设定了FLASK_COVERAGE，立即启动覆盖检测
import os
from app import create_app, db
from app.models import User, Follow, Role, Permission, Post, Comment
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

#此函数注册了程序、数据库实例、模型，因此这些对象能直接导入shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Follow=Follow, Role=Role,
                Permission=Permission, Post=Post, Comment=Comment)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


#启动单元测试的命令
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
		

if __name__ == '__main__':
    manager.run()
