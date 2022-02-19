"use strict";
import * as $ from "jquery";
import * as d3 from "d3";

// make these packages visible to the networktables helpers, too
window.$ = $;
window.d3 = d3;

$(document).ready(function () {

    // sets a function that will be called when the websocket connects/disconnects
    NetworkTables.addWsConnectionListener(onNetworkTablesConnection, true);

    // sets a function that will be called when the robot connects/disconnects
    NetworkTables.addRobotConnectionListener(onRobotConnection, true);

    NetworkTables.addGlobalListener(swerveListener, true);
    console.log("Started")

    // attaches the select element to a SendableChooser object
    attachSelectToSendableChooser("#autonomous", "Autonomous");

    // will load a camera from the robot's IP address on port 5800
    loadCameraOnConnect({
        container: '#camera_container', // where to put the img tag
        proto: null,                    // optional, defaults to http://
        host: null,                     // optional, if null will use robot's autodetected IP address
        port: 5800,                     // webserver port
        image_url: '/?action=stream',   // mjpg stream of camera
        data_url: '/program.json',      // used to test if connection is up
        wait_img: null,                 // optional img to show when not connected, can use SVG instead
        error_img: null,                // optional img to show when error connecting, can use SVG instead
        attrs: {                        // optional: attributes set on svg or img element
            width: 640,                     // optional, stretches image to this width
            height: 480,                    // optional, stretches image to this width
        }
    });
});

function swerveListener(key, value, isNew) {
    //console.log(key)

    var canvas = document.getElementById('SwerveCanvas');
    if (canvas.getContext) {
        var lf = canvas.getContext('2d');
        var swerveDriveImage = new Image();
        swerveDriveImage.src = 'resources/swerveModule.png'

        //console.log(key, value)
        if (key == "/SmartDashboard/SwerveDrive/fp_actual") {
            lf.clearRect(0, 0, 150, 150);
            //save the untranslated/unrotated context
            lf.save();
            lf.beginPath();
            //move the rotation point to the center of the rect
            lf.translate(25 + 50 / 2, 25 + 75 / 2);
            //rotate the rect
            lf.rotate(value);
            //draw the rect on the transformed context
            //Note: after transforming [0,0] is visually [x,y]
            //so the rect needs to be offset accordingly when drawn
            lf.drawImage(swerveDriveImage, -39 / 2, -48 / 2);
            lf.fill();
            //restore the context to its untranslated/unrotated state
            lf.restore();
        }


        if (key == "/SmartDashboard/SwerveDrive/fs_actual") {
            lf.clearRect(150, 0, canvas.width, 150);
            lf.save();
            lf.beginPath();
            lf.translate(200 + 50 / 2, 25 + 75 / 2);
            lf.rotate(value);
            lf.drawImage(swerveDriveImage, -39 / 2, -48 / 2);
            lf.fill();
            lf.restore();
        }

        if (key == "/SmartDashboard/SwerveDrive/ap_actual") {
            lf.clearRect(0, 150, 150, canvas.height);
            lf.save();
            lf.beginPath();
            lf.translate(50, 300 + 75);
            lf.rotate(value);
            lf.drawImage(swerveDriveImage, -39 / 2, -48 / 2);
            lf.fill();
            lf.restore();
        }

        if (key == "/SmartDashboard/SwerveDrive/as_actual") {
            lf.clearRect(150, 150, canvas.width, canvas.height);
            lf.save();
            lf.beginPath();
            lf.translate(175 + 50, 300 + 75);
            lf.rotate(value);
            lf.drawImage(swerveDriveImage, -39 / 2, -48 / 2);
            lf.fill();
            lf.restore();
        }


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
