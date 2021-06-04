from datetime import datetime, date
from sensor_data import get_data
from models import *


@app.route('/', methods=['POST', 'GET'])
def dashboard():
    """Home page view of the app, passes all active environments to dashboard.html
      template to display current crops, sensor data and latest pictures
    """
    sensor_data = get_data('all')
    enviros = Enviro.query.filter(Enviro.active == 1)
    return render_template('enviro/dashboard.html', enviros=enviros, sensor_data=sensor_data)


@app.route('/enviro')
def list_environments():
    """Index of all environments for updating and deleting"""
    sensor_data = get_data('all')
    enviros = Enviro.query.all()    
    return render_template('enviro/index_enviro.html', enviros=enviros, sensor_data=sensor_data)


@app.route('/add_enviro', methods=['POST', 'GET'])
def add_environment():
    """If there is a POST request to /add_enviro, it creates a new enviro row
      in the database, otherwise just returns the add_enviroment.html template
    """
    if request.method == 'POST':
        name = request.form['name']
        water = request.form['water_id']
        light = request.form['light_id']
        air = request.form['air_id']
        ph = request.form['ph_sensor']
        ec = request.form['ec_sensor']
        air_sensor = request.form['air_sensor']
        water_pump = request.form['water_pump']
        air_pump = request.form['air_pump']
        light_outlet = request.form['light_outlet']
        nutrient_solenoid = request.form['nutrient_solenoid']
        active = request.form['active']
        
        new_enviro = Enviro(name=name, water_id=water, light_id=light, active=active, ph_sensor=ph, ec_sensor=ec, air_sensor=air_sensor,
            water_pump=water_pump, air_pump=air_pump, light_outlet=light_outlet, nutrient_solenoid=nutrient_solenoid, air_id=air)

        try:
            db.session.add(new_enviro)
            db.session.commit()
            return redirect('/enviro')
        except:
            return 'There was an issue adding your environment'

    else:
        waters = Water.query.all()
        lights = Light.query.all()
        airs = Air.query.all()
        return render_template('enviro/add_environment.html', plants=plants, waters=waters, lights=lights, airs=airs)


@app.route('/update_enviro/<int:id>', methods=['POST', 'GET'])
def update_enviro(id):
    """If there is a POST request to /update_enviro/{id}, it updates the enviro row
      in the database, otherwise just returns the update_enviroment.html template
    """
    enviro = Enviro.query.get_or_404(id)
    enviro.air_sensor = 0

    if request.method == 'POST':
        enviro.name = request.form['name']
        enviro.water_id = request.form['water_id']
        enviro.light_id = request.form['light_id']
        enviro.air_id = request.form['air_id']
        enviro.ph_sensor = request.form['ph_sensor']
        enviro.ec_sensor = request.form['ec_sensor']
        enviro.air_sensor = request.form['air_sensor']
        enviro.water_pump = request.form['water_pump']
        enviro.air_pump = request.form['air_pump']
        enviro.light_outlet = request.form['light_outlet']
        enviro.nutrient_solenoid = request.form['nutrient_solenoid']
        enviro.active = request.form['active']

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

        return render_template('enviro/update_environment.html', enviro=enviro, plants=plants, lights=lights, airs=airs, waters=waters)


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
    """Index of all water profiles for updating and deleting"""
    waters = Water.query.all()
    return render_template('water/index_water.html', waters=waters)
        

@app.route('/add_water', methods=['POST', 'GET'])
def add_water_profile():
    """If there is a POST request to /add_water, it creates a new water row
      in the database, otherwise just returns the add_water.html template
    """
    if request.method == 'POST':
        name = request.form['name']
        min_ph = request.form['min_ph']
        max_ph = request.form['max_ph']
        start_time = request.form['start_time']
        duration = request.form['duration']
        min_ec = request.form['min_ec']
        max_ec = request.form['max_ec']
        start_time = request.form['start_time']
        duration = request.form['duration']
        recurring = request.form['recurring']
        new_water = Water(name=name, min_ph=min_ph, max_ph=max_ph, min_ec=min_ec, max_ec=max_ec)

        try:
            db.session.add(new_water)
            db.session.commit()
            new_cycle = Cycle(water_id=new_water.id, start_time=start_time, duration=duration, recurring=recurring)
            db.session.add(new_cycle)
            db.session.commit()
            return redirect('/water')
        except:
            return 'There was an issue adding your water profile'
    else:
        return render_template('water/add_water.html')


