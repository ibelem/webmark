from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from . import db, login_manager


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            # User 1 7
            # 'Moderator': [Permission.FOLLOW, Permission.COMMENT,
            #               Permission.WRITE, Permission.MODERATE],
            # Moderator 0 15
            # Administrator 0 31
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    # avatar_hash = db.Column(db.String(32))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    webmark = db.relationship('Webmark', backref='author', lazy='dynamic')
    star = db.relationship('Star', backref='author', lazy='dynamic')
    news = db.relationship('News', backref='author', lazy='dynamic')
    score = db.relationship('Score', backref='author', lazy='dynamic')
    subscription = db.relationship('Subscription', backref='author', lazy='dynamic')



    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['WEBMARK_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        # if self.email is not None and self.avatar_hash is None:
        #     self.avatar_hash = self.gravatar_hash()
        self.follow(self)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        # self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    # def gravatar_hash(self):
    #     return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
    #
    # def gravatar(self, size=100, default='identicon', rating='g'):
    #     url = 'https://secure.gravatar.com/avatar'
    #     hash = self.avatar_hash or self.gravatar_hash()
    #     return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
    #         url=url, hash=hash, size=size, default=default, rating=rating)

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        if user.id is None:
            return False
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id == Post.author_id)\
            .filter(Follow.follower_id == self.id)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts_url': url_for('api.get_user_posts', id=self.id),
            'followed_posts_url': url_for('api.get_user_followed_posts',
                                          id=self.id),
            'post_count': self.posts.count()
        }
        return json_user

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class WebmarkProposal(db.Model):
    __tablename__ = 'webmarkproposal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    email = db.Column(db.String(64))
    url = db.Column(db.String(1024))
    details = db.Column(db.Text)
    reviewed = db.Column(db.Boolean)
    added = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    title = db.Column(db.String(256))
    details = db.Column(db.Text)
    reviewed = db.Column(db.Boolean)
    replied = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class TagWebMark(db.Model):
    __tablename__ = 'tag_webmark'
    id = db.Column(db.Integer, primary_key=True)
    webmark_id = db.Column(db.Integer, db.ForeignKey('webmark.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    tag_webmark = db.relationship('TagWebMark', backref='Tag', lazy='dynamic')

    def __unicode__(self):
        return self.name


class CPU(db.Model):
    __tablename__ = 'e_cpu'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(128))
    architecture = db.Column(db.String(32))
    hardware_concurrency = db.Column(db.String(8))


class GPU(db.Model):
    __tablename__ = 'e_gpu'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(128))
    vender = db.Column(db.String(128))


class Browser(db.Model):
    __tablename__ = 'e_browser'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(64))
    version = db.Column(db.String(64))
    major = db.Column(db.String(16))
    language = db.Column(db.String(8))
    engine_name = db.Column(db.String(16))
    engine_version = db.Column(db.String(16))
    ua = db.Column(db.String(256))
    channel = db.Column(db.String(12))


class Software(db.Model):
    __tablename__ = 'e_software'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    os = db.Column(db.String(32))
    os_version = db.Column(db.String(32))
    platform = db.Column(db.String(32))
    timezone = db.Column(db.String(8))


class Hardware(db.Model):
    __tablename__ = 'e_hardware'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    device_vendor = db.Column(db.String(64))
    device_model = db.Column(db.String(32))
    device_type = db.Column(db.String(32))
    device_memory = db.Column(db.String(8))
    screen_width = db.Column(db.Integer)
    screen_height = db.Column(db.Integer)
    # screen_available_width = db.Column(db.Integer)
    # screen_available_height = db.Column(db.Integer)
    # screen_colordepth = db.Column(db.Integer)
    # screen_pixeldepth = db.Column(db.Integer)
    # device_pixelratio = db.Column(db.Integer)
    # cpu = db.relationship('CPU', backref='e_hardware', lazy='dynamic')
    # gpu = db.relationship('GPU', backref='e_hardware', lazy='dynamic')


class Environment(db.Model):
    __tablename__ = 'e_environment'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    cpu_id = db.Column(db.Integer, db.ForeignKey('e_cpu.id'))
    gpu_id = db.Column(db.Integer, db.ForeignKey('e_gpu.id'))
    hardware_id = db.Column(db.Integer, db.ForeignKey('e_hardware.id'))
    software_id = db.Column(db.Integer, db.ForeignKey('e_software.id'))
    browser_id = db.Column(db.Integer, db.ForeignKey('e_browser.id'))
    # finger_print = db.Column(db.String(128))
    # hardware = db.relationship('Hardware', backref='e_environment', lazy='dynamic')
    # software = db.relationship('Software', backref='e_environment', lazy='dynamic')
    # browser = db.relationship('Browser', backref='e_environment', lazy='dynamic')

    def to_json(self):
        json_environment = {
            'url': url_for('api.get_environment', id=self.id),
            'hardware_id': self.hardware_id,
            'browser_id': self.browser_id,
            'software_id': self.software_id,
            'cpu_id': self.cpu_id,
            'gpu_id': self.gpu_id,
            # 'finger_print': self.finger_print,
            'timestamp': self.timestamp,
            'author_url': url_for('api.get_user', id=self.author_id)
        }
        return json_environment

    @staticmethod
    def from_json(json_environment):
        hardware_id=json_environment.get('hardware_id')
        software_id=json_environment.get('software_id')
        browser_id=json_environment.get('browser_id')
        cpu_id = json_environment.get('cpu_id')
        gpu_id = json_environment.get('gpu_id')
        # finger_print=json_environment.get('finger_print')
        # return Environment(hardware_id=hardware_id,
        #                    software_id=software_id,
        #                    browser_id=browser_id,
        #                    software_id=software_id,
        #                    finger_print=finger_print)
        return Environment(hardware_id=hardware_id,
                           software_id=software_id,
                           browser_id=browser_id,
                           cpu_id=cpu_id,
                           gpu_id=gpu_id)

