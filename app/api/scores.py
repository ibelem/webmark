from flask import jsonify, request, g, url_for, current_app
from flask import make_response
from .. import db
from ..models import Scores, Webmark, User, Permission
from . import api
from .decorators import permission_required
from .errors import forbidden


@api.route('/scores/')
def get_scores():
    page = request.args.get('page', 1, type=int)
    pagination = Scores.query.paginate(
        page, per_page=current_app.config['WEBMARK_SCORES_PER_PAGE'],
        error_out=False)
    scores = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_scores', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_scores', page=page + 1)
    return jsonify({
        'scores': [score.to_json() for score in scores],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/scores/<int:id>')
def get_score(id):
    score = Scores.query.get_or_404(id)
    return jsonify(score.to_json())


@api.route('/scores/', methods=['POST', 'OPTIONS'])
@permission_required(Permission.WRITE)
def new_score():
    scorecheck = Scores.query.filter_by(browser_name=request.json['browser_name'],
                                        browser_version=request.json['browser_version'],
                                        browser_major=request.json['browser_major'],
                                        browser_language=request.json['browser_language'],
                                        browser_engine_name=request.json['browser_engine_name'],
                                        browser_engine_version=request.json['browser_engine_version'],
                                        browser_ua=request.json['browser_ua'],
                                        browser_channel=request.json['browser_channel'],
                                        cpu_name=request.json['cpu_name'],
                                        cpu_architecture=request.json['cpu_architecture'],
                                        cpu_hardware_concurrency=request.json['cpu_hardware_concurrency'],
                                        gpu_name=request.json['gpu_name'],
                                        gpu_vender=request.json['gpu_vender'],
                                        device_vendor=request.json['hardware_device_vendor'],
                                        device_model=request.json['hardware_device_model'],
                                        device_type=request.json['hardware_device_type'],
                                        device_memory=request.json['hardware_device_memory'],
                                        screen_width=request.json['hardware_screen_width'],
                                        screen_height=request.json['hardware_screen_height'],
                                        os=request.json['software_os'],
                                        os_version=request.json['software_os_version'],
                                        platform=request.json['software_platform'],
                                        timezone=request.json['software_timezone'],
                                        author_id=request.json['author_id'],
                                        webmark_id=request.json['webmark_id']).first()

    if scorecheck:
        print(scorecheck)
        return jsonify({'score_id': scorecheck.id}), 201, \
               {'Location': url_for('api.get_scores')}
    else:
        score = Scores.from_json(request.json)
        db.session.add(score)
        db.session.commit()
        scorecheck = Scores.query.filter_by(browser_name=request.json['browser_name'],
                                            browser_version=request.json['browser_version'],
                                            browser_major=request.json['browser_major'],
                                            browser_language=request.json['browser_language'],
                                            browser_engine_name=request.json['browser_engine_name'],
                                            browser_engine_version=request.json['browser_engine_version'],
                                            browser_ua=request.json['browser_ua'],
                                            browser_channel=request.json['browser_channel'],
                                            cpu_name=request.json['cpu_name'],
                                            cpu_architecture=request.json['cpu_architecture'],
                                            cpu_hardware_concurrency=request.json['cpu_hardware_concurrency'],
                                            gpu_name=request.json['gpu_name'],
                                            gpu_vender=request.json['gpu_vender'],
                                            device_vendor=request.json['hardware_device_vendor'],
                                            device_model=request.json['hardware_device_model'],
                                            device_type=request.json['hardware_device_type'],
                                            device_memory=request.json['hardware_device_memory'],
                                            screen_width=request.json['hardware_screen_width'],
                                            screen_height=request.json['hardware_screen_height'],
                                            os=request.json['software_os'],
                                            os_version=request.json['software_os_version'],
                                            platform=request.json['software_platform'],
                                            timezone=request.json['software_timezone'],
                                            author_id=request.json['author_id'],
                                            webmark_id=request.json['webmark_id']).first()
        print(scorecheck)
        return jsonify({'score_id': scorecheck.id}), 201, \
               {'Location': url_for('api.get_scores')}


@api.route('/scoresfinal/', methods=['POST', 'OPTIONS'])
@permission_required(Permission.WRITE)
def scores_final():
    if request.method == 'POST':
        result = request.get_json()
        score_id = result['score_id']
        score = result['score']
        cpu = result['cpu']
        if score and score_id:
            db.session.query(Scores).filter(Scores.id == int(score_id)).update(
                            {Scores.score: score, Scores.cpu_name: cpu})
            db.session.commit()
        return jsonify({'score_id': score_id, 'score': score}), 201, \
               {'Location': url_for('api.get_scores')}
    return jsonify({'options': True})


@api.route('/scores/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_score(id):
    score = Scores.query.get_or_404(id)
    if g.current_user != score.author and \
            not g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    score.body = request.json.get('body', score.body)
    db.session.add(score)
    db.session.commit()
    return jsonify(score.to_json())
