
window.onload = function () {
    new QWebChannel(qt.webChannelTransport, function(channel) {
        window.pyObj = channel.objects.pyObj;
        pyObj.sendData('Bar Chart initialized');
    });
};

window.receiveDataFromPython = function(data) {
    console.log(data);
    if (typeof data === 'string') {
        data = JSON.parse(data);
    }
    updateChartWithExternalData(data);

};


const svg = d3.select("#chart");
let width = window.innerWidth;
let height = window.innerHeight;
svg.attr("width", width).attr("height", height);

const margin = { top: 30, right: 30, bottom: 40, left: 50 };
const xScale = d3.scaleBand().padding(0.1).range([margin.left, width - margin.right]);
const yScale = d3.scaleLinear().range([height - margin.bottom, margin.top]);
const colorScale = d3.scaleSequential(d3.interpolateBlues);

const tooltip = d3.select("#tooltip");

function generateDummyData() {
    return Array.from({ length: 24 }, (_, i) => ({
        hour: i,
        value: Math.floor(Math.random() * 100),
    }));
}

let data = generateDummyData();

function render(data) {
    xScale.range([margin.left, width - margin.right]);
    yScale.range([height - margin.bottom, margin.top]);

    xScale.domain(data.map(d => d.hour));
    const maxVal = d3.max(data, d => d.value);
    yScale.domain([0, maxVal]);
    colorScale.domain([0, maxVal]);

    svg.selectAll(".x-axis").data([null]).join("g")
        .attr("class", "x-axis")
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .transition()
        .call(d3.axisBottom(xScale).tickFormat(d => `${d}:00`).tickSizeOuter(0));

    svg.selectAll(".y-axis").data([null]).join("g")
        .attr("class", "y-axis")
        .attr("transform", `translate(${margin.left},0)`)
        .transition()
        .call(d3.axisLeft(yScale));

    const bars = svg.selectAll(".bar").data(data, d => d.hour);

    bars.join(
        enter => enter.append("rect")
            .attr("class", "bar")
            .attr("x", d => xScale(d.hour))
            .attr("width", xScale.bandwidth())
            .attr("y", d => yScale(d.value))
            .attr("height", d => Math.max(0, yScale(0) - yScale(d.value)))
            .attr("fill", d => colorScale(d.value))
            .on("mousemove", (event, d) => {
                tooltip
                    .style("display", "block")
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 20) + "px")
                    .html(`<strong>${d.hour}:00</strong><br>${d.value} reviews, session ${d.session_id}`);
            })
            .on("mouseleave", () => tooltip.style("display", "none"))
            .on("click", (event, d) => {
                if (window.pyObj) {
                    const barData = {
                        hour: d.hour,
                        value: d.value,
                        session_id: d.session_id,
                    };
                    pyObj.sendData(JSON.stringify(barData));
                }
            })
            .transition()
            .duration(800)
            .attr("y", d => yScale(d.value))
            .attr("height", d => Math.max(0, yScale(0) - yScale(d.value))),

        update => update
            .transition()
            .duration(800)
            .attr("x", d => xScale(d.hour))
            .attr("width", xScale.bandwidth())
            .attr("y", d => yScale(d.value))
            .attr("height", d => Math.max(0, yScale(0) - yScale(d.value)))
            .attr("fill", d => colorScale(d.value)),

        exit => exit
            .transition()
            .duration(400)
            .attr("y", yScale(0))
            .attr("height", 0)
            .remove()
    );
}


function updateChartWithExternalData(newData) {
    console.log("Updating chart with:", newData);
    if (newData.data) {
        data = newData.data;
        render(data);
    }
}

function updateData() {
    data = generateDummyData();
    render(data);
    const dataString = JSON.stringify(data);
    pyObj.sendData(`Updated Data from JS: ${dataString}`);
}

window.addEventListener("resize", () => {
    width = window.innerWidth;
    height = window.innerHeight;
    svg.attr("width", width).attr("height", height);
    xScale.range([margin.left, width - margin.right]);
    yScale.range([height - margin.bottom, margin.top]);
    render(data);
});

render(data);
