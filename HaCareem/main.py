from bottle import route, run, request
import ml, json

@route('/bookingDropoff', method='GET')
def booking_dropoff_prediction():
    user_id = request.query.user_id
    pickup_time = request.query.pickup_time
    pickup_lat = request.query.pickup_lat
    pickup_long = request.query.pickup_long

    print(user_id)
    print(pickup_time)
    print(pickup_lat)
    print(pickup_long)

    return { "success" : True, "dropoffLocations" : json.dumps(ml.predict(user_id, pickup_time, pickup_lat, pickup_long)) }

if __name__ == "__main__":
    run(host='0.0.0.0', port=3080, debug=True)
