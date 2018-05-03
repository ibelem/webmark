import os, re
from functools import reduce
from flask import render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from sqlalchemy import *
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, \
    CommentForm, WebMarkForm, EditWebMarkForm, WebMarkProposalForm, \
    NewsForm, FeedbackForm
from .. import db
from ..models import Permission, Role, User, Post, Comment, Webmark, \
    Tag, TagWebMark, WebmarkProposal, Star, News, Subscription, \
    Scores, Feedback
from ..decorators import admin_required, permission_required
from werkzeug.utils import secure_filename
from ..email import send_email
from ..api import authentication
import json


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['WEBMARK_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/privacy', methods=['GET'])
def privacy():
    return render_template('other/privacy.html')

@main.route('/tou', methods=['GET'])
def tou():
    return render_template('other/tou.html')

@main.route('/about', methods=['GET'])
def about():
    return render_template('other/about.html')

# @main.route('/', methods=['GET', 'POST'])
# def index():
#     form = PostForm()
#     if current_user.can(Permission.WRITE) and form.validate_on_submit():
#         post = Post(body=form.body.data,
#                     author=current_user._get_current_object())
#         db.session.add(post)
#         db.session.commit()
#         return redirect(url_for('.index'))
#     page = request.args.get('page', 1, type=int)
#     show_followed = False
#     if current_user.is_authenticated:
#         show_followed = bool(request.cookies.get('show_followed', ''))
#     if show_followed:
#         query = current_user.followed_posts
#     else:
#         query = Post.query
#     pagination = query.order_by(Post.timestamp.desc()).paginate(
#         page, per_page=current_app.config['WEBMARK_POSTS_PER_PAGE'],
#         error_out=False)
#     posts = pagination.items
#     return render_template('index.html', form=form, posts=posts,
#                            show_followed=show_followed, pagination=pagination)

@main.route('/subscribe/', methods=['POST'])
@login_required
def subscribe():
    subscription = Subscription.query.filter_by(user_id=current_user.id).first()
    if subscription and subscription.global_subscribe == True:
        db.session.query(Subscription).filter(Subscription.user_id == current_user.id).delete()
        db.session.commit()
        flash('You have unsubscribed news and comments for WebMark.')
    else:
        sub = Subscription(user_id=current_user.id, global_subscribe=True)
        db.session.add(sub)
        db.session.commit()
        flash('You have subscribed news and comments for WebMark successfully. You will receive email for updates and new comments.')
    return redirect(url_for('main.webmarks'))


@main.route('/user/<username>')
@login_required
def user(username):
    # user = User.query.filter_by(username=username).first_or_404()
    # page = request.args.get('page', 1, type=int)
    # pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
    #     page, per_page=current_app.config['WEBMARK_POSTS_PER_PAGE'],
    #     error_out=False)
    # posts = pagination.items
    # return render_template('user.html', user=user, posts=posts,
    #                        pagination=pagination)

    user = User.query.filter_by(username=username).first_or_404()
    # comments = Comment.query.filter_by(author_id=user.id).order_by(Comment.timestamp.desc()).all()

    results = db.session.query(Comment, Webmark, User). \
        filter(User.username == username). \
        filter(Comment.author_id == User.id).\
        filter(Comment.webmark_id == Webmark.id). \
        order_by(Comment.timestamp.desc()).all()

    ratings = Star.query.filter_by(author_id=current_user.id).all()
    return render_template('user.html', user=user, results=results, ratings=ratings)


@main.route('/user-edit/', methods=['POST'])
@login_required
@admin_required
def user_edit():
    if request.method == 'POST':
        dict = request.form.to_dict()
        for i in dict:
            id = str(i).replace('r', '').replace('c', '')

            if i.find('c') > -1:
                if dict[i] == 'True':
                    db.session.query(User).filter(User.id == int(id)).update(
                        {User.confirmed: True})
                else:
                    db.session.query(User).filter(User.id == int(id)).update(
                        {User.confirmed: False})
                db.session.commit()
            elif i.find('r') > -1:
                if int(dict[i]) == 3:
                    db.session.query(User).filter(User.id == int(id)).update(
                        {User.role_id: 3})
                else:
                    db.session.query(User).filter(User.id == int(id)).update(
                        {User.role_id: 1})
                db.session.commit()
    return redirect(url_for('main.user_management'))


@main.route('/user/management')
@login_required
@admin_required
def user_management():
    # user = User.query.filter_by(username=username).first_or_404()
    # page = request.args.get('page', 1, type=int)
    # pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
    #     page, per_page=current_app.config['WEBMARK_POSTS_PER_PAGE'],
    #     error_out=False)
    # posts = pagination.items
    # return render_template('user.html', user=user, posts=posts,
    #                        pagination=pagination)

    user = User.query.with_entities(User.id, User.username, User.email, User.confirmed, User.role_id)
    page = request.args.get('page', 1, type=int)
    pagination = user.order_by(User.id.desc()).paginate(
             page, per_page=50,
             error_out=False)
    users = pagination.items
    return render_template('admin/user_management.html', user=user, pagination=pagination)


