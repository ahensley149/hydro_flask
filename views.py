from datetime import datetime, date
from sensor_data import current_ph, current_ec
from models import *


@app.route('/', methods=['POST', 'GET'])

def dashboard():
    """Home page view of the app, passes all active environments to dashboard.html
      template to display
    """
    environments = Enviro.query.filter(Enviro.active == 1)
    return render_template('dashboard.html', enviros=environments)

@app.route('/enviro')

def list_environments():
    """Index of all environments for updating and deleting
    """
    environments = Enviro.query.all()    
    return render_template('index_enviro.html', enviros=environments)

@app.route('/add_enviro', methods=['POST', 'GET'])

def add_environment():
    """If there is a POST request to /add_enviro, it creates a new enviro row
      in the database, otherwise just returns the add_enviroment.html template
    """
    plants = Plant.query.all()
    waters = Water.query.all()
    lights = Light.query.all()
    airs = Air.query.all()

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
        active = request.form['active']
        plants = request.form.getlist('plant')
        
        new_enviro = Enviro(name=name, water_id=water, light_id=light, active=active, ph_sensor=ph, ec_sensor=ec,
            water_pump=water_pump, air_pump=air_pump, ph_solenoid=ph_solenoid, nutrient_solenoid=nutrient_solenoid)
        for plant in plants:
            new_plant = Plant.query.get(plant)
            new_plant.plant_date = str(date.today())
            new_enviro.plants.append(new_plant)

        try:
            db.session.add(new_enviro)
            db.session.commit()
            return redirect('/enviro')
        except:
            return 'There was an issue adding your environment'

    else:
        return render_template('add_environment.html', plants=plants, waters=waters, lights=lights, airs=airs)

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
            return redirect('/enviro')
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
        return redirect('/enviro')
    except:
        return 'There was a problem delting that task'

@app.route('/water')

def list_water_profile():
    waters = Water.query.all()
    return render_template('index_water.html', waters=waters)
        
@app.route('/add_water', methods=['POST', 'GET'])

def add_water_profile():
    if request.method == 'POST':
        name = request.form['name']
        min_ph = request.form['min_ph']
        max_ph = request.form['max_ph']
        min_ec = request.form['min_ec']
        max_ec = request.form['max_ec']
        new_water = Water(name=name, min_ph=min_ph, max_ph=max_ph, min_ec=min_ec, max_ec=max_ec)

        try:
            db.session.add(new_water)
            db.session.commit()
            return redirect('/water')
        except:
            return 'There was an issue adding your water profile'
    
    else:
        return render_template('add_water.html')

@app.route('/update_water/<int:id>', methods=['POST', 'GET'])

def update_water_profile(id):
    water = Water.query.get_or_404(id)
    if request.method == 'POST':
        water.name = request.form['name']
        water.min_ph = request.form['min_ph']
        water.max_ph = request.form['max_ph']
        water.min_ec = request.form['min_ec']
        water.max_ec = request.form['max_ec']
        
        try:
            db.session.commit()
            return redirect('/water')
        except:
            return 'There was an issue updating the water profile'
    
    else:
        return render_template('update_water.html', water=water)

@app.route('/delete_water/<int:id>', methods=['POST', 'GET'])

def delete_water_profile(id):
    water = Water.query.get_or_404(id)
    try:
        db.session.delete(water)
        db.session.commit()
        return redirect('/water')
    except:
        return 'There was an issue deleting the water profile'
    
    else:
        return render_template('update_water.html', water=water)

@app.route('/light')

def list_light_profiles():
    lights = Light.query.all()
    return render_template('index_light.html', lights=lights)

@app.route('/add_light', methods=['POST', 'GET'])

def add_light_profile():
    if request.method == 'POST':
        name = request.form['name']
        model = request.form['model']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        new_light = Light(name=name, model=model, start_time=start_time, end_time=end_time)

        try:
            db.session.add(new_light)
            db.session.commit()
            return redirect('/light')
        except:
            return 'There was an issue adding the light profile'
    
    else:
        return render_template('add_light.html')

@app.route('/update_light/<int:id>', methods=['POST', 'GET'])

def update_light_profile(id):
    light = Light.query.get_or_404(id)
    if request.method == 'POST':
        light.name = request.form['name']
        light.model = request.form['model']
        light.start_time = request.form['start_time']
        light.end_time = request.form['end_time']
        
        try:
            db.session.commit()
            return redirect('/light')
        except:
            return 'There was an issue updating the light profile'
    
    else:
        return render_template('update_light.html', light=light)

@app.route('/delete_light/<int:id>', methods=['POST', 'GET'])

def delete_light_profile(id):
    light = Light.query.get_or_404(id)
    try:
        db.session.delete(light)
        db.session.commit()
        return redirect('/light')
    except:
        return 'There was an issue deleting the light profile'

@app.route('/plant')

def list_plant_profiles():
    plants = Plant.query.all()
    return render_template('index_plant.html', plants=plants)

@app.route('/add_plant', methods=['POST', 'GET'])

