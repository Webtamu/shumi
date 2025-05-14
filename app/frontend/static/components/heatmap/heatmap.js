window.onload = function () {
    new QWebChannel(qt.webChannelTransport, function(channel) {
        window.pyObj = channel.objects.pyObj;
        pyObj.sendData('Heatmap initialized');
    });
};

const svg = d3.select("#heatmap");
let width = window.innerWidth;
let height = window.innerHeight;
svg.attr("width", width).attr("height", height);

const tooltip = d3.select("#tooltip");
const margin = { top: 40, right: 20, bottom: 20, left: 30 };
const cellSize = 15;
const dayLabels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const colorScale = d3.scaleSequential(d3.interpolateYlGn)
    .domain([0, 10]);

function generateHeatmapData() {
    const startDate = d3.timeDay.offset(new Date(), -365);
    const data = d3.timeDays(startDate, new Date()).map(date => ({
        date,
        value: Math.floor(Math.random() * 10)
    }));
    return data;
}

let data = generateHeatmapData();

function render(data) {
    svg.selectAll("*").remove();
    width = window.innerWidth;
    height = window.innerHeight;
    svg.attr("width", width).attr("height", height);

    const weeks = d3.groups(data, d => d3.timeWeek.count(d3.timeYear(d.date), d.date));

    const g = svg.append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    g.selectAll("g")
        .data(weeks)
        .join("g")
        .attr("transform", (d, i) => `translate(${i * (cellSize + 2)},0)`)
        .selectAll("rect")
        .data(d => d[1])
        .join("rect")
        .attr("width", cellSize)
        .attr("height", cellSize)
        .attr("y", d => d.date.getDay() * (cellSize + 2))
        .attr("fill", d => colorScale(d.value))
        .on("mousemove", function (event, d) {

            d3.select(this)
                .attr("stroke", "black")
                .attr("stroke-width", 1.5)
                .style("cursor", "pointer");

            tooltip
                .style("display", "block")
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 20) + "px")
                .html(`<strong>${d3.timeFormat("%B %d, %Y")(d.date)}</strong><br>${d.value} commits`);
        })
        .on("mouseleave", function () {
            d3.select(this)
                .attr("stroke", "none");
    
            tooltip.style("display", "none");
        })
        .on("click", (event, d) => {
            if (window.pyObj) {
                const cellData = {
                    date: d.formattedDate,
                    day: d.day,
                    value: d.value,
                    weekNumber: d3.timeWeek.count(d3.timeYear(d.date), d.date),
                    year: d.date.getFullYear()
                };
                pyObj.sendData(JSON.stringify(cellData));
            }
        });
}

function updateData() {
    data = generateHeatmapData();
    render(data);
    pyObj.sendData(`Updated Heatmap Data from JS: ${JSON.stringify(data)}`);
}

window.addEventListener("resize", () => render(data));

render(data);
