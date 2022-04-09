const RED = "#FFBBBB"
const KHAN = "#fcec03"
const JOE = "#03fce3"
const KEEGAN = "#1c03fc"
const JACK = "#fc03c6"

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
            } else if (value.includes("keegan")) {
                elem.style.backgroundColor = KEEGAN;
            } else if (value.includes("jack")) {
                elem.style.backgroundColor = JACK;
            } else {
                elem.style.backgroundColor = "transparent";
            }
        }
    }
}

export default updateBuildData;