@main.route('/search/', methods=['GET'])
def search():
    subscription = None
    if current_user.is_authenticated:
        subscription = Subscription.query.filter_by(user_id=current_user.id).first()
    tags = Tag.query.order_by(Tag.name).all()
    form = WebMarkProposalForm()
    if form.validate_on_submit():
        webmark_proposal = WebmarkProposal(name=form.name.data,
                                           email=form.email.data,
                                           url=form.url.data,
                                           details=form.details.data)
        db.session.add(webmark_proposal)
        db.session.commit()
        flash('The new webmark ' + form.name.data + ' has been proposed, we will evaluate it asap.')
        return redirect(url_for('main.webmarks'))
    else:
        if form.errors:
            flash(form.errors)
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        form.email.data = user.email

    if request.method == 'GET':
        if request.args['q']:
            q_list = re.split(r'[;,\s]\s*', request.args['q'])
            q_list = remove_duplicated_list(q_list)
            print(q_list)
            webmarks = db.session.query(Webmark).filter(or_(Webmark.name.like("%"+name+"%") for name in q_list)).all()
            return render_template('search.html', subscription=subscription, webmarks=webmarks, tags=tags, form=form, qlist=q_list)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        print(user.role)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/view-trend/', methods=['GET', 'POST'])
def view_trend():
    webmarks = Webmark.query.with_entities(Webmark.id, Webmark.name, Webmark.ready,
                                           Webmark.score_measurement_unit).filter_by(ready=True)
    os = db.session.query(Scores.os, Scores.os_version).distinct().all()
    words = ['%8700%', '%1800%']
    rule = or_(*[Scores.cpu_name.like(w) for w in words])
    cpus = Scores.query.with_entities(Scores.cpu_name).filter(Scores.cpu_name != '').filter(rule).distinct()
    gpus = Scores.query.with_entities(Scores.gpu_name).filter(Scores.gpu_name != '').distinct().all()

    querylist = {}
    if request.method == 'GET':
        c = request.args.get('cpu')
        g = request.args.get('gpu')
        if g:
            g = g.replace('HD', '').replace('GTX', '').replace(' ', '')
        o = request.args.get('o')
        wm = request.args.get('wm')
        querylist = {'c': c, 'g': g, 'o': o, 'wm': wm}
        if c and g and o and wm:

            print(querylist)

            we = Webmark.query.with_entities(Webmark.id).filter_by(name=wm).first()
            print(we)
            scores = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.os == o.split(" ")[0]). \
                filter(Scores.os_version == o.split(" ")[1]). \
                filter(Scores.cpu_name.like('%'+c+'%')). \
                filter(Scores.gpu_name.like('%'+g+'%')). \
                filter(Scores.webmark_id == we.id). \
                order_by(cast(Scores.browser_version, Integer)).all()
            print(scores)

            l_chrome = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.os == o.split(" ")[0]). \
                filter(Scores.os_version == o.split(" ")[1]). \
                filter(Scores.cpu_name.like('%'+c+'%')). \
                filter(Scores.gpu_name.like('%'+g+'%')). \
                filter(Scores.webmark_id == we.id). \
                filter(Scores.browser_name == 'Chrome'). \
                order_by(cast(Scores.browser_version, Integer)).all()

            l_firefox = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.os == o.split(" ")[0]). \
                filter(Scores.os_version == o.split(" ")[1]). \
                filter(Scores.cpu_name.like('%'+c+'%')). \
                filter(Scores.gpu_name.like('%'+g+'%')). \
                filter(Scores.webmark_id == we.id). \
                filter(Scores.browser_name == 'Firefox'). \
                order_by(cast(Scores.browser_version, Integer)).all()

            l_edge = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.os == o.split(" ")[0]). \
                filter(Scores.os_version == o.split(" ")[1]). \
                filter(Scores.cpu_name.like('%'+c+'%')). \
                filter(Scores.gpu_name.like('%'+g+'%')). \
                filter(Scores.webmark_id == we.id). \
                filter(Scores.browser_name == 'Edge'). \
                order_by(cast(Scores.browser_version, Integer)).all()

            max_length = max(len(l_chrome), len(l_firefox), len(l_edge))
            chartArray = [n for n in range(1, max_length + 1)]

            chrome_score = [i.score for i, j in l_chrome]
            chrome_score = list(map(eval, chrome_score))
            edge_score = [i.score for i, j in l_edge]
            edge_score = list(map(eval, edge_score))
            firefox_score = [i.score for i, j in l_firefox]
            firefox_score = list(map(eval, firefox_score))

            if len(l_chrome) == max_length:
                edge_score += [None for i in range(len(l_chrome) - len(l_edge))]
                firefox_score += [None for i in range(len(l_chrome) - len(l_firefox))]
            elif len(l_edge) == max_length:
                chrome_score += [None for i in range(len(l_edge) - len(l_chrome))]
                firefox_score += [None for i in range(len(l_edge) - len(l_firefox))]
            elif len(l_firefox) == max_length:
                edge_score += [None for i in range(len(l_firefox) - len(l_edge))]
                chrome_score += [None for i in range(len(l_firefox) - len(l_chrome))]

            # list_3d = [chrome_score, firefox_score, edge_score]
            # list_3d = list(zip(*list_3d))
            # print(list_3d)

            chrome_score = json.dumps(chrome_score[::-1])
            firefox_score = json.dumps(firefox_score[::-1])
            edge_score = json.dumps(edge_score[::-1])

            print(chrome_score, firefox_score, edge_score)

            return render_template('trend.html', webmarks=webmarks, cpus=cpus, gpus=gpus, os=os,
                                   scores=scores, querylist=querylist, chartArray=chartArray, chrome_score=chrome_score,
                                   firefox_score=firefox_score, edge_score=edge_score, uid=current_user.get_id())

        else:
            querylist = {'c': cpus[0].cpu_name, 'g': gpus[0].gpu_name, 'o': os[0].os + ' ' + os[0].os_version,
                         'wm': webmarks[0].name}
            scores = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.os == os[0].os). \
                filter(Scores.os_version == os[0].os_version). \
                filter(Scores.cpu_name == cpus[0].cpu_name). \
                filter(Scores.gpu_name.like('%630%')). \
                filter(Webmark.name == webmarks[0].name). \
                order_by(cast(Scores.browser_version, Integer)).all()

            l_chrome = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.os == os[0].os). \
                filter(Scores.os_version == os[0].os_version). \
                filter(Scores.cpu_name == cpus[0].cpu_name). \
                filter(Scores.gpu_name.like('%630%')). \
                filter(Webmark.name == webmarks[0].name). \
                filter(Scores.browser_name == 'Chrome'). \
                order_by(cast(Scores.browser_version, Integer)).all()

            l_firefox = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.os == os[0].os). \
                filter(Scores.os_version == os[0].os_version). \
                filter(Scores.cpu_name == cpus[0].cpu_name). \
                filter(Scores.gpu_name.like('%630%')). \
                filter(Webmark.name == webmarks[0].name). \
                filter(Scores.browser_name == 'Firefox'). \
                order_by(cast(Scores.browser_version, Integer)).all()

            l_edge = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.os == os[0].os). \
                filter(Scores.os_version == os[0].os_version). \
                filter(Scores.cpu_name == cpus[0].cpu_name). \
                filter(Scores.gpu_name.like('%630%')). \
                filter(Webmark.name == webmarks[0].name). \
                filter(Scores.browser_name == 'Edge'). \
                order_by(cast(Scores.browser_version, Integer)).all()

            max_length = max(len(l_chrome), len(l_firefox), len(l_edge))
            chartArray = [n for n in range(1, max_length + 1)]

            chrome_score = [i.score for i, j in l_chrome]
            chrome_score = list(map(eval, chrome_score))
            edge_score = [i.score for i, j in l_edge]
            edge_score = list(map(eval, edge_score))
            firefox_score = [i.score for i, j in l_firefox]
            firefox_score = list(map(eval, firefox_score))

            if len(l_chrome) == max_length:
                edge_score += [None for i in range(len(l_chrome) - len(l_edge))]
                firefox_score += [None for i in range(len(l_chrome) - len(l_firefox))]
            elif len(l_edge) == max_length:
                chrome_score += [None for i in range(len(l_edge) - len(l_chrome))]
                firefox_score += [None for i in range(len(l_edge) - len(l_firefox))]
            elif len(l_firefox) == max_length:
                edge_score += [None for i in range(len(l_firefox) - len(l_edge))]
                chrome_score += [None for i in range(len(l_firefox) - len(l_chrome))]

            # list_3d = [chrome_score, firefox_score, edge_score]
            # list_3d = list(zip(*list_3d))
            # print(list_3d)

            chrome_score = json.dumps(chrome_score[::-1])
            firefox_score = json.dumps(firefox_score[::-1])
            edge_score = json.dumps(edge_score[::-1])

            return render_template('trend.html', webmarks=webmarks, cpus=cpus, gpus=gpus, os=os,
                                   scores=scores, querylist=querylist, chartArray=chartArray, chrome_score=chrome_score,
                                   firefox_score=firefox_score, edge_score=edge_score, uid=current_user.get_id())
    return redirect(url_for('main.index'))

