function updateBuildData(key, value) {
    const splitKey = key.split("/");
    const id = splitKey[splitKey.length - 1];
    if (id) {
        const elem = document.getElementById(id)
        if (elem) {
            elem.innerHTML = value;

            // Check if value is dirty
            if (value.includes("-dirty")) {
                elem.style.backgroundColor = "#FFBBBB";
            } else {
                elem.style.backgroundColor = "transparent";
            }
        }
    }
}

export default updateBuildData;
