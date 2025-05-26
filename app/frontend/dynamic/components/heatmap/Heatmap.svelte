<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  export let data = {};

  let currentYear = new Date().getFullYear();
  let allData = {};

  let width = window.innerWidth;
  let height = window.innerHeight;

  let svgEl;
  let tooltipEl;

  const margin = { top: 80, right: 40, bottom: 40, left: 60 };
  const cellSize = 15;
  const dayLabels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  const colorScale = d3.scaleSequential(d3.interpolateYlOrRd).domain([0, 10]);
  const monthFormat = d3.timeFormat("%b");
  const dateFormat = d3.timeFormat("%Y-%m-%d");
  const formattedDateFormat = d3.timeFormat("%B %d, %Y");

  onMount(() => {
    // QWebChannel initialization
    if (window.QWebChannel) {
      new QWebChannel(qt.webChannelTransport, function(channel) {
        window.pyObj = channel.objects.pyObj;
        pyObj.initializeComponent('Heatmap initialized');
      });
    }

    // Window resize listener
    window.addEventListener('resize', onResize);

    // Expose global function for receiving data from Python
    window.receiveDataFromPython = (incomingData) => {
      if (typeof incomingData === 'string') {
        try {
          incomingData = JSON.parse(incomingData);
        } catch (e) {
          console.error("Could not parse JSON string:", e);
          return;
        }
      }
      allData = incomingData;
      drawHeatmap();
    };

    initSvg();
    drawHeatmap();

    return () => window.removeEventListener('resize', onResize);
  });

  function onResize() {
    width = window.innerWidth;
    height = window.innerHeight;
    initSvg();
    drawHeatmap();
  }

  // Whenever data prop changes from outside, update allData and redraw
  $: if (data) {
    allData = data;
    drawHeatmap();
  }

  function initSvg() {
    const svg = d3.select(svgEl);
    svg.selectAll("*").remove();
    svg.attr("width", width).attr("height", height);
    svg.append("g").attr("class", "main-group").attr("transform", `translate(${margin.left},${margin.top})`);
  }

  function generateWeeks(year) {
    // Generate weeks starting from Jan 1 to Jan 1 next year
    return d3.timeWeeks(new Date(year, 0, 1), new Date(year + 1, 0, 1));
  }

  function drawHeatmap() {
    if (!svgEl || !allData) return;

    const svg = d3.select(svgEl);
    const g = svg.select("g.main-group");
    g.selectAll("*").remove();

    // Draw day labels
    dayLabels.forEach((day, i) => {
      g.append("text")
        .attr("x", -10)
        .attr("y", (i + 0.5) * (cellSize + 2))
        .attr("text-anchor", "end")
        .attr("dominant-baseline", "middle")
        .attr("font-size", 10)
        .text(day);
    });

    const weeks = generateWeeks(currentYear);
    const monthPositions = [];

    // Find first week index for each month
    weeks.forEach((weekDate, i) => {
      const month = weekDate.getMonth();
      if (!monthPositions[month] || i < monthPositions[month].weekIndex) {
        monthPositions[month] = { weekIndex: i, month };
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
          .text(monthFormat(new Date(currentYear, month, 1)));
      }
    });

    // Draw week groups with day cells
    const weekGroups = g.selectAll("g.week")
      .data(weeks)
      .join("g")
      .attr("class", "week")
      .attr("transform", (d, i) => `translate(${i * (cellSize + 2)},0)`);

    weekGroups.selectAll("rect.day")
      .data((weekDate, weekIndex) => {
        return dayLabels.map((_, dayIndex) => {
          const date = new Date(weekDate);
          date.setDate(date.getDate() + dayIndex);
          const dateStr = dateFormat(date);
          const isValid = date.getFullYear() === currentYear;
          return {
            date,
            dateStr,
            day: dayIndex,
            value: isValid ? (allData[dateStr] || 0) : null,
            formattedDate: formattedDateFormat(date),
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
      .on("mousemove", (event, d) => {
        if (!d.isValid) return;
        d3.select(event.currentTarget)
          .attr("stroke", "black")
          .attr("stroke-width", 1.5)
          .style("cursor", "pointer");

        tooltipEl.style.display = "block";
        tooltipEl.innerHTML = `<strong>${d.formattedDate}</strong><br>Value: ${d.value}`;
        tooltipEl.style.left = `${event.pageX + 10}px`;
        tooltipEl.style.top = `${event.pageY - 20}px`;
      })
      .on("mouseleave", (event, d) => {
        if (!d.isValid) return;
        d3.select(event.currentTarget)
          .attr("stroke", "#ddd")
          .attr("stroke-width", 0.5);

        tooltipEl.style.display = "none";
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

    // Update year display (needed because year can change)
    yearDisplay = currentYear;
  }

  function prevYear() {
    currentYear -= 1;
    drawHeatmap();
    if (window.pyObj) pyObj.sendData(`Switched to year: ${currentYear}`);
  }

  function nextYear() {
    currentYear += 1;
    drawHeatmap();
    if (window.pyObj) pyObj.sendData(`Switched to year: ${currentYear}`);
  }

  // For displaying the current year in UI
  let yearDisplay = currentYear;

</script>

<style>
  :global(body, html) {
    margin: 0;
    padding: 0;
    overflow: hidden;
    height: 100%;
    width: 100%;
    font-family: sans-serif;
  }
  .tooltip {
    position: absolute;
    pointer-events: none;
    background: rgba(0,0,0,0.7);
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    white-space: nowrap;
    z-index: 1000;
    display: none;
  }
  .nav-container {
    position: absolute;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    gap: 20px;
    z-index: 10;
  }
  .nav-button {
    background: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 5px 10px;
    cursor: pointer;
    font-size: 16px;
  }
  .nav-button:hover {
    background: #e0e0e0;
  }
  .year-display {
    font-size: 18px;
    font-weight: bold;
  }
</style>

<div class="nav-container">
  <button class="nav-button" on:click={prevYear}>&lt;</button>
  <div class="year-display">{yearDisplay}</div>
  <button class="nav-button" on:click={nextYear}>&gt;</button>
</div>

<svg bind:this={svgEl} id="heatmap"></svg>
<div class="tooltip" bind:this={tooltipEl}></div>
