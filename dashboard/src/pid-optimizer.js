import { updateValue } from "./utils";
const ids = [
    "p_value",
    "i_value",
    "d_value"
];
const lastValues = {};

function updateOnChange(e) {
    const id = e.target.id;
    if (e.target.value !== lastValues[id]) {
        // value was changed
        const key = `/SmartDashboard/PID/${id}`
        const numVal = parseFloat(e.target.value, 10);
        NetworkTables.putValue(key, numVal);
    }
}
export function setupPID() {
    // watch for change on the P, I, and D values.
    // Put the result
    for (const id of ids)  {
        const elem = documnt.getElementById(id)
        if (elem) {
            elem.addEventListener("blur", updateOnChange);
        }
    }
}

export function receivePIDUpdate(key, value) {
    const splitKey = key.split("/");
    const id = splitKey[splitKey.length - 1];
    lastValues[id] = value;
    updateValue(key, value);
}
