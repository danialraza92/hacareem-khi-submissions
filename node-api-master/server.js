// BASE SETUP
// =============================================================================

// call the packages we need
var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var morgan = require('morgan');

// configure app
app.use(morgan('dev')); // log requests to the console

// configure body parser
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

var port = process.env.PORT || 3000; // set our port

var mysql = require('mysql');
var connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'root',
    database: 'hacareem'
});

// ROUTES FOR OUR API
// =============================================================================

// create our router
var router = express.Router();

// middleware to use for all requests
router.use(function (req, res, next) {
    // do logging
    next();
});

// test route to make sure everything is working (accessed at GET http://localhost:8080/api)
router.get('/', function (req, res) {
    res.json({message: 'Api working !!'});
});

// on routes that end in /bears
// ----------------------------------------------------
router.route('/trips')

// create a bear (accessed at POST http://localhost:8080/bears)
    .post(function (req, res) {
   
        var trip = req.body;  // set the bears name (comes from the request)
        console.log('Result : [', JSON.stringify(trip), ']');
        var post = {
             user_id: trip.userId,
			ride_id: trip.rideId,
            pick_up_time: trip.pickUpTime,
            pick_up: trip.pickup.display,
            pick_up_lat: trip.pickup.latitude,
            pick_up_lng: trip.pickup.longitude,
            pick_up_geohash: trip.pickup.geohash,
            drop_off: trip.dropoff.display,
            drop_off_lat: trip.dropoff.latitude,
            drop_off_lng: trip.dropoff.longitude,
            drop_off_geohash: trip.dropoff.geohash,
            readFlag: false
        };
        var query = connection.query('INSERT INTO trips SET ?', post, function (error, results, fields) {
            if (error) console.log(JSON.stringify(error));
            console.log("--->" + JSON.stringify(results));
            // Neat!
        });
		
        console.log(query.sql);
        /* connection.end(); */
        res.json({Response: 'Inserted into Database'});


    })

    // get all the bears (accessed at GET http://localhost:8080/api/bears)
    .get(function (req, res) {

        // connection.connect();

        connection.query('SELECT * from trips', function (error, results, fields) {
            if (error) console.log(JSON.stringify(error));
            else {
                console.log('Result : [', JSON.stringify(results), ']');
                res.json(results);
            }
        });

        // connection.end();

    });

// REGISTER OUR ROUTES -------------------------------
app.use('/api', router);

// START THE SERVER
// =============================================================================
app.listen(port);
console.log('Magic happens on port ' + port);
