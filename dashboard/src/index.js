"use strict";
import * as $ from "jquery";
import * as d3 from "d3";
import updateTemp from "./temp-display";
import { updateValue } from "./utils";
import { setupPID, receivePIDUpdate } from "./pid-optimizer";

const WHEEL_PORT_X = 25 + 50 / 2;
const WHEEL_STARBOARD_X = 200 + 50 / 2;
const WHEEL_FORE_Y = 25 + 75 / 2;
const WHEEL_AFT_Y = 200 + 75 / 2;

// make these packages visible to the networktables helpers, too
window.$ = $;
window.d3 = d3;
var canvas;
var drawingContext;

$(document).ready(function () {

    // sets a function that will be called when the websocket connects/disconnects
    NetworkTables.addWsConnectionListener(onNetworkTablesConnection, true);

    // sets a function that will be called when the robot connects/disconnects
    NetworkTables.addRobotConnectionListener(onRobotConnection, true);

    NetworkTables.addGlobalListener(swerveListener, true);

    // attaches the select element to a SendableChooser object
    attachSelectToSendableChooser("#autonomous", "Autonomous");

    // will load a camera from the robot's IP address on port 5800
    loadCameraOnConnect({
        container: '#camera_container', // where to put the img tag
        proto: null,                    // optional, defaults to http://
        host: "10.17.21.11",                     // optional, if null will use robot's autodetected IP address
        port: 5801,                     // webserver port
        image_url: '/video',   // mjpg stream of camera
        data_url: '/',      // used to test if connection is up
        wait_img: 'resources/no_signal.png',                 // optional img to show when not connected, can use SVG instead
        error_img: 'resources/error.png',                // optional img to show when error connecting, can use SVG instead
        attrs: {                        // optional: attributes set on svg or img element
            width: 320,                     // optional, stretches image to this width
            height: 240,                    // optional, stretches image to this width
        }
    });

    canvas = document.getElementById('SwerveCanvas');
    if (canvas.getContext) {
        // draw initial wheels
        drawingContext = canvas.getContext('2d');
        drawModule(WHEEL_PORT_X, WHEEL_FORE_Y, 0, 0);
        drawModule(WHEEL_STARBOARD_X, WHEEL_FORE_Y, 0, 0);
        drawModule(WHEEL_PORT_X, WHEEL_AFT_Y, 0, 0);
        drawModule(WHEEL_STARBOARD_X, WHEEL_AFT_Y, 0, 0);
    }

    setupPID();
});

function drawModule(x, y, real_angle, target_angle) {
    if (drawingContext) {
        drawingContext.clearRect(x - 75, y - 75, 150, 150);
        //save the untranslated/unrotated context
        drawingContext.save();
        drawingContext.beginPath();
        //move the rotation point to the center of the rect
        drawingContext.translate(x, y);
        //rotate the rect
        drawingContext.rotate(real_angle);
        //draw the rect on the transformed context
        //Note: after transforming [0,0] is visually [x,y]
        //so the rect needs to be offset accordingly when drawn
        drawingContext.drawImage(swerveDriveImage, -39 / 2, -48 / 2);
        drawingContext.fill();
        //restore the context to its untranslated/unrotated state
        drawingContext.restore();

        // The same again for the target
        drawingContext.save();
        drawingContext.beginPath();
        drawingContext.translate(x, y);
        drawingContext.rotate(target_angle);
        drawingContext.drawImage(swerveReticleImage, -39 / 2, -85 / 2);
        drawingContext.fill();
        drawingContext.restore();
    }
}

var swerveDriveImage = new Image();
swerveDriveImage.src = 'resources/swerveModule.png'

var swerveReticleImage = new Image();
swerveReticleImage.src = 'resources/swerveReticle.png'
function swerveListener(key, value, isNew) {
    // console.log(key)
    if (key.includes("/SmartDashboard/SwerveDrive/fp_")) {
        drawModule(WHEEL_PORT_X, WHEEL_FORE_Y, NetworkTables.getValue("/SmartDashboard/SwerveDrive/fp_actual"), NetworkTables.getValue("/SmartDashboard/SwerveDrive/fp_target"));
    }
    if (key.includes("/SmartDashboard/SwerveDrive/fs_")) {
        drawModule(WHEEL_STARBOARD_X, WHEEL_FORE_Y, NetworkTables.getValue("/SmartDashboard/SwerveDrive/fs_actual"), NetworkTables.getValue("/SmartDashboard/SwerveDrive/fs_target"));
    }
    if (key.includes("/SmartDashboard/SwerveDrive/ap_")) {
        drawModule(WHEEL_PORT_X, WHEEL_AFT_Y, NetworkTables.getValue("/SmartDashboard/SwerveDrive/ap_actual"), NetworkTables.getValue("/SmartDashboard/SwerveDrive/ap_target"));
    }
    if (key.includes("/SmartDashboard/SwerveDrive/as_")) {
        drawModule(WHEEL_STARBOARD_X, WHEEL_AFT_Y, NetworkTables.getValue("/SmartDashboard/SwerveDrive/as_actual"), NetworkTables.getValue("/SmartDashboard/SwerveDrive/as_target"));
    }

    if (key.includes("/SmartDashboard/Thermals/")) {
        updateTemp(key, value);
    }
    if (key.includes("/SmartDashboard/PID/")) {
        receivePIDUpdate(key, value);
    }
}

function onRobotConnection(connected) {
    $('#robotstate').text(connected ? "Connected!" : "Disconnected");
    $('#robotAddress').text(connected ? NetworkTables.getRobotAddress() : "disconnected");
}

function onNetworkTablesConnection(connected) {

    if (connected) {
        $("#connectstate").text("Connected!");

        // clear the table
        $("#nt tbody > tr").remove();

        console.log(NetworkTables.getKeys())

    } else {
        $("#connectstate").text("Disconnected!");
    }
}
