const RED = "#FFBBBB"
const GREEN = "#abfc8d"
const KHAN = "#fff985"
const JOE = "#85e0ff"
const KEEGAN = "#89ff85"
const JACK = "#ff85f9"

function updateBuildData(key, value) {
    const splitKey = key.split("/");
    const id = splitKey[splitKey.length - 1];
    if (id) {
        const elem = document.getElementById(id)
        if (elem) {
            elem.innerHTML = value;

            // Check if value is dirty
            if (value.includes("-dirty")) {
                elem.style.backgroundColor = RED;
            } else if (value.includes("joe")) {
                elem.style.backgroundColor = JOE;
            } else if (value.includes("khan")) {
                elem.style.backgroundColor = KHAN;
            } else if (value.includes("kredcool")) {
                elem.style.backgroundColor = KEEGAN;
            } else if (value.includes("jack")) {
                elem.style.backgroundColor = JACK;
            } else if (value.includes("HEAD")) {
                elem.style.backgroundColor = GREEN;
            } else {
                elem.style.backgroundColor = "transparent";
            }
        }
    }
}

export default updateBuildData;
