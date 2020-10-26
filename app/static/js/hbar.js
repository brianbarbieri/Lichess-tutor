const d3 = window.d3

function groupData (data, total) {
    // use scale to get percent values
    const percent = d3.scaleLinear()
      .domain([0, total])
      .range([0, 100])
    // filter out data that has zero values
    // also get mapping for next placement
    // (save having to format data for d3 stack)
    let cumulative = 0
    const _data = data.map(d => {
      cumulative += d.value
      return {
        value: d.value,
        // want the cumulative to prior value (start of rect)
        cumulative: cumulative - d.value,
        label: d.label,
        percent: percent(d.value)
      }
    }).filter(d => d.value > 0)
    return _data
  }

function stackedBar (bind, data, config) {
  config = {
    f: d3.format(".1f"),
    margin: {top: 20, right: 10, bottom: 20, left: 10},
    width: 500,
    height: 50,
    barHeight: 35,
    colors: ["#4daf4a", "#377eb8", "#e41a1c"],
    ...config
  }
  const { f, margin, width, height, barHeight, colors } = config
  const w = width - margin.left - margin.right
  const h = height - margin.top - margin.bottom
  const halfBarHeight = barHeight / 2

  const total = d3.sum(data, d => d.value)
  const _data = groupData(data, total)

  // set up scales for horizontal placement
  const xScale = d3.scaleLinear()
    .domain([0, total])
    .range([0, w])

  // create svg in passed in div
  const selection = d3.select(bind)
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

  // stack rect for each data value
  selection.selectAll("rect")
    .data(_data)
    .enter().append("rect")
    .attr("class", "rect-stacked")
    .attr("x", d => xScale(d.cumulative))
    .attr("y", h / 2 - halfBarHeight)
    .attr("height", barHeight)
    .attr("width", d => xScale(d.value))
    .style("fill", (d, i) => colors[i])

  // add values on bar
  selection.selectAll(".text-value")
    .data(_data)
    .enter().append("text")
    .attr("class", "text-value")
    .attr("text-anchor", "middle")
    .attr("x", d => xScale(d.cumulative) + (xScale(d.value) / 2))
    .attr("y", (h / 2) + 5)
    .text(d => f(d.percent) + "%")
}