from datetime import datetime
from sensor_data import current_ph, current_ec
from models import *


@app.route('/', methods=['POST', 'GET'])

def dashboard():
    environments = Enviro.query.filter(Enviro.active == 1)
    return render_template('dashboard.html', enviros=environments)

@app.route('/add_enviro', methods=['POST', 'GET'])

def add_environment():
    if request.method == 'POST':
        name = request.form['name']
        water = request.form['water_id']
        light = request.form['light_id']
        ph = request.form['ph_sensor']
        ec = request.form['ec_sensor']
        active = request.form['active']
        new_enviro = Enviro(name=name, water_id=water, light_id=light, active=active, ph_sensor=ph, ec_sensor=ec)

        try:
            db.session.add(new_enviro)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your environment'

    else:
        return render_template('add_environment.html')

@app.route('/add_water', methods=['POST', 'GET'])

def add_water():
    water1 = Water(name="Default")
    try:
        db.session.add(water1)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue adding your task'

@app.route('/add_light', methods=['POST', 'GET'])

def add_lights():
    light1 = Light(name="Default")
    try:
        db.session.add(light1)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue adding your task'

if __name__ == "__main__":
    app.run(debug=True)
