import db

def delete():
    conn = db.get_db().cursor()
    conn.execute("DELETE FROM BOOKING")
    
    
def get_date_time_booking():
    conn = db.get_db().cursor()
    date = conn.execute("SELECT BOOKING_DATE, BOOKING_TIME FROM BOOKING;").fetchall()
    return date

def get_all_booking():
    conn = db.get_db().cursor()
    all_booking = conn.execute("SELECT BOOKING_DATE, BOOKING_TIME, G.GUEST_NAME, D.DESK_AMOUNT, D.DESK_NUMB "
                               "FROM BOOKING B JOIN GUEST G ON B.GUEST_ID = G.GUEST_ID "
                               "JOIN DESK D ON B.DESK_ID = D.DESK_ID").fetchall()
    return all_booking

def insert_guest(fio, number_phone):
    conn = db.get_db().cursor()
    conn.execute('INSERT INTO GUEST (guest_name, guest_phone) VALUES (?, ?)', (fio, number_phone))
    db.get_db().commit()
    guest_id = conn.execute('SELECT GUEST_ID FROM GUEST WHERE GUEST_NAME = ? '
                            'AND GUEST_PHONE = ?', (fio, number_phone)).fetchone()
    return guest_id[0]


def get_place(place_floor, place_window):
    conn = db.get_db().cursor()
    place_id = conn.execute('SELECT PLACE_ID FROM PLACE WHERE PLACE_FLOOR = ? AND '
                            'PLACE_WINDOW = ?', (place_floor, place_window)).fetchone()
    return place_id[0]


def select_desk(desk_amount, place_id):
    conn = db.get_db().cursor()
    desc_id = conn.execute('SELECT DESk_ID FROM BOOKING WHERE DESk_ID = ? '
                          , (desk_amount)).fetchone()
    if desc_id is None:
        desk_amount += 1
        desc_id = conn.execute('SELECT DESk_ID FROM DESk WHERE DESk_AMOUNT = ? '
                               'AND PLACE_ID = ?', (desk_amount, place_id)).fetchone()
    return desc_id[0]


def insert_booking(desc_id, quest_id, date, time, amount):
    conn = db.get_db().cursor()
    conn.execute(' INSERT INTO BOOKING (DESK_ID,GUEST_ID,schedule_id,BOOKING_DATE,BOOKING_TIME, BOOKING_AMOUNT) VALUES '
                 ' (?,?,?,?,?,?) ' , (desc_id, quest_id, 1, date, time, amount))
    db.get_db().commit()

def get_block_time(var_date):
    conn = db.get_db().cursor()
    data = conn.execute('SELECT booking_time from booking where booking_date = ?', (var_date,)).fetchall()
    return data




