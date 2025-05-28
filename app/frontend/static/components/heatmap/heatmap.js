window.onload = function () {
    new QWebChannel(qt.webChannelTransport, function(channel) {
        window.pyObj = channel.objects.pyObj;
        pyObj.initializeComponent('Heatmap initialized');
    });
};

window.receiveDataFromPython = function(data) {
    console.log("Received raw session data:", data);

    if (typeof data === 'string') {
        try {
            data = JSON.parse(data);
        } catch (e) {
            console.error("Could not parse JSON string:", e);
            return;
        }
    }

    allData = data;
    render(currentYear);
};

const svg = d3.select("#heatmap");
let width = window.innerWidth;
let height = window.innerHeight;
svg.attr("width", width).attr("height", height);

const videoTooltip = d3.select("#video-tooltip");
const videoEl = document.getElementById("tooltip-video");
const tooltipDate = document.getElementById("tooltip-date");
const tooltipValue = document.getElementById("tooltip-value");
const dayLabels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
const colorScale = d3.scaleSequential(d3.interpolateYlOrRd).domain([0, 10]);

let currentYear = new Date().getFullYear();
let allData = {};
let g = svg.append("g");

let userInteracted = false;

// Track user interaction (any click counts)
document.addEventListener('click', () => {
    userInteracted = true;
});

function render(year) {
    width = window.innerWidth;
    height = window.innerHeight;
    svg.attr("width", width).attr("height", height);

    const allWeeks = d3.timeWeeks(new Date(year, 0, 1), new Date(year, 11, 31));
    const totalWeekCount = allWeeks.length;

    const margin = { top: 30, right: 20, bottom: 20, left: 40 };
    const gridSpacing = 2;

    // Determine cell size based on vertical space
    const cellSize = Math.floor(
        (height - margin.top - margin.bottom - (7 - 1) * gridSpacing) / 7
    );

    // Calculate how many weeks can fit horizontally
    const maxVisibleWeeks = Math.floor(
        (width - margin.left - margin.right + gridSpacing) / (cellSize + gridSpacing)
    );

    // Center around middle of the year if not all weeks fit
    let weeks;
    if (maxVisibleWeeks < totalWeekCount) {
        const mid = Math.floor(totalWeekCount / 2);
        const start = Math.max(0, mid - Math.floor(maxVisibleWeeks / 2));
        weeks = allWeeks.slice(start, start + maxVisibleWeeks);
    } else {
        weeks = allWeeks;
    }

    const weekCount = weeks.length;

    const heatmapWidth = weekCount * (cellSize + gridSpacing) - gridSpacing;
    const heatmapHeight = 7 * (cellSize + gridSpacing) - gridSpacing;

    const offsetX = (width - heatmapWidth) / 2;
    const offsetY = (height - heatmapHeight) / 2;

    g.transition().duration(500)
        .attr("transform", `translate(${offsetX},${offsetY})`);

    const weekGroups = g.selectAll("g.week")
        .data(weeks, d => d);

    const weekEnter = weekGroups.enter()
        .append("g")
        .attr("class", "week");

    weekGroups.merge(weekEnter)
        .transition().duration(500)
        .attr("transform", (d, i) => `translate(${i * (cellSize + gridSpacing)}, 0)`);

    const labels = g.selectAll("text.day-label").data(dayLabels);
    labels.enter()
        .append("text")
        .attr("class", "day-label")
        .attr("x", -8)
        .attr("text-anchor", "end")
        .attr("dominant-baseline", "middle")
        .attr("font-size", 10)
        .merge(labels)
        .transition().duration(500)
        .attr("y", (d, i) => (i + 0.5) * (cellSize + gridSpacing))
        .text(d => d);

    weekGroups.merge(weekEnter).each(function(week, weekIndex) {
        const cells = d3.select(this).selectAll("rect.day")
            .data(dayLabels.map((_, dayIndex) => {
                const date = new Date(week);
                date.setDate(date.getDate() + dayIndex);
                const dateStr = d3.timeFormat("%Y-%m-%d")(date);
                const isValid = date.getFullYear() === year;

                return {
                    date,
                    dateStr,
                    day: dayIndex,
                    value: isValid ? (allData[dateStr] || 0) : null,
                    formattedDate: d3.timeFormat("%B %d, %Y")(date),
                    weekIndex,
                    isValid
                };
            }), d => d.dateStr);

        const cellsEnter = cells.enter().append("rect")
            .attr("class", "day")
            .attr("fill", d => d.isValid ? colorScale(d.value) : "none")
            .attr("stroke", d => d.isValid ? "#ddd" : "none")
            .attr("stroke-width", 0.5)
            .on("mouseover", function (event, d) {
                if (!d.isValid) return;
            
                d3.select(this)
                    .attr("stroke", "black")
                    .attr("stroke-width", 1.5)
                    .style("cursor", "pointer");
            
                tooltipDate.textContent = d.formattedDate;
                tooltipValue.textContent = `Count: ${d.value}`;
            
                videoTooltip.style("display", "block");
                videoEl.currentTime = 10;
                videoEl.play();
            })
            .on("mousemove", function (event, d) {
                if (!d.isValid) return;
            
                const tooltipWidth = videoTooltip.node().offsetWidth;
                const tooltipHeight = videoTooltip.node().offsetHeight;
                const padding = 20;
            
                const mouseX = event.pageX;
                const mouseY = event.pageY;
            
                // Position horizontally (left or right of cursor)
                let left;
                if (mouseX + tooltipWidth + padding > window.innerWidth) {
                    left = mouseX - tooltipWidth - padding; // left side
                } else {
                    left = mouseX + padding; // right side
                }
            
                // Position vertically (centered on mouseY)
                let top = mouseY - tooltipHeight / 2;
            
                // Clamp vertically within bounds
                if (top < padding) {
                    top = padding;
                } else if (top + tooltipHeight > window.innerHeight - padding) {
                    top = window.innerHeight - tooltipHeight - padding;
                }
            
                videoTooltip
                    .style("left", `${left}px`)
                    .style("top", `${top}px`);
            })
            .on("mouseout", function (event, d) {
                if (!d.isValid) return;
                d3.select(this)
                    .attr("stroke", "#ddd")
                    .attr("stroke-width", 0.5);
            
                videoTooltip.style("display", "none");
                videoEl.pause();
                videoEl.currentTime = 0;
            })
            
            .on("click", (event, d) => {
                if (!d.isValid || !window.pyObj) return;
                const cellData = {
                    date: d.formattedDate,
                    day: dayLabels[d.day],
                    value: d.value,
                    weekNumber: d.weekIndex + 1,
                    year: d.date.getFullYear()
                };
                pyObj.sendData(JSON.stringify(cellData));
            });

        cells.merge(cellsEnter)
            .transition().duration(500)
            .attr("width", cellSize)
            .attr("height", cellSize)
            .attr("y", d => d.day * (cellSize + gridSpacing))
            .attr("fill", d => d.isValid ? colorScale(d.value) : "none")
            .attr("stroke", d => d.isValid ? "#ddd" : "none");

        cells.exit().remove();
    });

    weekGroups.exit().remove();
}

// Initial render
render(currentYear);

// Smooth resize
let resizeTimeout;
window.addEventListener("resize", () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => render(currentYear), 150);
});