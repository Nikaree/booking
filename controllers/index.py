from app import app
from flask import Flask, render_template, request, session, flash, url_for, g
from werkzeug.utils import redirect
import copy
from flask_caching import Cache
from models import models
cache = Cache(app)

#функция получения ближайшего свободного времени для резервирования столика
def get_close_date():
    result_close = []
    var_result = {}
    date = models.get_date_time_booking()
    for d in date:
        temp_data = d[0]
        temp_time = d[1][:2]
        data_temp = []
        for j in date:
            if j[0] == temp_data:
                data_temp.append(j[1])
        var_result[temp_data] = data_temp

    setting = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
               '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    for value in var_result.items():
        var_sett = copy.copy(setting)
        for i in range(len(value[1])):
            if value[1][i] in var_sett:
                index = var_sett.index(value[1][i])
                if abs(index - len(value[1])) < 5:
                    del var_sett[index:index + 6]
                else:
                    del var_sett[index:]
        flag = False
        k = 0
        for i in range(len(var_sett) - 1):
            if abs(int(var_sett[i][:2]) - int(var_sett[i + 1][:2])) == 1:
                k += 1
            else:
                k = 0
        if k >= 5:
            flag = True
        if not flag:
            result_close.append(value[0])
    return result_close

#роут получения данных для отображения календаря резервированных дат
@app.route('/', methods=["POST", "GET"])
def select_date():
    # подключение к бд
    temp_data = get_close_date()
    data = {'date': temp_data}
    # обработчик нажатия на кнопку
    if request.method == "POST":
        if 'entrance' in request.form:
            date = request.form['val']
            date = date.replace('.', '')
            return redirect(url_for('booking', date=date))
        elif 'all_booking' in request.form:
            return redirect(url_for('all_booking'))
    else:
        cache.clear()
        return render_template('main.html', data=data, settings=cache.get('booking_true'))


#роут авторизации для получения данных о бронированных столиках
@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            cache.set('login', 'True')
            return redirect(url_for('all_booking'))
    return render_template('login.html')

#роут получения и отображения данных все бронирований
@app.route('/all_booking', methods=["POST", "GET"])
def all_booking():
    print('123')
    if cache.get('login') is None:
        return redirect(url_for('login'))
    else:
        return render_template('all_booking.html', all_booking=models.get_all_booking())

#роут регистрации бронирования
@app.route('/booking/<date>', methods=["POST", "GET"])
def booking(date):
    var_date = str(date[-4:]) + "-" + str(date[2:4]) + "-" + str(date[0:2])
    setting = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
               '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    block_time = models.get_block_time(var_date)
    for i in range(len(block_time)):
        if block_time[i][0] in setting:
            index = setting.index(block_time[i][0])
        
    if request.method == "POST":
        try:
            
            guest_id = models.insert_guest(request.form['fio'], request.form['number_phone'])
            place_id = models.get_place(request.form['system_kat'], request.form['dva'])
            desk_id = models.select_desk(request.form['desc_amount'], place_id)
            print(desk_id)
            var_date = str(date[-4:]) + "-" + str(date[2:4]) + "-" + str(date[0:2])
            time = request.form['time']
            amount = request.form['desc_amount']
            models.insert_booking(desk_id, guest_id, var_date, time, amount)
            cache.set('booking_true', 'True')
            return redirect('/')
        except TypeError:
            print('Ошибка типа данных')
    else:
        return render_template('librarian.html', time=setting)