from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo


# 'class':'form-control',之后可以用css根据类名form-control进行属性修改
# 定义登录表单对象类
class loginform(FlaskForm):
    user = StringField('用户名：', validators=[DataRequired()],
                       render_kw={'placeholder': '请输入用户名', 'class': 'form-control'})
    password = PasswordField('密码：', validators=[DataRequired()],
                             render_kw={'placeholder': '请输入密码', 'class': 'form-control'})
    submit_login = SubmitField('登录')
    submit_register = SubmitField('注册')
    submit_forget = SubmitField('忘记密码')


# render_kw={'class':'form-control'}键值对设置属性
# 定义注册表单对象类
class registerform(FlaskForm):
    user = StringField(validators=[DataRequired()], render_kw={'placeholder': '注册用户名', 'class': 'form-control'})
    password1 = PasswordField(validators=[DataRequired()], render_kw={'placeholder': '注册用户密码', 'class': 'form-control'})
    password2 = PasswordField(validators=[DataRequired(), EqualTo('password1', message='两次密码不一致')],
                              render_kw={'placeholder': '确认密码', 'class': 'form-control'})
    email = StringField(validators=[DataRequired()], render_kw={'placeholder': '注册用户邮箱', 'class': 'form-control'})
    submit = SubmitField('提交')


# 定义注销表单对象类
class withdrawform(FlaskForm):
    user = StringField(validators=[DataRequired()], render_kw={'placeholder': '注销用户名', 'class': 'form-control', })
    password = PasswordField(validators=[DataRequired()], render_kw={'placeholder': '注销用户密码', 'class': 'form-control'})
    submit = SubmitField('提交')
