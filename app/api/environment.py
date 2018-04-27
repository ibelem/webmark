from flask import jsonify, request, g, url_for, current_app, redirect
from flask import make_response
from .. import db
from ..models import Environment, Webmark, User, Permission, Environment, CPU, GPU, Hardware, Software, Browser
from . import api
from .decorators import permission_required
from .errors import forbidden


@api.route('/environments/')
def get_environments():
    page = request.args.get('page', 1, type=int)
    pagination = Environment.query.paginate(
        page, per_page=current_app.config['WEBMARK_SCORES_PER_PAGE'],
        error_out=False)
    environments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_environments', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_environments', page=page + 1)
    return jsonify({
        'environments': [environment.to_json() for environment in environments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/environments/<int:id>')
def get_environment(id):
    environment = Environment.query.get_or_404(id)
    return jsonify(environment.to_json())


@api.route('/environments/', methods=['POST', 'OPTIONS'])
@permission_required(Permission.WRITE)
def new_environment():
    cpu_id = 0
    cpucheck = CPU.query.filter_by(name=request.json['cpu_name']).filter_by(
        architecture=request.json['cpu_architecture']).filter_by(
        hardware_concurrency=request.json['cpu_hardware_concurrency']).first()
    if cpucheck:
        cpu_id = cpucheck.id
    else:
        cpu = CPU(name=request.json['cpu_name'],
                  architecture=request.json['cpu_architecture'],
                  hardware_concurrency=request.json['cpu_hardware_concurrency'])
        db.session.add(cpu)
        db.session.commit()
        cpucheck = CPU.query.filter_by(name=request.json['cpu_name']).filter_by(
            architecture=request.json['cpu_architecture']).filter_by(
            hardware_concurrency=request.json['cpu_hardware_concurrency']).first()
        cpu_id = cpucheck.id
    print('G')
    gpu_id = 0
    gpucheck = GPU.query.filter_by(name=request.json['gpu_name']).filter_by(
        vender=request.json['gpu_vender']).first()
    if gpucheck:
        gpu_id = gpucheck.id
    else:
        gpu = GPU(name=request.json['gpu_name'],
                  vender=request.json['gpu_vender'])
        db.session.add(gpu)
        db.session.commit()
        gpucheck = GPU.query.filter_by(name=request.json['gpu_name']).filter_by(
            vender=request.json['gpu_vender']).first()
        gpu_id = gpucheck.id
    print('B')
    browser_id = 0
    browsercheck = Browser.query.filter_by(ua=request.json['browser_ua']).first()
    if browsercheck:
        browser_id = browsercheck.id
    else:
        browser = Browser(name=request.json['browser_name'],
                          version=request.json['browser_version'],
                          major=request.json['browser_major'],
                          language=request.json['browser_language'],
                          engine_name=request.json['browser_engine_name'],
                          engine_version=request.json['browser_engine_version'],
                          ua=request.json['browser_ua'],
                          channel=request.json['browser_channel'])
        db.session.add(browser)
        db.session.commit()
        browsercheck = Browser.query.filter_by(ua=request.json['browser_ua']).first()
        browser_id = browsercheck.id
    print('S')
    software_id = 0
    softwarecheck = Software.query.filter_by(os=request.json['software_os']).filter_by(
        os_version=request.json['software_os_version']).filter_by(
        platform=request.json['software_platform']).filter_by(
        timezone=request.json['software_timezone']).first()
    if softwarecheck:
        software_id = softwarecheck.id
    else:
        software = Software(os=request.json['software_os'],
                            os_version=request.json['software_os_version'],
                            platform=request.json['software_platform'],
                            timezone=request.json['software_timezone'])
        db.session.add(software)
        db.session.commit()
        softwarecheck = Software.query.filter_by(os=request.json['software_os']).filter_by(
            os_version=request.json['software_os_version']).filter_by(
            platform=request.json['software_platform']).filter_by(
            timezone=request.json['software_timezone']).first()
        software_id = softwarecheck.id
    print('H')
    hardware_id = 0
    hardwarecheck = Hardware.query.filter_by(device_vendor=request.json['hardware_device_vendor']).filter_by(
        device_model=request.json['hardware_device_model']).filter_by(
        device_type=request.json['hardware_device_type']).filter_by(
        device_memory=request.json['hardware_device_memory']).filter_by(
        screen_width=request.json['hardware_screen_width']).filter_by(
        screen_height=request.json['hardware_screen_height']).first()
    print('H1')
    if hardwarecheck:
        hardware_id = hardwarecheck.id
        print('H3')
    else:
        hardware = Hardware(device_vendor=request.json['hardware_device_vendor'],
                            device_model=request.json['hardware_device_model'],
                            device_type=request.json['hardware_device_type'],
                            device_memory=request.json['hardware_device_memory'],
                            screen_width=int(request.json['hardware_screen_width']),
                            screen_height=int(request.json['hardware_screen_height']))
        print('H5')
        db.session.add(hardware)
        db.session.commit()
        hardwarecheck = Hardware.query.filter_by(device_vendor=request.json['hardware_device_vendor']).filter_by(
            device_model=request.json['hardware_device_model']).filter_by(
            device_type=request.json['hardware_device_type']).filter_by(
            device_memory=request.json['hardware_device_memory']).filter_by(
            screen_width=request.json['hardware_screen_width']).filter_by(
            screen_height=request.json['hardware_screen_height']).first()
        hardware_id = hardwarecheck.id

    print('E')
    environment_id = 0
    environmentcheck = Environment.query.filter_by(hardware_id=hardware_id).filter_by(
        software_id=software_id).filter_by(browser_id=browser_id).filter_by(
        browser_id=browser_id).filter_by(cpu_id=cpu_id).filter_by(
        gpu_id=gpu_id).first()
    if environmentcheck:
        environment_id = environmentcheck.id
    else:
        environment = Environment(hardware_id=hardware_id,
                                  software_id=software_id,
                                  browser_id=browser_id,
                                  cpu_id=cpu_id,
                                  gpu_id=gpu_id)
        db.session.add(environment)
        db.session.commit()
        environmentcheck = Environment.query.filter_by(hardware_id=hardware_id).filter_by(
            software_id=software_id).filter_by(browser_id=browser_id).filter_by(
            browser_id=browser_id).filter_by(cpu_id=cpu_id).filter_by(
            gpu_id=gpu_id).first()
        environment_id = environmentcheck.id
    return jsonify(h=hardware_id, s=software_id, b=browser_id, c=cpu_id, g=gpu_id, id=environment_id), 201, \
         {'Location': url_for('api.get_environments')}


@api.route('/environments/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_environment(id):
    environment = Environment.query.get_or_404(id)
    if g.current_user != environment.author and \
            not g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    environment.body = request.json.get('body', environment.body)
    db.session.add(environment)
    db.session.commit()
    return jsonify(environment.to_json())
