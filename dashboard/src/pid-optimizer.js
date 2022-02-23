const ids = [
    "kp",
    "ki",
    "kd",
    "ff",
    "maxI",
    "min",
    "max"
];
const subsystems = ["primary_yoke", "off"];
var selectedSubsystem = "off";
const lastValues = {};
var graphData = []
// set the dimensions and margins of the graph
const GRAPH_MARGIN = {top: 12, right: 12, bottom: 12, left: 36};
var graphWidth, graphHeight;
var svg;

function updateOnChange(e) {
    const id = e.target.id;
    if (e.target.value !== lastValues[id] && selectedSubsystem !== "off") {
        // value was changed and system is on. Push the new value
        const key = `/SmartDashboard/PID/${selectedSubsystem}_${id}`
        const numVal = parseFloat(e.target.value, 10);
        NetworkTables.putValue(key, numVal);
        lastValues[id] = numVal;
        // and reset our graph in preparation for the new info
        restartPIDGraph()
    }
}
export function setupPID() {
    // watch for change on the P, I, and D values.
    // Put the result
    setupPIDGraph();
    for (const id of ids)  {
        const elem = document.getElementById(id)
        if (elem) {
            elem.addEventListener("blur", updateOnChange);
        }
    }
    $("#pid_subsystem").change(function (e) {
        selectedSubsystem = e.target.value;
        NetworkTables.putValue("/SmartDashboard/PID/subsystem", selectedSubsystem);
        if (selectedSubsystem !== "off") {
            restartPIDGraph();
        }
    });
    $("#pid_graph_reset").click(restartPIDGraph);
}

export function receivePIDUpdate(key, value) {
    // handle incoming updates to the network table
    if (key.includes("/SmartDashboard/PID/")) {
        // always handle graphing data
        const lastSection = key.split("/").pop();
        if (lastSection === "graph_data") {
            graphData = formatGraphData(value);
            updatePIDGraph()
        }
        // then only watch for PID values that match our current selected
        // subsystem, for examplle "primary_yoke"
        if (lastSection.includes(selectedSubsystem)) {
            const splitKey = lastSection.split("_");
            // we use the text after the last underscore in the key as the id
            // of the element on the screen to update
            const id = splitKey[splitKey.length - 1];
            if (id) {
                const numVal = parseFloat(value, 10);
                lastValues[id] = numVal;
                const elem = document.getElementById(id);
                if (elem) {
                    elem.innerHTML = `${value}`;
                }
            }
        }
    }
}

export function setupPIDGraph() {
    // find our graphing area and append the svg object to the body of the page
    const elem = $("#pid_graph_spacer")
    const width = elem.innerWidth()
    const height = elem.innerHeight()
    graphWidth = width - GRAPH_MARGIN.left - GRAPH_MARGIN.right
    graphHeight = height - GRAPH_MARGIN.top - GRAPH_MARGIN.bottom
    svg = d3.select("#pid_graph")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + GRAPH_MARGIN.left + "," + GRAPH_MARGIN.top + ")");
}

function formatGraphData(networkData) {
    var n = networkData.length
    if (n % 2 === 1) {
        networkData.pop()
        n = networkData.length
    }
    const result = [];
    for (let i = 0; i < n; i += 2) {
        const time = networkData[i];
        const error = networkData[i+1];
        result.push({
            time: time,
            error: error
        });
    }
    return result;
}

function restartPIDGraph() {
    // reset the graph
    // NOTE that you cannot put an empty array because it has to be able to
    // guess a type (Double or string). This is the best we can do for resetting
    NetworkTables.putValue("/SmartDashboard/PID/graph_data", [0, 0]);
    graphData = [];
    updatePIDGraph();
}

function updatePIDGraph () {
    // clear the graph
    svg.selectAll('*')?.remove();

    // Add X axis --> it is a date format
    var x = d3.scaleLinear()
        .domain(d3.extent(graphData, function(d) { return d.time; }))
        .range([ 0, graphWidth ]);
    svg.append("g")
        .attr("transform", "translate(0," + graphHeight/2 + ")")
        .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
        .domain(d3.extent(graphData, function(d) { return d.error; }))
        .range([ graphHeight, 0 ]);
    svg.append("g")
        .call(d3.axisLeft(y));

    svg.append("path")
       .datum(graphData)
       .attr("fill", "none")
       .attr("stroke", "#94221A")
       .attr("stroke-width", 1)
       .attr("d", d3.line()
           .x(d => x(d.time))
           .y(d => y(d.error))
   );

   // add a dot for each measure
   svg
      .append("g")
      .selectAll("dot")
      .data(graphData)
      .enter()
      .append("circle")
        .attr("cx", d => x(d.time) )
        .attr("cy", d => y(d.error) )
        .attr("r", 3)
        .attr("fill", "#94221A")
}
