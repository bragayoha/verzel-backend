from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, create_access_token, verify_password, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, User, Car
from uploads import images, configure_uploads
from config.config import app

configure_uploads(app)

# Função para verificar se a extensão do arquivo é permitida
def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

# Rota de Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=email, expires_delta=False)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid/Incorrect email or password."}), 401

# Rotas protegidas por JWT para Usuários
@app.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'name': user.name, 'email': user.email, 'cpf': user.cpf} for user in users]
    return jsonify({'users': users_list})

@app.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_data = {'id': user.id, 'name': user.name, 'email': user.email, 'cpf': user.cpf}
    user_data['cars'] = [{'id': car.id, 'brand': car.brand, 'model': car.model, 'year': car.year, 'value': car.value} for car in user.cars]
    return jsonify(user_data)

@app.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    try:
        new_user = User(name=data['name'], email=data['email'], cpf=data['cpf'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'id': new_user.id, 'name': new_user.name, 'email': new_user.email, 'cpf': new_user.cpf}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    if int(current_user_id) == user_id:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        try:
            user.name = data['name']
            user.email = data['email']
            user.cpf = data['cpf']
            db.session.commit()
            return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'cpf': user.cpf})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()

    if int(current_user_id) == user_id:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'Unauthorized'}), 401

# Rotas protegidas por JWT para Carros
@app.route('/cars', methods=['GET'])
def get_all_cars():
    cars = Car.query.order_by(Car.value.desc()).all()
    cars_list = [{'id': car.id, 'brand': car.brand, 'model': car.model, 'year': car.year, 'value': car.value, 'user_id': car.user_id} for car in cars]
    return jsonify({'cars': cars_list})


@app.route('/cars', methods=['POST'])
@jwt_required()
def create_car():
    data = request.form
    try:
        new_car = Car(
            brand=data['brand'],
            model=data['model'],
            year=data['year'],
            value=float(data['value']),
            user_id=data['user_id']
        )

        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_image(image.filename):
                filename = secure_filename(image.filename)
                image_path = current_app.config['UPLOADED_IMAGES_DEST'] + filename
                image.save(image_path)
                new_car.image = images.url(filename)
            else:
                return jsonify({'error': 'Invalid file format for image'}), 400

        db.session.add(new_car)
        db.session.commit()

        return jsonify({
            'id': new_car.id,
            'brand': new_car.brand,
            'model': new_car.model,
            'year': new_car.year,
            'value': new_car.value,
            'user_id': new_car.user_id,
            'image': new_car.image
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/cars/<int:car_id>', methods=['PUT'])
@jwt_required()
def update_car(car_id):
    current_user_id = get_jwt_identity()

    car = Car.query.get_or_404(car_id)
    if int(current_user_id) == car.user_id:
        data = request.form
        try:
            car.brand = data['brand']
            car.model = data['model']
            car.year = data['year']
            car.value = float(data['value'])

            if 'image' in request.files:
                image = request.files['image']
                if image and allowed_image(image.filename):
                    filename = secure_filename(image.filename)
                    image_path = current_app.config['UPLOADED_IMAGES_DEST'] + filename
                    image.save(image_path)
                    car.image = images.url(filename)
                else:
                    return jsonify({'error': 'Invalid file format for image'}), 400

            db.session.commit()

            return jsonify({
                'id': car.id,
                'brand': car.brand,
                'model': car.model,
                'year': car.year,
                'value': car.value,
                'user_id': car.user_id,
                'image': car.image
            })
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/cars/<int:car_id>', methods=['DELETE'])
@jwt_required()
def delete_car(car_id):
    current_user_id = get_jwt_identity()
    car = Car.query.get_or_404(car_id)

    if int(current_user_id) == car.user_id:
        db.session.delete(car)
        db.session.commit()
        return jsonify({'message': 'Car deleted successfully'})
    else:
        return jsonify({'error': 'Unauthorized'}), 401