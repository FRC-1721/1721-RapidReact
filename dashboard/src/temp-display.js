const RED_TEMP = 80;
const YELLOW_TEMP = 60;
const RED = "#FFBBBB"
const YELLOW = "#FFE900"
function updateTemp(key, value) {
    const splitKey = key.split("/");
    const id = splitKey[splitKey.length - 1];
    if (id) {
        const elem = document.getElementById(id)
        if (elem) {
            elem.innerHTML = `${value} C`;
            if (value > RED_TEMP) {
                elem.style.backgroundColor = RED;
            } else if (value > YELLOW_TEMP) {
                elem.style.backgroundColor = YELLOW;
            } else {
                elem.style.backgroundColor = "transparent";
            }
        }
    }
}

export default updateTemp;