def add_plant_profile():
    if request.method == 'POST':
        name = request.form['name']
        new_plant = Plant(name=name)

        try:
            db.session.add(new_plant)
            db.session.commit()
            return redirect('/plant')
        except:
            return 'There was an issue adding the plant'
    
    else:
        return render_template('add_plant.html')

@app.route('/update_plant/<int:id>', methods=['POST', 'GET'])

def update_plant_profile(id):
    plant = Plant.query.get_or_404(id)
    if request.method == 'POST':
        plant.name = request.form['name']
        
        try:
            db.session.commit()
            return redirect('/plant')
        except:
            return 'There was an issue updating the plant'
    
    else:
        return render_template('update_plant.html', plant=plant)

@app.route('/delete_plant/<int:id>', methods=['POST', 'GET'])

def delete_plant_profile(id):
    plant = Plant.query.get_or_404(id)
    try:
        db.session.delete(plant)
        db.session.commit()
        return redirect('/plant')
    except:
        return 'There was an issue deleting the plant'
    

@app.route('/air')

def list_air_profiles():
    airs = Air.query.all()
    return render_template('index_air.html', airs=airs)

@app.route('/add_air', methods=['POST', 'GET'])

def add_air_profile():
    if request.method == 'POST':
        name = request.form['name']
        min_temp = request.form['min_temp']
        max_temp = request.form['max_temp']
        min_humid = request.form['min_humid']
        max_humid = request.form['max_humid']

        new_air = Air(name=name,min_temp=min_temp,max_temp=max_temp,min_humid=min_humid,max_humid=max_humid)

        try:
            db.session.add(new_air)
            db.session.commit()
            return redirect('/air')
        except:
            return 'There was an issue adding the air profile'
    
    else:
        return render_template('add_air.html')

@app.route('/update_air/<int:id>', methods=['POST', 'GET'])

def update_air_profile(id):
    air = Air.query.get_or_404(id)
    if request.method == 'POST':
        air.name = request.form['name']
        air.min_temp = request.form['min_temp']
        air.max_temp = request.form['max_temp']
        air.min_humid = request.form['min_humid']
        air.max_humid = request.form['max_humid']

        try:
            db.session.commit()
            return redirect('/air')
        except:
            return 'There was an issue updating the air profile'
    
    else:
        return render_template('update_air.html', air=air)

@app.route('/delete_air/<int:id>', methods=['POST', 'GET'])

def delete_air_profile(id):
    air = Air.query.get_or_404(id)
    try:
        db.session.delete(air)
        db.session.commit()
        return redirect('/air')
    except:
        return 'There was an issue deleting the air profile'
    

@app.route('/pins')

def list_pins():
    ac_pins = Pin.query.filter_by(output = 1)
    dc_pins = Pin.query.filter_by(output = 2)
    return render_template('index_pins.html', ac_pins=ac_pins, dc_pins=dc_pins)

@app.route('/add_pin', methods=['POST', 'GET'])

def add_pin():
    if request.method == 'POST':
        num = request.form['num']
        output = request.form['output']
        gpio_pin = request.form['gpio_pin']

        new_pin = Pin(num=num,output=output,gpio_pin=gpio_pin)

        try:
            db.session.add(new_pin)
            db.session.commit()
            return redirect('/pins')
        except:
            return 'There was an issue adding the pin'
    
    else:
        return render_template('add_pin.html')

@app.route('/update_pin/<int:id>', methods=['POST', 'GET'])

def update_pin(id):
    pin = Pin.query.get_or_404(id)
    if request.method == 'POST':
        pin.num = request.form['num']
        pin.output = request.form['output']
        pin.gpio_pin = request.form['gpio_pin']

        try:
            db.session.commit()
            return redirect('/pins')
        except:
            return 'There was an issue updating the pin'
    
    else:
        return render_template('update_pin.html', pin=pin)

@app.route('/delete_pin/<int:id>', methods=['POST', 'GET'])

def delete_pin(id):
    pin = Pin.query.get_or_404(id)
    try:
        db.session.delete(pin)
        db.session.commit()
        return redirect('/pins')
    except:
        return 'There was an issue deleting the pin'

@app.route('/sensors', methods=['POST', 'GET'])

def sensors():
    ph_level = current_ph(1)
    ec_level = current_ec(1)
    if request.method == 'POST':
        if request.form['sensor'] == 'ph':
            offset = ph_level - request.form['actual_ph']
        else:
            offset = ec_level - request.form['actual_ec']
    
        return offset
    else:
        return render_template('sensor_calibration.html', ph_level=ph_level, ec_level=ec_level)

@app.route('/sensor/<int:sensor>', methods=['POST', 'GET'])

def sensor_calibration(sensor):
    ph_level = current_ph(1)
    ec_level = current_ec(1)
    if request.method == 'POST':
        if sensor == 1:
            offset = ph_level - float(request.form['actual_ph'])
        else:
            offset = ec_level - float(request.form['actual_ec'])
    
        return str(offset)
    else:
        return render_template('sensor_calibration.html', ph_level=ph_level, ec_level=ec_level)


if __name__ == "__main__":
    app.run(debug=True)


