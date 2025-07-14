<script setup>
import { ref, watch } from 'vue'
import * as d3 from 'd3'
import productionPerSea from '/data/processed/production_per_sea.csv?raw'

const props = defineProps({
  selectedSeas: {
    type: Array,
    required: true,
  },
})

const SEA_ORDER = ['Barents sea', 'Norwegian sea', 'North sea']
const COMMODITIES = ['oil', 'gas', 'condensate', 'ngl']
const COLOR_MAP = {
  oil: '#333333',
  gas: '#00bcd4',
  condensate: '#795548',
  ngl: '#9c27b0',
}

const csvData = ref(null)

if (!csvData.value) {
  csvData.value = d3.csvParse(productionPerSea)
}

watch(
  () => props.selectedSeas,
  (newSeas) => {
    if (!newSeas || newSeas.length === 0) {
      d3.select('#barchart').selectAll('*').remove()
      return
    }
    const ordered = SEA_ORDER.filter((sea) => newSeas.includes(sea))
    drawChart(ordered)
  },
  { immediate: true },
)

function drawChart(selectedSeas) {
  const barData = []

  COMMODITIES.forEach((product) => {
    selectedSeas.forEach((sea) => {
      const rows = csvData.value.filter((d) => d.area === sea)
      const total = rows.length > 0 ? rows.reduce((acc, cur) => acc + (+cur[product] || 0), 0) : 0
      barData.push({ product, sea, value: total })
    })
  })

  const svgWidth = 450
  const svgHeight = 350
  const margin = { top: 20, right: 20, bottom: 30, left: 80 }
  const innerWidth = svgWidth - margin.left - margin.right
  const innerHeight = svgHeight - margin.top - margin.bottom

  const svg = d3.select('#barchart').attr('width', svgWidth).attr('height', svgHeight)

  svg.selectAll('*').remove()

  const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`)

  const productScale = d3.scaleBand().domain(COMMODITIES).range([0, innerHeight]).padding(0.4)

  const seaScale = d3
    .scaleBand()
    .domain(selectedSeas)
    .range([0, productScale.bandwidth()])
    .padding(0.2)

  const maxValue = d3.max(barData, (d) => d.value) || 1

  const xScale = d3
    .scaleLinear()
    .domain([0, maxValue * 1.2])
    .range([0, innerWidth])

  const grouped = d3.group(barData, (d) => d.product)

  for (const [product, records] of grouped) {
    const yOffset = productScale(product)
    const rowG = g.append('g').attr('transform', `translate(0, ${yOffset})`)

    rowG
      .selectAll('rect')
      .data(records)
      .join(
        (enter) =>
          enter
            .append('rect')
            .attr('x', 0)
            .attr('y', (d) => seaScale(d.sea))
            .attr('height', seaScale.bandwidth())
            .attr('width', 0)
            .attr('fill', (d) => COLOR_MAP[d.product])
            .transition()
            .duration(800)
            .attr('width', (d) => xScale(d.value)),
        (update) =>
          update
            .transition()
            .duration(800)
            .attr('width', (d) => xScale(d.value)),
        (exit) => exit.transition().duration(500).attr('width', 0).remove(),
      )

    rowG
      .selectAll('text.bar-label')
      .data(records)
      .join('text')
      .attr('class', 'bar-label')
      .attr('x', (d) => xScale(d.value) + 8)
      .attr('y', (d) => seaScale(d.sea) + seaScale.bandwidth() / 2 + 1)
      .attr('fill', '#333')
      .attr('font-size', 11)
      .attr('dominant-baseline', 'middle')
      .text((d) => `${d.sea}: ${d.value.toFixed(1)} MSm³`)
  }

  g.append('g')
    .attr('transform', `translate(0, ${innerHeight})`)
    .call(d3.axisBottom(xScale).ticks(5))
    .selectAll('text')
    .attr('font-size', 12)
    .attr('fill', '#333')

  g.append('g').call(d3.axisLeft(productScale)).selectAll('text').attr('font-size', 14)
}
</script>

<template>
  <svg id="barchart"></svg>
</template>

<style scoped>
body {
  margin: 0;
  font-family: system-ui, sans-serif;
}

svg {
  height: 400px;
  max-width: 95%;
  overflow: visible;
}
</style>
