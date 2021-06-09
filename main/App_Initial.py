'''
author: feifei
date: 2020-12-24
file info: 初始化app
'''
from flask import Flask
from sqlalchemy import PrimaryKeyConstraint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# 将默认的template_folder改成templates路径
app = Flask(__name__,template_folder='../templates')
'''
如果使用不同的协议，或者请求来自于其他的 IP 地址或域名或端口，就需要用到CORS，
这正是 Flask-CORS 扩展帮我们做到的。实际环境中只配置来自前端应用所在的域的请求。
'''
CORS(app)
app.secret_key = 'feifei'

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/nba_base?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# 用对象对app进行配置
app.config.from_object(Config)
# app.config['MAIL_SERVER'] = 'smtp.qq.com'
# app.config['MAIL_PORT'] = 465
db = SQLAlchemy(app)


# 定义系统用户对象类
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer)
    name = db.Column(db.String(16))
    password = db.Column(db.String(32))
    email = db.Column(db.String(32), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_delete = db.Column(db.Boolean,default=False)
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        {},
    )

    def __repr__(self):
        return 'User:<id:%s name:%s email:%s role_id:%s>' % (self.id, self.name, self.email, self.role_id)


# 定义系统用户类型类
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(16), unique=True)

    users = db.relationship('User', backref='role')

    def __repr__(self):
        return 'Role:<id:%s role:%s>' % (self.id, self.role_name)
