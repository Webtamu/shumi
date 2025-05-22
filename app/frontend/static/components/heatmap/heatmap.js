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

    // Data is already in format: { "YYYY-MM-DD": value }
    allData = data;
    render(currentYear);
};

const svg = d3.select("#heatmap");
let width = window.innerWidth;
let height = window.innerHeight;
svg.attr("width", width).attr("height", height);

const tooltip = d3.select("#tooltip");
const margin = { top: 80, right: 40, bottom: 40, left: 60 };
const cellSize = 15;
const dayLabels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
const colorScale = d3.scaleSequential(d3.interpolateYlOrRd)
    .domain([0, 10]);

let currentYear = new Date().getFullYear();
const yearDisplay = d3.select("#year-display");

let allData = {};

function generateYearData(year) {
    const startDate = new Date(year, 0, 1);
    const endDate = new Date(year, 11, 31);
    
    return d3.timeDays(startDate, endDate).map(date => {
        const dateStr = d3.timeFormat("%Y-%m-%d")(date);
        return {
            date,
            dateStr,
            day: date.getDay(),
            value: allData[dateStr] || 0,
            formattedDate: d3.timeFormat("%B %d, %Y")(date)
        };
    });
}

function render(year) {
    yearDisplay.text(year);
    
    svg.selectAll("*").remove();
    width = window.innerWidth;
    height = window.innerHeight;
    svg.attr("width", width).attr("height", height);

    const weeks = d3.timeWeeks(new Date(year, 0, 1), new Date(year, 11, 31));
    const weekCount = weeks.length;

    const g = svg.append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // Add day labels on the left
    dayLabels.forEach((day, i) => {
        g.append("text")
            .attr("x", -10)
            .attr("y", (i + 0.5) * (cellSize + 2))
            .attr("text-anchor", "end")
            .attr("dominant-baseline", "middle")
            .attr("font-size", 10)
            .text(day);
    });

    // Add month labels at the top
    const monthFormat = d3.timeFormat("%b");
    const monthPositions = [];
    
    // Calculate month positions
    weeks.forEach((week, weekIndex) => {
        const firstDayOfWeek = new Date(week);
        const month = firstDayOfWeek.getMonth();
        
        if (!monthPositions[month] || weekIndex < monthPositions[month].weekIndex) {
            monthPositions[month] = {
                weekIndex,
                month
            };
        }
    });

    // Draw month labels
    monthPositions.forEach((pos, month) => {
        if (pos) {
            g.append("text")
                .attr("x", (pos.weekIndex + 0.5) * (cellSize + 2))
                .attr("y", -10)
                .attr("text-anchor", "middle")
                .attr("font-size", 10)
                .text(monthFormat(new Date(year, month, 1)));
        }
    });

    // Create cells
    g.selectAll("g.week")
        .data(weeks)
        .join("g")
        .attr("class", "week")
        .attr("transform", (d, i) => `translate(${i * (cellSize + 2)},0)`)
        .selectAll("rect.day")
        .data((week, weekIndex) => {
            return dayLabels.map((_, dayIndex) => {
                const date = new Date(week);
                date.setDate(date.getDate() + dayIndex);
                const dateStr = d3.timeFormat("%Y-%m-%d")(date);
                const isValid = date.getFullYear() === year && 
                                 date.getMonth() >= 0 && date.getMonth() <= 11;
                
                return {
                    date,
                    dateStr,
                    day: dayIndex,
                    value: isValid ? (allData[dateStr] || 0) : null,
                    formattedDate: d3.timeFormat("%B %d, %Y")(date),
                    weekIndex,
                    isValid
                };
            });
        })
        .join("rect")
        .attr("class", "day")
        .attr("width", cellSize)
        .attr("height", cellSize)
        .attr("y", d => d.day * (cellSize + 2))
        .attr("fill", d => d.isValid ? colorScale(d.value) : "none")
        .attr("stroke", d => d.isValid ? "#ddd" : "none")
        .attr("stroke-width", 0.5)
        .on("mousemove", function (event, d) {
            if (!d.isValid) return;
            
            d3.select(this)
                .attr("stroke", "black")
                .attr("stroke-width", 1.5)
                .style("cursor", "pointer");

            tooltip
                .style("display", "block")
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 20) + "px")
                .html(`<strong>${d.formattedDate}</strong><br>Value: ${d.value}`);
        })
        .on("mouseleave", function (event, d) {
            if (!d.isValid) return;
            
            d3.select(this)
                .attr("stroke", "#ddd")
                .attr("stroke-width", 0.5);

            tooltip.style("display", "none");
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
}

// Navigation handlers
d3.select("#prev-year").on("click", () => {
    currentYear--;
    render(currentYear);
    if (window.pyObj) {
        pyObj.sendData(`Switched to year: ${currentYear}`);
    }
});

d3.select("#next-year").on("click", () => {
    currentYear++;
    render(currentYear);
    if (window.pyObj) {
        pyObj.sendData(`Switched to year: ${currentYear}`);
    }
});

// Initial render
render(currentYear);

// Handle window resize
window.addEventListener("resize", () => render(currentYear));