@main.route('/view-browser/', methods=['GET', 'POST'])
def view_browser():
    webmarks = Webmark.query.with_entities(Webmark.id, Webmark.name, Webmark.ready, Webmark.score_measurement_unit).filter_by(ready=True)
    os = db.session.query(Scores.os, Scores.os_version).distinct().all()
    browsers = db.session.query(Scores.browser_name).order_by(Scores.browser_name).distinct().all()
    update = Scores.query.with_entities(Scores.timestamp).order_by(Scores.timestamp.desc()).first()

    querylist = {}
    if request.method == 'GET':
        o = request.args.get('o')
        b = request.args.get('b')
        wm = request.args.get('wm')
        querylist = {'o': o, 'b': b, 'wm': wm}
        if o and b and wm:
            we = Webmark.query.with_entities(Webmark.id).filter_by(name=wm).first()
            scores = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.os == o.split(" ")[0]). \
                filter(Scores.os_version == o.split(" ")[1]). \
                filter(Scores.browser_name == b). \
                filter(Scores.webmark_id == we.id). \
                filter(Scores.score.isnot(None)). \
                filter(Scores.score != ''). \
                order_by(cast(Scores.score, Integer)).all()
            return render_template('browser.html', webmarks=webmarks, os=os, browsers=browsers, update=update,
                                   scores=scores, querylist=querylist, uid=current_user.get_id())
        else:
            querylist = {'o': os[0].os + ' ' + os[0].os_version, 'b': browsers[0].browser_name, 'wm': webmarks[0].name}
            scores = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.os == os[0].os). \
                filter(Scores.os_version == os[0].os_version). \
                filter(Scores.browser_name == browsers[0].browser_name). \
                filter(Webmark.name == webmarks[0].name). \
                filter(Scores.score.isnot(None)). \
                filter(Scores.score != ''). \
                order_by(cast(Scores.score, Integer)).all()
            return render_template('browser.html', webmarks=webmarks, os=os, browsers=browsers, update=update,
                                   scores=scores,
                                   querylist=querylist, uid=current_user.get_id())

    if request.method == 'POST':
        o = request.form.get('o')
        b = request.form.get('b')
        wm = request.form.get('wm')
        querylist = {'o': o, 'b': b, 'wm': wm}
        we = Webmark.query.with_entities(Webmark.id).filter_by(name=wm).first()
        if o and b and wm:
            scores = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.os == o.split(" ")[0]). \
                filter(Scores.os_version == o.split(" ")[1]). \
                filter(Scores.browser_name == b). \
                filter(Scores.webmark_id == we.id). \
                filter(Scores.score.isnot(None)). \
                filter(Scores.score != ''). \
                order_by(cast(Scores.score, Integer)).all()
        elif o and b:
            scores = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.os == o.split(" ")[0]). \
                filter(Scores.os_version == o.split(" ")[1]). \
                filter(Scores.browser_name == b). \
                filter(Scores.score.isnot(None)). \
                filter(Scores.score != ''). \
                order_by(cast(Scores.score, Integer)).all()
        elif o and wm:
            scores = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.os == o.split(" ")[0]). \
                filter(Scores.os_version == o.split(" ")[1]). \
                filter(Scores.webmark_id == we.id). \
                filter(Scores.score.isnot(None)). \
                filter(Scores.score != ''). \
                order_by(cast(Scores.score, Integer)).all()
        elif b and wm:
            scores = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.browser_name == b). \
                filter(Scores.webmark_id == we.id). \
                filter(Scores.score.isnot(None)). \
                filter(Scores.score != ''). \
                order_by(cast(Scores.score, Integer)).all()
        elif o:
            scores = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.os == o.split(" ")[0]). \
                filter(Scores.os_version == o.split(" ")[1]). \
                filter(Scores.score.isnot(None)). \
                filter(Scores.score != ''). \
                order_by(cast(Scores.score, Integer)).all()
        elif b:
            scores = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.browser_name == b). \
                filter(Scores.score.isnot(None)). \
                filter(Scores.score != ''). \
                order_by(cast(Scores.score, Integer)).all()
        elif wm:
            scores = db.session.query(Scores, Webmark). \
                filter(Scores.webmark_id == Webmark.id). \
                filter(Scores.webmark_id == we.id). \
                filter(Scores.score.isnot(None)). \
                filter(Scores.score != ''). \
                order_by(cast(Scores.score, Integer)).all()
        return render_template('browser.html', webmarks=webmarks, os=os, browsers=browsers, update=update,
                               scores=scores, querylist=querylist, uid=current_user.get_id())

