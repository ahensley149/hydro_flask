from datetime import datetime
from sensor_data import current_ph, current_ec
from models import *


@app.route('/', methods=['POST', 'GET'])

def dashboard():
    """Home page view of the app, passes all active environments to dashboard.html
      template to display
    """
    environments = Enviro.query.filter(Enviro.active == 1)
    return render_template('dashboard.html', enviros=environments)

@app.route('/add_enviro', methods=['POST', 'GET'])

def add_environment():
    """If there is a POST request to /add_enviro, it creates a new enviro row
      in the database, otherwise just returns the add_enviroment.html template
    """
    plants = Plant.query.all()
    waters = Water.query.all()
    lights = Light.query.all()

    if request.method == 'POST':
        name = request.form['name']
        water = request.form['water_id']
        light = request.form['light_id']
        ph = request.form['ph_sensor']
        ec = request.form['ec_sensor']
        water_pump = request.form['water_pump']
        air_pump = request.form['air_pump']
        ph_solenoid = request.form['ph_solenoid']
        nutrient_solenoid = request.form['nutrient_solenoid']
        if not request.form['active']:
            active = 0
        else:
            active = request.form['active']
        plants = request.form.getlist('plant')
        
        new_enviro = Enviro(name=name, water_id=water, light_id=light, active=active, ph_sensor=ph, ec_sensor=ec,
            water_pump=water_pump, air_pump=air_pump, ph_solenoid=ph_solenoid, nutrient_solenoid=nutrient_solenoid)
        for plant in plants:
            new_plant = Plant.query.get(plant)
            new_enviro.plants.append(new_plant)

        try:
            db.session.add(new_enviro)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your environment'

    else:
        return render_template('add_environment.html', plants=plants, waters=waters, lights=lights)

@app.route('/update_enviro/<int:id>', methods=['POST', 'GET'])

def update_enviro(id):
    """If there is a POST request to /update_enviro/{id}, it updates the enviro row
      in the database, otherwise just returns the update_enviroment.html template
    """
    enviro = Enviro.query.get_or_404(id)

    if request.method == 'POST':
        enviro.name = request.form['name']
        enviro.water_id = request.form['water_id']
        enviro.light_id = request.form['light_id']
        enviro.ph_sensor = request.form['ph_sensor']
        enviro.ec_sensor = request.form['ec_sensor']
        enviro.active = request.form['active']
        plants = request.form.getlist('plant')
        enviro.plants = []

        for plant in plants:
            new_plant = Plant.query.get(plant)
            enviro.plants.append(new_plant)

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Update Unsuccesful'
    else:
        plants = Plant.query.all()
        lights = Light.query.all()
        airs = Air.query.all()
        waters = Water.query.all()

        return render_template('update_environment.html', enviro=enviro, plants=plants, lights=lights, airs=airs, waters=waters)

@app.route('/delete_enviro/<int:id>')


def delete_enviro(id):
    """Deletes the environment related to the id sent to /delete_enviro/{id}"""
    enviro_to_delete = Enviro.query.get_or_404(id)

    try:
        db.session.delete(enviro_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem delting that task'
        
@app.route('/add_water', methods=['POST', 'GET'])

def add_water_profile():
    water1 = Water(name='Default')
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

@app.route('/add_plant', methods=['POST', 'GET'])

def add_plant():
    plant1 = Plant(name="Roma Tomatoes")
    plant2 = Plant(name="Beef Steak Tomatoes")
    plant3 = Plant(name="Kale")

    try:
        db.session.add(plant1)
        db.session.add(plant2)
        db.session.add(plant3)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue adding your task'

if __name__ == "__main__":
    app.run(debug=True)