@app.route('/update_water/<int:id>', methods=['POST', 'GET'])
def update_water_profile(id):
    """If there is a POST request to /update_water/{id}, it updates the water row
      in the database, otherwise just returns the update_water.html template
    """
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
        return render_template('water/update_water.html', water=water)


@app.route('/delete_water/<int:id>')
def delete_water_profile(id):
    """Deletes the water profile related to the id sent to /delete_water/{id}"""
    water = Water.query.get_or_404(id)
    try:
        db.session.delete(water)
        db.session.commit()
        return redirect('/water')
    except:
        return 'There was an issue deleting the water profile'
    

@app.route('/add_cycle/<int:water_id>')
def add_cycle(water_id):
    """If there is a POST request to /add_light, it creates a new light row
      in the database, otherwise just returns the add_light.html template
    """
    new_cycle = Cycle(water_id=water_id)

    try:
        db.session.add(new_cycle)
        db.session.commit()
        return redirect('/water')
    except:
        return 'There was an issue adding the cycle'


@app.route('/update_cycle/<int:id>', methods=['POST'])
def update_cycle(id):
    """If there is a POST request to /add_light, it creates a new light row
      in the database, otherwise just returns the add_light.html template
    """
    cycle = Cycle.query.get_or_404(id)
    if request.form['duration'] == "0":
        try:
            db.session.delete(cycle)
            db.session.commit()
            return redirect('/water')
        except:
            return 'There was an issue deleting the cycle'
    else:
        cycle.start_time = request.form['start_time']
        cycle.duration = request.form['duration']

        try:
            db.session.commit()
            return redirect('/water')
        except:
            return 'There was an issue updating the cycle'


@app.route('/light')
def list_light_profiles():
    """Index of all light profiles for updating and deleting"""
    lights = Light.query.all()
    return render_template('light/index_light.html', lights=lights)


@app.route('/add_light', methods=['POST', 'GET'])
def add_light_profile():
    """If there is a POST request to /add_light, it creates a new light row
      in the database, otherwise just returns the add_light.html template
    """
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
        return render_template('light/add_light.html')


@app.route('/update_light/<int:id>', methods=['POST', 'GET'])
def update_light_profile(id):
    """If there is a POST request to /update_light/{id}, it updates the light row
      in the database, otherwise just returns the update_light.html template
    """
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
        return render_template('light/update_light.html', light=light)


@app.route('/delete_light/<int:id>')
def delete_light_profile(id):
    """Deletes the light profile related to the id sent to /delete_light/{id}"""
    light = Light.query.get_or_404(id)
    try:
        db.session.delete(light)
        db.session.commit()
        return redirect('/light')
    except:
        return 'There was an issue deleting the light profile'


@app.route('/plant')
def list_plant_profiles():
    """Index of all plant profiles for updating and deleting"""
    plants = Plant.query.all()
    return render_template('plant/index_plant.html', plants=plants)


@app.route('/add_plant', methods=['POST', 'GET'])
def add_plant_profile():
    """If there is a POST request to /add_plant, it creates a new water row
      in the database, otherwise just returns the add_plant.html template
    """
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
        return render_template('plant/add_plant.html')


@app.route('/update_plant/<int:id>', methods=['POST', 'GET'])
def update_plant_profile(id):
    """If there is a POST request to /update_plant/{id}, it updates the plant row
      in the database, otherwise just returns the update_plant.html template
    """
    plant = Plant.query.get_or_404(id)
    if request.method == 'POST':
        plant.name = request.form['name']
        
        try:
            db.session.commit()
            return redirect('/plant')
        except:
            return 'There was an issue updating the plant'
    
    else:
        return render_template('plant/update_plant.html', plant=plant)


@app.route('/delete_plant/<int:id>')
def delete_plant_profile(id):
    """Deletes the plant profile related to the id sent to /delete_plant/{id}"""
    plant = Plant.query.get_or_404(id)
    try:
        db.session.delete(plant)
        db.session.commit()
        return redirect('/plant')
    except:
        return 'There was an issue deleting the plant'
    

@app.route('/air')
def list_air_profiles():
    """Index of all airr profiles for updating and deleting"""
    airs = Air.query.all()
    return render_template('air/index_air.html', airs=airs)


@app.route('/add_air', methods=['POST', 'GET'])
def add_air_profile():
    """If there is a POST request to /add_air, it creates a new air row
      in the database, otherwise just returns the add_air.html template
    """
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
        return render_template('air/add_air.html')