@main.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(email=form.email.data,
                                           title=form.title.data,
                                           details=form.details.data)
        db.session.add(feedback)
        db.session.commit()
        flash('Your feedback ' + form.title.data + ' has been submitted.')

        if request.args.get('refer'):
            print(request.args.get('refer'))
            return redirect(request.args.get('refer'))
        else:
            return redirect(url_for('main.index'))
    else:
        if form.errors:
            flash(form.errors)
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        form.email.data = user.email
    return render_template('other/feedback.html', form=form)


@main.route('/review-feedback/', methods=['GET', 'POST'])
@login_required
@admin_required
def review_feedback():
    feedback = Feedback.query.all()
    return render_template('other/review_feedback.html', feedback=feedback)

@main.route('/edit-feedback/', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_feedback():
    if request.method == 'POST':
        dict = request.form.to_dict()
        for i in dict:
            id = str(i).replace('r', '').replace('a', '').replace('d', '')

            if i.find('d') > -1:
                db.session.query(Feedback).filter(Feedback.id == int(id)).delete()
                db.session.commit()
            elif i.find('r') > -1:
                if dict[i] == 'Yes':
                    db.session.query(Feedback).filter(Feedback.id == int(id)).update(
                        {Feedback.reviewed: True})
                else:
                    db.session.query(Feedback).filter(Feedback.id == int(id)).update(
                        {Feedback.reviewed: False})
                db.session.commit()
            elif i.find('a') > -1:
                if dict[i] == 'Yes':
                    db.session.query(Feedback).filter(Feedback.id == int(id)).update(
                        {Feedback.replied: True})
                else:
                    db.session.query(Feedback).filter(Feedback.id == int(id)).update(
                        {Feedback.replied: False})
                db.session.commit()
    return redirect(url_for('main.review_feedback'))

@main.route('/webmark-proposal', methods=['GET', 'POST'])
def webmark_proposal():
    form = WebMarkProposalForm()
    if form.validate_on_submit():
        webmark_proposal = WebmarkProposal(name=form.name.data,
                                           email=form.email.data,
                                           url=form.url.data,
                                           details=form.details.data)
        db.session.add(webmark_proposal)
        db.session.commit()
        flash('The new webmark ' + form.name.data + ' has been proposed, we will evaluate it asap.')
        return redirect(url_for('main.webmarks'))
    else:
        if form.errors:
            flash(form.errors)
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        form.email.data = user.email
    return render_template('webmark_proposal.html', form=form)


@main.route('/edit-webmark-proposal/', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_webmark_proposal():
    if request.method == 'POST':
        dict = request.form.to_dict()
        for i in dict:
            id = str(i).replace('r', '').replace('a', '').replace('d', '')

            if i.find('d') > -1:
                db.session.query(WebmarkProposal).filter(WebmarkProposal.id == int(id)).delete()
                db.session.commit()
            elif i.find('r') > -1:
                if dict[i] == 'Yes':
                    db.session.query(WebmarkProposal).filter(WebmarkProposal.id == int(id)).update(
                        {WebmarkProposal.reviewed: True})
                else:
                    db.session.query(WebmarkProposal).filter(WebmarkProposal.id == int(id)).update(
                        {WebmarkProposal.reviewed: False})
                db.session.commit()
            elif i.find('a') > -1:
                if dict[i] == 'Yes':
                    db.session.query(WebmarkProposal).filter(WebmarkProposal.id == int(id)).update(
                        {WebmarkProposal.added: True})
                else:
                    db.session.query(WebmarkProposal).filter(WebmarkProposal.id == int(id)).update(
                        {WebmarkProposal.added: False})
                db.session.commit()
    return redirect(url_for('main.review_webmark_proposal'))


@main.route('/review-webmark-proposal/', methods=['GET', 'POST'])
@login_required
@admin_required
def review_webmark_proposal():
    webmark_proposal = WebmarkProposal.query.all()
    return render_template('admin/review_webmark_proposal.html', webmark_proposal=webmark_proposal)


@main.route('/webmark', methods=['GET', 'POST'])
def webmarks():
    subscription = None
    if current_user.is_authenticated:
        subscription = Subscription.query.filter_by(user_id=current_user.id).first()
    tags = Tag.query.order_by(Tag.name).all()
    page = request.args.get('page', 1, type=int)
    rating = request.args.get('rating', type=int)
    comment = request.args.get('comment', type=int)
    if rating == 1:
        pagination = Webmark.query.order_by(Webmark.rating_avg.desc()).paginate(page, per_page=6, error_out=False)
    elif comment == 1:
        pagination = Webmark.query.order_by(Webmark.comments_count.desc()).paginate(page, per_page=6, error_out=False)
    else:
        pagination = Webmark.query.order_by(Webmark.timestamp.desc()).paginate(page, per_page=6, error_out=False)

    webmarks = pagination.items

    form = WebMarkProposalForm()
    if form.validate_on_submit():
        webmark_proposal = WebmarkProposal(name=form.name.data,
                                           email=form.email.data,
                                           url=form.url.data,
                                           details=form.details.data)
        db.session.add(webmark_proposal)
        db.session.commit()
        flash('The new webmark ' + form.name.data + ' has been proposed, we will evaluate it asap.')
        return redirect(url_for('main.webmarks'))
    else:
        if form.errors:
            flash(form.errors)
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        form.email.data = user.email

    return render_template('webmarks.html', subscription=subscription, webmarks=webmarks, tags=tags, pagination=pagination, form=form)


@main.route('/webmark-vote/<int:id>', methods=['POST'])
@login_required
def webmark_vote(id):
    if request.method == 'POST':
        if request.form.get("rating"):
            star = Star(webmark_id=id,
                        star=request.form.get("rating"),
                        author_id=current_user.get_id())
            db.session.add(star)
            db.session.commit()

            ratingaverage = Star.query.with_entities(func.avg(Star.star)).filter_by(webmark_id=id).all()
            rating_average = 0
            for i in ratingaverage:
                if i:
                    for j in i:
                        rating_average = j

            db.session.query(Webmark).filter(Webmark.id == id).update(
                {Webmark.rating_avg: rating_average})
            db.session.commit()

            flash('Your rating result has been recorded.')
    return redirect(url_for('main.webmark', id=id))


@main.route('/run-webmark/<int:id>', methods=['GET'])
@login_required
def run_webmark(id):
    token = current_user.generate_auth_token(expiration=14400)
    webmark = Webmark.query.with_entities(Webmark.id, Webmark.name, Webmark.test_path, Webmark.score_measurement_unit, Webmark.ready, Webmark.config,
                                          Webmark.duration).filter_by(id=id).first()
    return render_template('t/bridge.html', webmarkid=id, token=token, webmark=webmark, uid=current_user.get_id())


@main.route('/webmark/<int:id>', methods=['GET', 'POST'])
def webmark(id):
    star_num = Star.query.filter_by(webmark_id=id).filter_by(author_id=current_user.get_id()).count()
    webmark = Webmark.query.filter_by(id=id).first_or_404()
    tag_list = get_tag_list_from_webmark_id(id)

    news = db.session.query(News, User). \
        filter(News.webmark_id == id). \
            filter(User.id == News.author_id). \
            order_by(News.timestamp.desc()).all()

    if webmark.click_count:
        click_count = webmark.click_count + 1
    else:
        click_count = 1
    db.session.query(Webmark).filter(Webmark.id == id).update(
        {Webmark.click_count: click_count})
    db.session.commit()

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          webmark_id=id,
                          author_id=current_user.get_id())
        db.session.add(comment)
        db.session.commit()

        comments_count = Comment.query.filter_by(webmark_id=id).count()
        db.session.query(Webmark).filter(Webmark.id == id).update(
            {Webmark.comments_count: comments_count})
        db.session.commit()

        if current_user.is_authenticated:
            user = User.query.filter_by(id=current_user.get_id()).first()
            sub = db.session.query(Subscription, User). \
                filter(Subscription.global_subscribe == 1). \
                filter(User.id == Subscription.user_id).all()
            for s, u in sub:
                send_email(u.email, 'New comment for ' + webmark.name,
                           'main/mail/subscription', user=user, webmark=webmark, u=u)

        flash('Your comment has been published.')
        return redirect(url_for('main.webmark', id=id))
    else:
        if form.errors:
            flash(form.errors)

    results = db.session.query(Comment, User). \
        filter(Comment.author_id == User.id). \
        filter(Comment.webmark_id == id). \
        order_by(Comment.timestamp.desc()).all()

    ratings = Star.query.filter_by(webmark_id=id).all()

    return render_template('webmark.html', webmark=webmark, tag=tag_list, results=results, ratings=ratings, form=form,
                           star_num=star_num, news=news)


@main.route('/webmark-comment-delete/', methods=['POST'])
@login_required
@admin_required
def webmark_comment_delete():
    if request.method == 'POST':
        comment_id = request.form["comment_id"]
        db.session.query(Comment).filter(Comment.id == comment_id).delete()
        db.session.commit()
        flash('The comment id: ' + comment_id + ' has been deleted.')

        if request.form.get("webmark_id"):
            webmark_id = request.form["webmark_id"]
            return redirect(url_for('main.webmark', id=webmark_id))
        else:
            return redirect(url_for('main.user', username=current_user.username))


@main.route('/webmark/tag/<string:name>')
def webmarktag(name):
    subscription = None
    if current_user.is_authenticated:
        subscription = Subscription.query.filter_by(user_id=current_user.id).first()
    tag_list = Tag.query.order_by(Tag.name).all()
    tag = Tag.query.filter_by(name=name).first()
    tagwebmark = TagWebMark.query.filter_by(tag_id=tag.id).all()
    webmarkids = []
    for i in tagwebmark:
        webmarkids.append(i.webmark_id)
    webmarks = Webmark.query.filter(Webmark.id.in_(webmarkids)).all()

    form = WebMarkProposalForm()
    if form.validate_on_submit():
        webmark_proposal = WebmarkProposal(name=form.name.data,
                                           email=form.email.data,
                                           url=form.url.data,
                                           details=form.details.data)
        db.session.add(webmark_proposal)
        db.session.commit()
        flash('The new webmark ' + form.name.data + ' has been proposed, we will evaluate it asap.')
        return redirect(url_for('main.webmarks'))
    else:
        if form.errors:
            flash(form.errors)
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        form.email.data = user.email

    return render_template('webmarks.html', webmarks=webmarks, tags=tag_list, name=name, form=form, subscription=subscription)


def get_tag_list_from_webmark_id(id):
    webmark = Webmark.query.filter_by(id=id).first_or_404()
    tag_webmark = TagWebMark.query.filter_by(webmark_id=webmark.id).all()
    tag_list = []
    for tagid in tag_webmark:
        tag = Tag.query.filter_by(id=tagid.tag_id).first_or_404()
        if tag:
            tag_list.append(tag.name)
    return tag_list


def insert_tag_from_list(tag_list):
    for tmp in tag_list:
        if Tag.query.filter_by(name=tmp).count() < 1:
            if tmp.strip():
                tag = Tag()
                tag.name = tmp
                db.session.add(tag)
                db.session.commit()


def insert_tag_webmark_relation_from_webmark_name(webmark_name, tag_list):
    webmarkquery = Webmark.query.filter_by(name=webmark_name).first()
    if webmarkquery:
        for tmp in tag_list:
            tagquery = Tag.query.filter_by(name=tmp).first()
            if tagquery:
                tagwebmark = TagWebMark(webmark_id=webmarkquery.id,
                                        tag_id=tagquery.id)
                db.session.add(tagwebmark)
                db.session.commit()


def delete_tag_webmark_relation_from_webmark_id(webmark_id):
    TagWebMark.query.filter_by(webmark_id=webmark_id).delete()
    db.session.commit()


def tag_list_to_string(list):
    return '; '.join(list)


def remove_duplicated_list(list):
    func = lambda x, y: x if y in x else x + [y]
    return reduce(func, [[], ] + list)


@login_required
@admin_required
def clean_unrelated_tags():
    tag_webmark_id = db.session.query(TagWebMark.tag_id)
    tag_unrelated = db.session.query(Tag).filter(~Tag.id.in_(tag_webmark_id)).all()
    for i in tag_unrelated:
        Tag.query.filter_by(id=i.id).delete()
        db.session.commit()


@login_required
@admin_required
@main.route('/tag-clean', methods=['GET', 'POST'])
def tag_clean():
    clean_unrelated_tags()
    form = WebMarkForm()
    return render_template('index.html')


@main.route('/add-webmark', methods=['GET', 'POST'])
@login_required
@admin_required
def add_webmark():
    form = WebMarkForm()
    if form.validate_on_submit():
        f = form.screenshot_path.data
        filenameadjust = ''
        if f:
            filename = secure_filename(f.filename)
            filenameadjust = secure_filename(form.name.data) + filename[-4:]
            f.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], filenameadjust
            ))
        webmark = Webmark(name=form.name.data,
                          metrics=form.metrics.data,
                          # ready=form.ready.data,
                          # duration=form.duration.data,
                          version=form.version.data,
                          license=form.license.data,
                          developed_by=form.developed_by.data,
                          screenshot_path=filenameadjust,
                          url=form.url.data,
                          repo_url=form.repo_url.data,
                          summary=form.summary.data,
                          details=form.details.data,
                          pros=form.pros.data,
                          cons=form.cons.data,
                          author_id=current_user.get_id())
        db.session.add(webmark)
        db.session.commit()

        tag_data = form.tags.data
        tag_data = re.split(r'[;,\s]\s*', tag_data)
        tag_list = []
        for i in tag_data:
            if i:
                tag_list.append(i.strip())
        insert_tag_from_list(remove_duplicated_list(tag_list))
        insert_tag_webmark_relation_from_webmark_name(form.name.data, remove_duplicated_list(tag_list))

        clean_unrelated_tags()
        flash('The new webmark ' + form.name.data + ' has been added.')
        return redirect(url_for('main.webmarks'))
    else:
        if form.errors:
            flash(form.errors)
    return render_template('admin/add_webmark.html', form=form)


