<template>
  <div class="w-full h-[400px] relative">
    <svg ref="svg" class="absolute top-0 left-0 w-full h-full"></svg>
  </div>
</template>

<script setup>
import * as d3 from 'd3'
import { ref, onMounted } from 'vue'

const svg = ref(null)

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

  keys.forEach((key) => {
    const lineData = data.map((d) => ({ year: d.year, value: d[key] }))
    g.append('path')
      .datum(lineData)
      .attr('fill', 'none')
      .attr('stroke', color(key))
      .attr('stroke-width', 2)
      .attr('d', line)
  })
})
</script>

<style scoped>
svg {
  overflow: visible;
}
</style>