@app.route('/update_air/<int:id>', methods=['POST', 'GET'])
def update_air_profile(id):
    """If there is a POST request to /update_air/{id}, it updates the air row
      in the database, otherwise just returns the update_air.html template
    """
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
        return render_template('air/update_air.html', air=air)


@app.route('/delete_air/<int:id>')
def delete_air_profile(id):
    """Deletes the air profile related to the id sent to /delete_air/{id}"""
    air = Air.query.get_or_404(id)
    try:
        db.session.delete(air)
        db.session.commit()
        return redirect('/air')
    except:
        return 'There was an issue deleting the air profile'
    

@app.route('/pins')
def list_pins():
    """Index of all pins for updating and deleting and
      sensor calibration for attached sensors with a current value reading 
      and input box for correct value to calculate offset for calibration
    """
    # TODO add auto calibration by using offset value calculated to update sensor_data.py
    ac_pins = Pin.query.filter_by(output = 1)
    dc_pins = Pin.query.filter_by(output = 2)
    ph_level = current_ph(1)
    ec_level = current_ec(1)
    if request.method == 'POST':
        if request.form['sensor'] == 'ph':
            offset = ph_level - request.form['actual_ph']
        else:
            offset = ec_level - request.form['actual_ec']
    
        return offset
    return render_template('pin/index_pins.html', ac_pins=ac_pins, dc_pins=dc_pins, ph_level=ph_level, ec_level=ec_level)


@app.route('/add_pin', methods=['POST', 'GET'])
def add_pin():
    """If there is a POST request to /add_pin, it creates a new pin row
      in the database, otherwise just returns the add_pin.html template
    """
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
        return render_template('pin/add_pin.html')


@app.route('/update_pin/<int:id>', methods=['POST', 'GET'])
def update_pin(id):
    """If there is a POST request to /update_pin/{id}, it updates the pin row
      in the database, otherwise just returns the update_pin.html template
    """
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
        return render_template('pin/update_pin.html', pin=pin)


@app.route('/delete_pin/<int:id>')
def delete_pin(id):
    """Deletes the pin related to the id sent to /delete_pin/{id}"""
    pin = Pin.query.get_or_404(id)
    try:
        db.session.delete(pin)
        db.session.commit()
        return redirect('/pins')
    except:
        return 'There was an issue deleting the pin'


@app.route('/sensors', methods=['POST', 'GET'])
def sensors():
    """OUTDATED - added sensor calibration to pins page
      Will Delete Soon once settings/pin page is finalized
    """
    ph_level = current_ph(1)
    ec_level = current_ec(1)
    if request.method == 'POST':
        if request.form['sensor'] == 'ph':
            offset = ph_level - request.form['actual_ph']
        else:
            offset = ec_level - request.form['actual_ec']
    
        return offset
    else:
        return render_template('pin/sensor_calibration.html', ph_level=ph_level, ec_level=ec_level)


@app.route('/sensor/<int:sensor>', methods=['POST', 'GET'])
def sensor_calibration(sensor):
    """OUTDATED - added sensor calibration to pins page
      Will Delete Soon once settings/pin page is finalized
    """
    ph_level = current_ph(1)
    ec_level = current_ec(1)
    if request.method == 'POST':
        if sensor == 1:
            offset = ph_level - float(request.form['actual_ph'])
        else:
            offset = ec_level - float(request.form['actual_ec'])
    
        return str(offset)
    else:
        return render_template('pin/sensor_calibration.html', ph_level=ph_level, ec_level=ec_level)


@app.route('/add_crop/<int:enviro_id>', methods=['POST', 'GET'])
def add_crop(enviro_id):
    """If there is a POST request to /add_crop/{enviro_id}, it creates a new crop row
      in the database associated with the passed enviro_id and plant date of today, 
      otherwise just returns the add_crop/{enviro_id}.html template
    """
    if request.method == 'POST':
        plants = request.form.getlist('plants')
        name = request.form['name']
        date = datetime.today()
        plant_date = date.strftime("%d/%m/%Y")
        new_crop = Crop(enviro_id=enviro_id,plants=[],plant_date=plant_date, name=name)

        for plant in plants:
            new_plant = Plant.query.get(plant)
            new_crop.plants.append(new_plant)

        try:
            db.session.add(new_crop)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding the crop'
    else:
        plants = Plant.query.all()
        return render_template('crop/add_crop.html', plants=plants, enviro_id=enviro_id)