@main.route('/edit-my-browser-results/', methods=['POST'])
@login_required
def edit_my_browser_results():
    if request.method == 'POST':
        dict = request.form.to_dict()
        for i in dict:
            id = str(i).replace('s', '').replace('d', '')
            if i.find('d') > -1:
                db.session.query(Scores).filter(Scores.id == int(id)).delete()
                db.session.commit()
            if i.find('s') > -1:
                db.session.query(Scores).filter(Scores.id == int(id)).update(
                    {Scores.cpu_name: dict[i]})
                db.session.commit()
    return redirect(url_for('main.review_my_browser_results'))


@main.route('/review-my-browser-results/', methods=['GET'])
@login_required
def review_my_browser_results():
    results = db.session.query(Webmark, Scores).filter(Scores.webmark_id == Webmark.id).filter(Scores.author_id == current_user.get_id()).order_by(Scores.webmark_id).all()
    return render_template('review_my_browser_results.html', results=results)


@main.route('/edit-webmark-test/', methods=['POST'])
@login_required
@admin_required
def edit_webmark_test():
    if request.method == 'POST':
        dict = request.form.to_dict()
        for i in dict:
            id = str(i).replace('r', '').replace('d', '').replace('c', '').replace('p', '').replace('m', '')
            if i.find('d') > -1:
                db.session.query(Webmark).filter(Webmark.id == int(id)).update(
                        {Webmark.duration: dict[i]})
                db.session.commit()
            if i.find('p') > -1:
                db.session.query(Webmark).filter(Webmark.id == int(id)).update(
                        {Webmark.test_path: dict[i]})
                db.session.commit()
            elif i.find('c') > -1:
                db.session.query(Webmark).filter(Webmark.id == int(id)).update(
                        {Webmark.config: dict[i]})
                db.session.commit()
            elif i.find('m') > -1:
                db.session.query(Webmark).filter(Webmark.id == int(id)).update(
                        {Webmark.score_measurement_unit: dict[i]})
                db.session.commit()
            elif i.find('r') > -1:
                if dict[i] == 'Yes':
                    db.session.query(Webmark).filter(Webmark.id == int(id)).update(
                        {Webmark.ready: True})
                else:
                    db.session.query(Webmark).filter(Webmark.id == int(id)).update(
                        {Webmark.ready: False})
                db.session.commit()
    return redirect(url_for('main.review_webmark_test'))


