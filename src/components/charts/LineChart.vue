<template>
  <div ref="chartContainer" class="w-full h-[400px] relative">
    <svg ref="svg" class="absolute top-0 left-0 w-full h-full"></svg>
  </div>
</template>

<script setup>
import * as d3 from 'd3'
import { ref, onMounted } from 'vue'

const svg = ref(null)
const chartContainer = ref(null)

onMounted(async () => {
  const margin = { top: 30, right: 40, bottom: 50, left: 60 }
  const width = 800 - margin.left - margin.right
  const height = 400 - margin.top - margin.bottom

  const data = await d3.csv('/assets/data/annual_historical_production.csv', d3.autoType)
  const keys = ['oil', 'gas', 'condensate', 'ngl']

  const x = d3
    .scaleLinear()
    .domain(d3.extent(data, (d) => d.year))
    .range([0, width])

  const y = d3
    .scaleLinear()
    .domain([0, d3.max(data, (d) => d3.max(keys, (key) => d[key]))])
    .nice()
    .range([height, 0])

  const color = d3.scaleOrdinal().domain(keys).range(d3.schemeCategory10)

  const svgEl = d3
    .select(svg.value)
    .attr('viewBox', [
      0,
      0,
      width + margin.left + margin.right,
      height + margin.top + margin.bottom,
    ])

  const g = svgEl.append('g').attr('transform', `translate(${margin.left},${margin.top})`)

  g.append('g')
    .call(d3.axisLeft(y).ticks(6))
    .append('text')
    .attr('x', -margin.left)
    .attr('y', -10)
    .attr('fill', 'currentColor')
    .attr('text-anchor', 'start')
    .text('Million Sm³ oil equivalents')

  g.append('g')
    .attr('transform', `translate(0,${height})`)
    .call(d3.axisBottom(x).tickFormat(d3.format('d')))

  const line = d3
    .line()
    .x((d) => x(d.year))
    .y((d) => y(d.value))

  const tooltip = d3
    .select(chartContainer.value)
    .append('div')
    .attr('class', 'tooltip')
    .style('position', 'absolute')
    .style('pointer-events', 'none')
    .style('opacity', 0)
    .style('background', 'white')
    .style('border', '1px solid #ccc')
    .style('padding', '4px 8px')
    .style('font-size', '12px')
    .style('border-radius', '4px')

  keys.forEach((key) => {
    const lineData = data.map((d) => ({ year: d.year, value: d[key] }))
    g.append('path')
      .datum(lineData)
      .attr('fill', 'none')
      .attr('stroke', color(key))
      .attr('stroke-width', 2)
      .attr('d', line)

    g.selectAll(`circle-${key}`)
      .data(lineData)
      .enter()
      .append('circle')
      .attr('cx', (d) => x(d.year))
      .attr('cy', (d) => y(d.value))
      .attr('r', 3)
      .attr('fill', color(key))
      .on('mouseover', (event, d) => {
        // Calculate absolute pixel position of the data point
        const pointX = x(d.year) + margin.left
        const pointY = y(d.value) + margin.top

        tooltip.transition().duration(100).style('opacity', 1)

        tooltip
          .html(
            `
          <div style="font-weight: 600; color: ${color(key)};">${key.toUpperCase()}</div>
          <div><span style="font-weight: 500;">Year:</span> ${d.year}</div>
          <div><span style="font-weight: 500;">Value:</span> ${d.value.toFixed(2)} <span style="color: #666;">Million Sm³</span></div>
        `,
          )
          .style('left', `${pointX - tooltip.node().offsetWidth / 2}px`) // center horizontally
          .style('top', `${pointY - tooltip.node().offsetHeight - 8}px`) // directly above with small gap
      })
      .on('mousemove', function (event) {
        tooltip.style('left', `${event.pageX + 5}px`).style('top', `${event.pageY - 28}px`)
      })
      .on('mouseout', () => {
        tooltip.transition().duration(200).style('opacity', 0)
      })
  })
})
</script>

<style scoped>
svg {
  overflow: visible;
}

.tooltip {
  z-index: 20;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid #ddd;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-family: 'Segoe UI', sans-serif;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  color: #333;
  pointer-events: none;
  transition: opacity 0.15s ease;
}
</style>
