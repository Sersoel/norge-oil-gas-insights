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
  const containerWidth = 800
  const containerHeight = 400
  const width = containerWidth - margin.left - margin.right
  const height = containerHeight - margin.top - margin.bottom

  const data = await d3.csv(
    new URL('/assets/data/annual_historical_production.csv', import.meta.url),
    d3.autoType,
  )
  const keys = ['oil', 'gas', 'condensate', 'ngl']
  const color = d3.scaleOrdinal().domain(keys).range(d3.schemeCategory10)

  const x = d3
    .scaleLinear()
    .domain(d3.extent(data, (d) => d.year))
    .range([0, width])

  const y = d3
    .scaleLinear()
    .domain([0, d3.max(data, (d) => d3.max(keys, (key) => d[key]))])
    .nice()
    .range([height, 0])

  const svgEl = d3
    .select(svg.value)
    .attr('viewBox', [0, 0, containerWidth, containerHeight])
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  // Axes
  svgEl
    .append('g')
    .call(d3.axisLeft(y).ticks(6))
    .append('text')
    .attr('x', -margin.left)
    .attr('y', -10)
    .attr('fill', 'currentColor')
    .attr('text-anchor', 'start')
    .text('Million Sm³ oil equivalents')

  svgEl
    .append('g')
    .attr('transform', `translate(0,${height})`)
    .call(d3.axisBottom(x).tickFormat(d3.format('d')))

  // Line generator
  const line = d3
    .line()
    .x((d) => x(d.year))
    .y((d) => y(d.value))

  // Tooltip
  const tooltip = d3
    .select(chartContainer.value)
    .append('div')
    .attr('class', 'tooltip')
    .style('position', 'absolute')
    .style('opacity', 0)
    .style('pointer-events', 'none')
    .style('background', '#414141')
    .style('color', '#fff')
    .style('border', '1px solid #fff')
    .style('padding', '6px 10px')
    .style('font-size', '8px')
    .style('border-radius', '4px')
    .style('z-index', 10)

  function showTooltip(event, key, d) {
    const xPos = x(d.year) + margin.left
    const yPos = y(d.value) + margin.top

    tooltip
      .html(
        `
        <div style="font-weight: 600; color: ${color(key)};">${key.toUpperCase()}</div>
        <div><strong>Year:</strong> ${d.year}</div>
        <div><strong>Value:</strong> ${d.value.toFixed(2)} <span style="color: #fff;">MSm³</span></div>
      `,
      )
      .style('left', `${xPos - tooltip.node().offsetWidth / 2}px`)
      .style('top', `${yPos - tooltip.node().offsetHeight - 8}px`)
      .transition()
      .duration(800)
      .style('opacity', 1)
  }

  function hideTooltip() {
    tooltip.transition().duration(800).style('opacity', 0)
  }

  // Draw lines
  keys.forEach((key) => {
    const lineData = data.map((d) => ({ year: d.year, value: d[key] }))
    const lastPoint = lineData.at(-1)

    const group = svgEl.append('g').attr('class', 'line-group').attr('data-key', key)

    // Line path
    group
      .append('path')
      .datum(lineData)
      .attr('class', 'line-path')
      .attr('fill', 'none')
      .attr('stroke', color(key))
      .attr('stroke-width', 2)
      .attr('d', line)

    // Dots
    group
      .selectAll('.line-dot')
      .data(lineData)
      .join('circle')
      .attr('class', 'line-dot')
      .attr('r', 3)
      .attr('cx', (d) => x(d.year))
      .attr('cy', (d) => y(d.value))
      .attr('fill', color(key))
      .on('mouseover', (event, d) => showTooltip(event, key, d))
      .on('mousemove', (event) => {
        tooltip.style('left', `${event.pageX + 5}px`).style('top', `${event.pageY - 28}px`)
      })
      .on('mouseout', hideTooltip)

    // Label
    group
      .append('text')
      .attr('class', 'line-label')
      .attr('x', x(lastPoint.year) + 6)
      .attr('y', y(lastPoint.value))
      .attr('dy', '0.35em')
      .attr('fill', color(key))
      .attr('font-size', 12)
      .attr('font-weight', 'bold')
      .text(key.toUpperCase())
  })

  // Group hover interactivity
  svgEl
    .selectAll('.line-group')
    .on('mouseover', function () {
      const activeKey = d3.select(this).attr('data-key')

      svgEl.selectAll('.line-group').each(function () {
        const key = d3.select(this).attr('data-key')
        const group = d3.select(this)
        const isActive = key === activeKey

        group
          .select('.line-path')
          .attr('stroke', isActive ? color(key) : '#bbb')
          .attr('stroke-opacity', isActive ? 1 : 0.4)

        group.selectAll('.line-dot').attr('fill', isActive ? color(key) : '#bbb')

        group.select('.line-label').attr('fill', isActive ? color(key) : '#aaa')
      })
    })
    .on('mouseout', function () {
      svgEl.selectAll('.line-group').each(function () {
        const key = d3.select(this).attr('data-key')
        const group = d3.select(this)

        group.select('.line-path').attr('stroke', color(key)).attr('stroke-opacity', 1)

        group.selectAll('.line-dot').attr('fill', color(key))
        group.select('.line-label').attr('fill', color(key))
      })
    })

  // Interactivity
  svgEl
    .selectAll('.line-group')
    .on('mouseover', function () {
      const activeKey = d3.select(this).attr('data-key')

      svgEl.selectAll('.line-group').each(function () {
        const key = d3.select(this).attr('data-key')
        const group = d3.select(this)
        const isActive = key === activeKey

        group
          .select('.line-path')
          .attr('stroke', isActive ? color(key) : '#bbb')
          .attr('stroke-opacity', isActive ? 1 : 0.5)

        group.selectAll('.line-dot').attr('fill', isActive ? color(key) : '#bbb')

        group.select('.line-label').attr('fill', isActive ? color(key) : '#aaa')
      })
    })
    .on('mouseout', () => {
      svgEl.selectAll('.line-group').each(function () {
        const key = d3.select(this).attr('data-key')
        const group = d3.select(this)

        group.select('.line-path').attr('stroke', color(key)).attr('stroke-opacity', 1)
        group.selectAll('.line-dot').attr('fill', color(key))
        group.select('.line-label').attr('fill', color(key))
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
  position: absolute;
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

.line-label {
  pointer-events: none;
}
</style>