@main.route('/review-webmark-test/', methods=['GET'])
@login_required
@admin_required
def review_webmark_test():
    webmarks = Webmark.query.with_entities(Webmark.id, Webmark.name, Webmark.ready, Webmark.test_path,
                                           Webmark.score_measurement_unit, Webmark.config, Webmark.duration,
                                           Webmark.timestamp)
    return render_template('admin/review_webmark_test.html', webmarks=webmarks)


@main.route('/add-webmark-news/', methods=['GET', 'POST'])
@login_required
@admin_required
def add_webmark_news():
    form = NewsForm()

    if form.validate_on_submit():
        wm = Webmark.query.get(form.forwebmark.data)
        news = News(webmark_id=wm.id,
                    summary=form.summary.data,
                    url=form.url.data,
                    details=form.details.data,
                    source=form.source.data,
                    author_id=current_user.get_id())
        db.session.add(news)
        db.session.commit()

        news_count = News.query.filter_by(webmark_id=wm.id).count()
        db.session.query(Webmark).filter(Webmark.id == wm.id).update(
            {Webmark.news_count: news_count})
        db.session.commit()

        if current_user.is_authenticated:
            wm = Webmark.query.get(form.forwebmark.data)
            webmark = Webmark.query.filter_by(id=wm.id).first()
            user = User.query.filter_by(id=current_user.get_id()).first()
            sub = db.session.query(Subscription, User). \
                filter(Subscription.global_subscribe == 1). \
                filter(User.id == Subscription.user_id).all()
            for s, u in sub:
                send_email(u.email, 'New update for ' + webmark.name,
                           'main/mail/subscription', user=user, webmark=webmark, u=u)

        flash('The news has been updated.')
        return redirect(url_for('main.review_webmark_news'))
    else:
        if form.errors:
            flash(form.errors)
    return render_template('admin/add_news.html', form=form)