class Scores(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    webmark_id = db.Column(db.Integer, db.ForeignKey('webmark.id'))
    score = db.Column(db.String(64))

    device_vendor = db.Column(db.String(64))
    device_model = db.Column(db.String(32))
    device_type = db.Column(db.String(32))
    device_memory = db.Column(db.String(8))
    screen_width = db.Column(db.Integer)
    screen_height = db.Column(db.Integer)

    cpu_name = db.Column(db.String(128))
    cpu_architecture = db.Column(db.String(32))
    cpu_hardware_concurrency = db.Column(db.String(8))

    gpu_name = db.Column(db.String(128))
    gpu_vender = db.Column(db.String(128))

    os = db.Column(db.String(32))
    os_version = db.Column(db.String(32))
    platform = db.Column(db.String(32))
    timezone = db.Column(db.String(8))

    browser_name = db.Column(db.String(64))
    browser_version = db.Column(db.String(64))
    browser_major = db.Column(db.String(16))
    browser_language = db.Column(db.String(8))
    browser_engine_name = db.Column(db.String(16))
    browser_engine_version = db.Column(db.String(16))
    browser_ua = db.Column(db.String(256))
    browser_channel = db.Column(db.String(12))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_json(self):
        json_score = {
            'url': url_for('api.get_score', id=self.id),
            'score': self.score,
            'webmark_id': self.webmark_id,
            'author_id': self.author_id,
            'timestamp': self.timestamp,
            'author_url': url_for('api.get_user', id=self.author_id)
        }
        return json_score

    # def to_json(self):
    #     json_score = {
    #         'url': url_for('api.get_score', id=self.id),
    #         'score': self.score,
    #         'webmark_id': self.webmark_id,
    #         'environment_id': self.environment_id,
    #         'device_vendor': self.device_vendor,
    #         'device_model': self.device_model,
    #         'device_type': self.device_type,
    #         'device_memory': self.device_memory,
    #         'screen_width': self.screen_width,
    #         'screen_height': self.screen_height,
    #         'cpu_name': self.cpu_name,
    #         'cpu_architecture': self.cpu_architecture,
    #         'cpu_hardware_concurrency': self.cpu_hardware_concurrency,
    #         'gpu_name': self.gpu_name,
    #         'gpu_vender': self.gpu_vender,
    #         'os': self.os,
    #         'os_version': self.os_version,
    #         'platform': self.platform,
    #         'timezone': self.timezone,
    #         'browser_name': self.browser_name,
    #         'browser_version': self.browser_version,
    #         'browser_major': self.browser_major,
    #         'browser_language': self.browser_language,
    #         'browser_engine_name': self.browser_engine_name,
    #         'browser_engine_version': self.browser_engine_version,
    #         'browser_ua': self.browser_ua,
    #         'browser_channel': self.browser_channel,
    #         'author_id': self.author_id,
    #         'timestamp': self.timestamp,
    #         'author_url': url_for('api.get_user', id=self.author_id)
    #     }
    #     return json_score

    @staticmethod
    def from_json(json_score):
        score = json_score.get('score')
        webmark_id=json_score.get('webmark_id')
        device_type = json_score.get('hardware_device_type')
        device_memory = json_score.get('hardware_device_memory')
        device_vendor = json_score.get('hardware_device_vendor')
        device_model = json_score.get('hardware_device_model')
        screen_width = json_score.get('hardware_screen_width')
        screen_height = json_score.get('hardware_screen_height')
        cpu_name = json_score.get('cpu_name')
        cpu_architecture = json_score.get('cpu_architecture')
        cpu_hardware_concurrency = json_score.get('cpu_hardware_concurrency')
        gpu_name = json_score.get('gpu_name')
        gpu_vender = json_score.get('gpu_vender')
        os = json_score.get('software_os')
        os_version = json_score.get('software_os_version')
        platform = json_score.get('software_platform')
        timezone = json_score.get('software_timezone')
        browser_name = json_score.get('browser_name')
        browser_version = json_score.get('browser_version')
        browser_major = json_score.get('browser_major')
        browser_language = json_score.get('browser_language')
        browser_engine_name = json_score.get('browser_engine_name')
        browser_engine_version = json_score.get('browser_engine_version')
        browser_ua = json_score.get('browser_ua')
        browser_channel = json_score.get('browser_channel')
        author_id=json_score.get('author_id')
        # if score is None or score == '':
        #     raise ValidationError('score does not have a score')
        return Scores(score=score,
                     webmark_id=webmark_id,
                     device_type=device_type,
                     device_memory=device_memory,
                     device_model=device_model,
                     device_vendor=device_vendor,
                     screen_width=screen_width,
                     screen_height=screen_height,
                     cpu_name=cpu_name,
                     cpu_architecture=cpu_architecture,
                     cpu_hardware_concurrency=cpu_hardware_concurrency,
                     gpu_name=gpu_name,
                     gpu_vender=gpu_vender,
                     os=os,
                     os_version=os_version,
                     platform=platform,
                     timezone=timezone,
                     browser_name=browser_name,
                     browser_version=browser_version,
                     browser_major=browser_major,
                     browser_language=browser_language,
                     browser_engine_name=browser_engine_name,
                     browser_engine_version=browser_engine_version,
                     browser_ua=browser_ua,
                     browser_channel=browser_channel,
                     author_id=author_id)


class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True)
    webmark_id = db.Column(db.Integer, db.ForeignKey('webmark.id'))
    score = db.Column(db.String(64))
    environment_id = db.Column(db.Integer, db.ForeignKey('e_environment.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # environment = db.relationship('Environment', backref='Score', lazy='dynamic')

    def to_json(self):
        json_score = {
            'url': url_for('api.get_score', id=self.id),
            'score': self.score,
            'webmark_id': self.webmark_id,
            'environment_id': self.environment_id,
            'author_id': self.author_id,
            'timestamp': self.timestamp,
            'author_url': url_for('api.get_user', id=self.author_id)
        }
        return json_score

    @staticmethod
    def from_json(json_score):
        score = json_score.get('score')
        webmark_id=json_score.get('webmark_id')
        environment_id=json_score.get('environment_id')
        author_id=json_score.get('author_id')
        if score is None or score == '':
            raise ValidationError('score does not have a score')
        return Score(score=score,
                     webmark_id=webmark_id,
                     environment_id=environment_id,
                     author_id=author_id)

class Webmark(db.Model):
    __tablename__ = 'webmark'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    ready = db.Column(db.Boolean)
    duration = db.Column(db.String(32))
    config = db.Column(db.String(128))
    test_path = db.Column(db.String(128))
    score_measurement_unit = db.Column(db.String(16))
    metrics = db.Column(db.String(64))
    version = db.Column(db.String(32))
    license = db.Column(db.String(32))
    developed_by = db.Column(db.String(64))
    screenshot_path = db.Column(db.String(256))
    url = db.Column(db.String(1024))
    repo_url = db.Column(db.String(1024))
    summary = db.Column(db.String(256))
    details = db.Column(db.Text)
    pros = db.Column(db.Text)
    cons = db.Column(db.Text)
    rating_avg = db.Column(db.String(16))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments_count = db.Column(db.Integer)
    news_count = db.Column(db.Integer)
    click_count = db.Column(db.Integer)
    comments = db.relationship('Comment', backref='webmark', lazy='dynamic')
    star = db.relationship('Star', backref='webmark', lazy='dynamic')
    tag_webmark = db.relationship('TagWebMark', backref='webmark', lazy='dynamic')
    news = db.relationship('News', backref='webmark', lazy='dynamic')
    score = db.relationship('Scores', backref='webmark', lazy='dynamic')

    def __unicode__(self):
        return self.name


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author_url': url_for('api.get_user', id=self.author_id)
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Post(body=body)


db.event.listen(Post.body, 'set', Post.on_changed_body)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    webmark_id = db.Column(db.Integer, db.ForeignKey('webmark.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author_url': url_for('api.get_user', id=self.author_id),
        }
        return json_comment

    @staticmethod
    def from_json(json_comment):
        body = json_comment.get('body')
        if body is None or body == '':
            raise ValidationError('comment does not have a body')
        return Comment(body=body)


db.event.listen(Comment.body, 'set', Comment.on_changed_body)

class Star(db.Model):
    __tablename__ = 'star'
    id = db.Column(db.Integer, primary_key=True)
    star = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    webmark_id = db.Column(db.Integer, db.ForeignKey('webmark.id'))

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.String(256))
    url = db.Column(db.String(1024))
    source = db.Column(db.String(128))
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    webmark_id = db.Column(db.Integer, db.ForeignKey('webmark.id'))


class Subscription(db.Model):
    __tablename__ = 'subscription'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    webmark_id = db.Column(db.Integer, db.ForeignKey('webmark.id'))
    global_subscribe = db.Column(db.Boolean)
