<template>
  <div class="heatmap-container">
    <h2 class="text-2xl font-bold mb-4">Production per sea</h2>

    <div class="mb-6">
      <label for="sea-select" class="mr-2 font-semibold"> Choose a sea field: </label>
      <select
        id="sea-select"
        v-model="selectedSea"
        @change="loadData"
        class="border rounded px-2 py-1 text-sm"
      >
        <option v-for="sea in seaOptions" :key="sea" :value="sea">
          {{ sea }}
        </option>
      </select>
    </div>

    <div class="heatmap-wrapper">
      <div ref="heatmapContainer"></div>
      <div ref="legendContainer" class="legend-container"></div>
    </div>

    <div ref="tooltip" class="tooltip"></div>
  </div>
</template>

<script setup>
import * as d3 from 'd3'
import { ref, onMounted } from 'vue'

const seaOptions = ['Barents Sea', 'North Sea', 'Norwegian Sea']

const selectedSea = ref('Barents Sea')

const filePaths = {
  'Barents Sea': new URL(
    '/data/processed/Annual_production_from_fields_in_the_Barents_Sea.csv',
    import.meta.url,
  ),
  'North Sea': new URL(
    '/data/processed/Annual_production_from_fields_in_the_North_Sea.csv',
    import.meta.url,
  ),
  'Norwegian Sea': new URL(
    '/data/processed/Annual_production_from_fields_in_the_Norwegian_Sea.csv',
    import.meta.url,
  ),
}

const heatmapContainer = ref(null)
const legendContainer = ref(null)
const tooltip = ref(null)

// Brand colors
const fieldColors = {
  oil: '#333333',
  gas: '#00bcd4',
  condensate: '#795548',
  ngl: '#9c27b0',
}

let svg = null

onMounted(() => {
  loadData()
})

function loadData() {
  const path = filePaths[selectedSea.value]
  d3.csv(path, d3.autoType)
    .then((rawData) => {
      console.log('Loaded data:', rawData)

      rawData.forEach((d) => {
        d.total = +d.oil + +d.condensate + +d.ngl + +d.gas
      })

      renderHeatmap(rawData)
      renderLegend(rawData)
    })
    .catch((err) => {
      console.error('Error loading CSV:', err)
    })
}

function renderHeatmap(data) {
  d3.select(heatmapContainer.value).selectAll('*').remove()

  const margin = { top: 40, right: 40, bottom: 100, left: 100 }
  const width = 900 - margin.left - margin.right
  const height = 400 - margin.top - margin.bottom

  svg = d3
    .select(heatmapContainer.value)
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  const fields = ['oil', 'gas', 'condensate', 'ngl'] // updated order
  const years = data.map((d) => d.year)

  // Calculate max per field
  const maxValuePerField = {}
  fields.forEach((field) => {
    maxValuePerField[field] = d3.max(data, (d) => d[field])
  })

  // Create color scales for each field
  const colorScales = {}
  fields.forEach((field) => {
    colorScales[field] = d3
      .scaleLinear()
      .domain([0, maxValuePerField[field]])
      .range(['#e0e0e0', fieldColors[field]])
  })

  const x = d3.scaleBand().domain(years).range([0, width]).padding(0.05)

  const y = d3.scaleBand().domain(fields).range([0, height]).padding(0.05)

  //  X-axis (years)
  svg
    .append('g')
    .attr('transform', `translate(0, ${height})`)
    .call(d3.axisBottom(x).tickValues(years).tickFormat(d3.format('d')))
    .selectAll('text')
    .attr('transform', 'rotate(-45)')
    .style('text-anchor', 'end')

  //  Y-axis (fields) - leave as is, or replace with axisLeft
  svg
    .append('g')
    .selectAll('text')
    .data(fields)
    .join('text')
    .attr('x', -10)
    .attr('y', (d) => y(d) + y.bandwidth() / 2)
    .attr('text-anchor', 'end')
    .attr('alignment-baseline', 'middle')
    .attr('font-size', '12px')
    .text((d) => d)

  svg
    .selectAll('.cell')
    .data(
      data.flatMap((d) =>
        fields.map((field) => ({
          year: d.year,
          field,
          value: +d[field],
        })),
      ),
    )
    .join('rect')
    .attr('class', 'cell')
    .attr('x', (d) => x(d.year))
    .attr('y', (d) => y(d.field))
    .attr('width', x.bandwidth())
    .attr('height', y.bandwidth())
    .attr('fill', (d) => colorScales[d.field](d.value))
    .attr('stroke', '#fff')
    .on('mouseover', (event, d) => {
      d3.select(tooltip.value)
        .style('opacity', 1)
        .html(
          `
          <strong>Year:</strong> ${d.year}<br/>
          <strong>Field:</strong> ${d.field}<br/>
          <strong>Production:</strong> ${d.value.toFixed(2)} MSm³ o.e.
        `,
        )
        .style('left', `${event.pageX + 10}px`)
        .style('top', `${event.pageY - 30}px`)
    })
    .on('mousemove', (event) => {
      d3.select(tooltip.value)
        .style('left', `${event.pageX + 10}px`)
        .style('top', `${event.pageY - 30}px`)
    })
    .on('mouseout', () => {
      d3.select(tooltip.value).style('opacity', 0)
    })
}

function renderLegend(data) {
  d3.select(legendContainer.value).selectAll('*').remove()

  const legendWidth = 150
  const legendHeight = 20

  const fields = ['oil', 'gas', 'condensate', 'ngl']

  const maxValuePerField = {}
  fields.forEach((field) => {
    maxValuePerField[field] = d3.max(data, (d) => d[field])
  })

  const legendSvg = d3
    .select(legendContainer.value)
    .append('svg')
    .attr('width', legendWidth + 60)
    .attr('height', fields.length * (legendHeight + 10))

  fields.forEach((field, i) => {
    const gradientId = `gradient-${field}`

    const defs = legendSvg.append('defs')
    const gradient = defs
      .append('linearGradient')
      .attr('id', gradientId)
      .attr('x1', '0%')
      .attr('x2', '100%')
      .attr('y1', '0%')
      .attr('y2', '0%')

    gradient.append('stop').attr('offset', '0%').attr('stop-color', '#e0e0e0')

    gradient.append('stop').attr('offset', '100%').attr('stop-color', fieldColors[field])

    legendSvg
      .append('rect')
      .attr('x', 0)
      .attr('y', i * (legendHeight + 10))
      .attr('width', legendWidth)
      .attr('height', legendHeight)
      .style('fill', `url(#${gradientId})`)

    legendSvg
      .append('text')
      .attr('x', legendWidth + 10)
      .attr('y', i * (legendHeight + 10) + legendHeight / 2 + 4)
      .text(`${field}`)
      .style('font-size', '12px')
      .style('alignment-baseline', 'middle')
  })
}
</script>

<style scoped>
.heatmap-container {
  max-width: 1200px;
  margin: auto;
}

.heatmap-wrapper {
  display: flex;
  gap: 32px;
  align-items: center;
}

.legend-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.tooltip {
  position: absolute;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 4px;
  pointer-events: none;
  opacity: 0;
}
</style>