@main.route('/delete-webmark-news/', methods=['POST'])
@login_required
@admin_required
def delete_webmark_news():
    if request.method == 'POST':
        dict = request.form.to_dict()
        for i in dict:
            id = str(i).replace('d', '')
            if i.find('d') > -1:
                db.session.query(News).filter(News.id == int(id)).delete()
                db.session.commit()
    return redirect(url_for('main.review_webmark_news'))


@main.route('/review-webmark-news/', methods=['GET', 'POST'])
@login_required
@admin_required
def review_webmark_news():
    results = db.session.query(Webmark, News, User). \
        filter(News.author_id == User.id). \
        filter(News.webmark_id == Webmark.id). \
        order_by(News.timestamp.desc()).all()
    return render_template('admin/review_news.html', results=results)


@main.route('/edit-webmark-news/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_webmark_news(id):
    news = News.query.filter_by(id=id).first()
    form = NewsForm(id=id)
    if form.validate_on_submit():
        webmark = Webmark.query.get(form.forwebmark.data)
        news.webmark_id = webmark.id,
        news.summary = form.summary.data,
        news.url = form.url.data,
        news.details = form.details.data,
        news.source = form.source.data,
        news.author_id = current_user.get_id()
        db.session.add(news)
        db.session.commit()
        flash('The news has been updated.')
        return redirect(url_for('main.review_webmark_news'))
    else:
        if form.errors:
            flash(form.errors)
        form.forwebmark.data = news.webmark_id
        form.summary.data = news.summary
        form.url.data = news.url
        form.details.data = news.details
        form.source.data = news.source
    return render_template('admin/edit_news.html', form=form)


@main.route('/review-webmark/', methods=['GET', 'POST'])
@login_required
@admin_required
def review_webmark():
    results = db.session.query(Webmark, User). \
        filter(Webmark.author_id == User.id). \
        order_by(Webmark.timestamp.desc()).all()
    return render_template('admin/review_webmark.html', results=results)


@main.route('/edit-webmark/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_webmark(id):
    webmark = Webmark.query.filter_by(id=id).first()
    if webmark:
        form = EditWebMarkForm(id=id)
        if form.validate_on_submit():
            delete_tag_webmark_relation_from_webmark_id(webmark.id)

            tag_data = form.tags.data
            tag_data = re.split(r'[;,\s]\s*', tag_data)
            insert_tag_from_list(remove_duplicated_list(tag_data))
            insert_tag_webmark_relation_from_webmark_name(form.name.data, remove_duplicated_list(tag_data))

            oldscreenshot = webmark.screenshot_path or ''
            f = form.screenshot_path.data
            webmark.name = form.name.data,
            webmark.metrics = form.metrics.data,
            webmark.tags = form.tags.data,
            webmark.version = form.version.data,
            webmark.license = form.license.data,
            webmark.developed_by = form.developed_by.data,
            # webmark.screenshot_path = f,
            webmark.url = form.url.data,
            webmark.repo_url = form.repo_url.data,
            webmark.summary = form.summary.data,
            webmark.details = form.details.data,
            webmark.pros = form.pros.data,
            webmark.cons = form.cons.data,
            webmark.author_id = current_user.get_id()
            if f:
                filename = secure_filename(f.filename)
                filenameadjust = secure_filename(form.name.data) + filename[-4:]
                f.save(os.path.join(
                    current_app.config['UPLOAD_FOLDER'], filenameadjust
                ))
                webmark.screenshot_path = filenameadjust
            # else:
            #     oldscreenshotpath = os.path.join(
            #         current_app.config['UPLOAD_FOLDER'], oldscreenshot
            #     )
            #     if os.path.isfile(oldscreenshotpath):
            #         os.remove(oldscreenshotpath)
            db.session.add(webmark)
            db.session.commit()

            flash('The ' + form.name.data + ' has been updated.')
            return redirect(url_for('main.webmark', id=webmark.id))
        else:
            if form.errors:
                flash(form.errors)
            form.name.data = webmark.name
            form.metrics.data = webmark.metrics
            form.tags.data = tag_list_to_string(get_tag_list_from_webmark_id(webmark.id))
            form.version.data = webmark.version
            form.license.data = webmark.license
            form.developed_by.data = webmark.developed_by
            form.screenshot_path.data = webmark.screenshot_path
            form.url.data = webmark.url
            form.repo_url.data = webmark.repo_url
            form.summary.data = webmark.summary
            form.details.data = webmark.details
            form.pros.data = webmark.pros
            form.cons.data = webmark.cons
        return render_template('admin/edit_webmark.html', form=form)
    else:
        flash('The webmark id:' + str(id) + ' does not exist.')
        return redirect(url_for('main.webmarks'))


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
               current_app.config['WEBMARK_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['WEBMARK_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMIN):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['WEBMARK_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['WEBMARK_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['WEBMARK_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))