@app.route('/crop/<int:id>', methods=['POST', 'GET'])
def crop(id):
    """Displays crop data for current crop and allows for updating crop progress
      Allows adding manual task and additional notes, setting milestone dates,
      adding photos, and splitting plants from the crop into a seperate crop
    """
    #TODO setup photos class to store periodic photos of crop and display most recent one
    #TODO add split crop feature to split crops that need their own notes while copying all current date into new row
    #TODO add harvested button to milestone dates allowing setting of havest rating and harvest note and removing from current list
    if request.method == 'POST':
        crop = Crop.query.get_or_404(id)
        if request.form['milestone'] == 'germ':
            crop.germ_date = request.form['date']
        elif request.form['milestone'] == 'fruit':
            crop.fruit_date = request.form['date']
        elif request.form['milestone'] == 'harvest':
            crop.harvested_date = request.form['date']

        try:
            db.session.commit()
            return redirect('/crop/{}'.format(id))
        except:
            return 'There was an issue adding the crop'
    else:
        crop = Crop.query.get_or_404(id)
        today1 = date.today()
        today1 = today1.strftime("%Y-%m-%d")
        other_crops = Crop.query.filter(Crop.enviro_id==crop.enviro_id)

        return render_template('crop/manage_crop.html', crop=crop,today=today1, other_crops=other_crops)


@app.route('/delete_crop/<int:id>')
def delete_crop(id):
    """Deletes the crop related to the id sent to /delete_pin/{id}"""
    crop = Crop.query.get_or_404(id)
    try:
        db.session.delete(crop)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting the crop'


@app.route('/add_log/<int:crop_id>', methods=['POST', 'GET'])
def add_log(crop_id):
    """If there is a POST request to /add_log{crop_id}, it creates a new log row 
      associated with the crop_id passed, as a task or just a note in the database
    """
    if request.method == 'POST':
        if request.form['task'] == 'note':
            today1 = date.today()
            note_date = str(today1.strftime("%d/%m/%Y"))
            note=request.form['note']
            new_log = Log(crop_id=crop_id,note_date=note_date,note=note)
            try:
                db.session.add(new_log)
                db.session.commit()
                return redirect('/crop/{}'.format(crop_id))
            except:
                return 'There was an issue adding the log'
        else:
            task = request.form['task']
            note_date = request.form['note_date']
            note = request.form['note']
            other_crops = request.form.getlist('other_crops')
            if int(other_crops[0]) > 0:
                new_log = Log(crop_id=crop_id,note_date=note_date, task=task, note=note)
                db.session.add(new_log)
                for other_crop in other_crops:
                    id = int(other_crop)
                    new_log = Log(crop_id=id,note_date=note_date, task=task, note=note)
                    db.session.add(new_log)

            try:
                db.session.commit()
                return redirect('/crop/{}'.format(crop_id))
            except:
                return 'There was an issue adding the log'


@app.route('/delete_log/<int:id>')
def delete_log(id):
    """Deletes the log related to the id sent to /delete_log/{id}"""
    log = Log.query.get_or_404(id)
    try:
        db.session.delete(log)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting the log'


@app.route('/update_cron')
def update_cron():
    """Updates the crontab that handles running the scripts at specified times"""
    enviros = Enviro.query.filter(Enviro.active == 1)
    cron = CronTab(user=True)
    cron.remove_all(comment="hydro")
    cron.remove_all(comment="light")
    for enviro in enviros:
        light = Light.query.get_or_404(enviro.light_id)
        cycles = Cycle.query.filter(Cycle.water_id == enviro.water_id)
        if enviro.water_pump > 0:
            for cycle in cycles:
                hour = int(cycle.start_time[0:2])
                minute = int(cycle.start_time[3:5])
                job = cron.new(command='python3 /home/pi/repos/hydro_flask/water_pump.py {} {}'.format(enviro.water_pump, cycle.duration))
                job.comment = "hydro"
                job.day.every(1)
                job.hour.on(hour)
                job.minute.on(minute)
                cron.write()
        if enviro.light_outlet > 0:
            hour = int(light.start_time[0:2])
            minute = int(light.start_time[3:5])
            job1 = cron.new(command='python3 /home/pi/repos/hydro_flask/lights.py {}'.format(enviro.light_outlet))
            job1.hour.on(hour)
            job1.minute.on(minute)
            job1.comment = "light"
            
            hour = int(light.end_time[0:2])
            minute = int(light.end_time[3:5])
            job2 = cron.new(command='python3 /home/pi/repos/hydro_flask/lights.py {}'.format(enviro.light_outlet))
            job2.hour.on(hour)
            job2.minute.on(minute)
            job2.comment = "light"
            cron.write()

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
