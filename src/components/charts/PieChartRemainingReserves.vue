<template>
  <div class="relative">
    <div ref="container" class="inline-block">
      <svg ref="svg" :width="width" :height="height"></svg>
    </div>
    <div id="buttons" class="flex gap-2 mt-4">
      <button
        v-for="sea in seas"
        :key="sea"
        class="bg-blue-600 hover:bg-blue-800 text-white px-4 py-2 rounded"
        @click="update(sea)"
      >
        {{ sea }}
      </button>
      <button class="bg-green-600 hover:bg-green-800 text-white px-4 py-2 rounded" @click="compare">
        Compare Totals
      </button>
    </div>
  </div>
</template>

<script setup>
import * as d3 from 'd3'
import { ref, onMounted } from 'vue'

// SVG + chart references
const svg = ref(null)
const container = ref(null)

// Seas for buttons
const seas = ref(['Barents sea', 'Norwegian sea', 'North sea'])

// Store totals for compare chart
const totals = ref({})

// Dimensions
const width = 400
const height = 400
const radius = 150

let svgGroup = null
let color = null

onMounted(async () => {
  // LOAD CSV
  const csvUrl = new URL('/data/processed/remaining_reserves.csv', import.meta.url)
  const raw = await d3.csv(csvUrl, d3.autoType)

  console.log('Loaded data', raw)

  // BUILD dataBySea and totals
  const dataBySea = {}
  const totalsTemp = {}

  raw.forEach((d) => {
    dataBySea[d.Sea] = {
      Oil: d.Oil,
      Condensate: d.Condensate,
      NGL: d.NGL,
      Gas: d.Gas,
    }
    totalsTemp[d.Sea] = d.Sum
  })

  window.__dataBySea = dataBySea
  totals.value = totalsTemp

  console.log('window.__dataBySea', window.__dataBySea)

  // Build SVG
  svgGroup = d3
    .select(svg.value)
    .attr('viewBox', `0 0 ${width} ${height}`)
    .append('g')
    .attr('transform', `translate(${width / 2}, ${height / 2})`)

  color = d3
    .scaleOrdinal()
    .domain(['Oil', 'Condensate', 'NGL', 'Gas', 'Barents sea', 'Norwegian sea', 'North sea'])
    .range(['#333333', '#00bcd4', '#795548', '#9c27b0', '#ADD8E6', '#00BCD4', '#0000FF'])

  // Draw initial chart
  update(seas.value[0])
})

// Draw a single sea
function update(sea) {
  console.log('Clicked sea:', sea)

  const data = window.__dataBySea?.[sea]

  if (!data) {
    console.error('Data not found for:', sea)
    return
  }

  const pie = d3
    .pie()
    .value((d) => d.value)
    .sort(null)

  const data_ready = pie(
    Object.entries(data).map(([key, value]) => ({
      key,
      value,
    })),
  )

  const arc = d3.arc().innerRadius(0).outerRadius(radius)

  const labelArc = d3
    .arc()
    .innerRadius(radius / 2)
    .outerRadius(radius)

  // JOIN paths
  const u = svgGroup.selectAll('path').data(data_ready)

  u.enter()
    .append('path')
    .merge(u)
    .transition()
    .duration(1000)
    .attr('d', arc)
    .attr('fill', (d) => color(d.data.key))
    .attr('stroke', 'white')
    .style('stroke-width', '2px')
    .style('opacity', 1)

  u.exit().remove()

  // JOIN labels
  const labels = svgGroup.selectAll('text').data(data_ready)

  labels
    .enter()
    .append('text')
    .merge(labels)
    .transition()
    .duration(1000)
    .attr('transform', (d) => `translate(${labelArc.centroid(d)})`)
    .attr('text-anchor', 'middle')
    .attr('font-size', '12px')
    .text((d) => {
      const total = d3.sum(data_ready.map((d) => d.data.value))
      const percent = ((d.data.value / total) * 100).toFixed(1)
      return percent + '%'
    })

  labels.exit().remove()

  // Tooltip
  svgGroup
    .selectAll('path')
    .on('mouseover', (event, d) => {
      d3.select('body')
        .append('div')
        .attr('class', 'tooltip')
        .style('position', 'absolute')
        .style('background', '#fff')
        .style('border', '1px solid #ccc')
        .style('padding', '5px')
        .style('border-radius', '5px')
        .style('pointer-events', 'none')
        .html(`Type: ${d.data.key}<br>Value: ${d.data.value.toFixed(2)}`)
        .style('left', event.pageX + 10 + 'px')
        .style('top', event.pageY + 10 + 'px')
    })
    .on('mousemove', (event) => {
      d3.select('.tooltip')
        .style('left', event.pageX + 10 + 'px')
        .style('top', event.pageY + 10 + 'px')
    })
    .on('mouseout', () => {
      d3.select('.tooltip').remove()
    })
}

// Compare totals across seas
function compare() {
  console.log('Comparing totals', totals.value)

  const pie = d3
    .pie()
    .value((d) => d.value)
    .sort(null)

  const data_ready = pie(
    Object.entries(totals.value).map(([key, value]) => ({
      key,
      value,
    })),
  )

  const arc = d3.arc().innerRadius(0).outerRadius(radius)

  const labelArc = d3
    .arc()
    .innerRadius(radius / 2)
    .outerRadius(radius)

  const u = svgGroup.selectAll('path').data(data_ready)

  u.enter()
    .append('path')
    .merge(u)
    .transition()
    .duration(1000)
    .attr('d', arc)
    .attr('fill', (d) => color(d.data.key))
    .attr('stroke', 'white')
    .style('stroke-width', '2px')
    .style('opacity', 1)

  u.exit().remove()

  const labels = svgGroup.selectAll('text').data(data_ready)

  labels
    .enter()
    .append('text')
    .merge(labels)
    .transition()
    .duration(1000)
    .attr('transform', (d) => `translate(${labelArc.centroid(d)})`)
    .attr('text-anchor', 'middle')
    .attr('font-size', '12px')
    .text((d) => {
      const total = d3.sum(data_ready.map((d) => d.data.value))
      const percent = ((d.data.value / total) * 100).toFixed(1)
      return `${d.data.key} (${percent}%)`
    })

  labels.exit().remove()

  svgGroup
    .selectAll('path')
    .on('mouseover', (event, d) => {
      d3.select('body')
        .append('div')
        .attr('class', 'tooltip')
        .style('position', 'absolute')
        .style('background', '#fff')
        .style('border', '1px solid #ccc')
        .style('padding', '5px')
        .style('border-radius', '5px')
        .style('pointer-events', 'none')
        .html(`Sea: ${d.data.key}<br>Total: ${d.data.value.toFixed(2)}`)
        .style('left', event.pageX + 10 + 'px')
        .style('top', event.pageY + 10 + 'px')
    })
    .on('mousemove', (event) => {
      d3.select('.tooltip')
        .style('left', event.pageX + 10 + 'px')
        .style('top', event.pageY + 10 + 'px')
    })
    .on('mouseout', () => {
      d3.select('.tooltip').remove()
    })
}
</script>

<style scoped>
.tooltip {
  position: absolute;
  background: #fff;
  border: 1px solid #ccc;
  padding: 5px;
  border-radius: 5px;
  font-size: 12px;
  pointer-events: none;
}
</style>
