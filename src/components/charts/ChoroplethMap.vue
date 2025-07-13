<script setup>
import { ref, onMounted } from 'vue'
import * as d3 from 'd3'

// ---- Props & Emits ----

const props = defineProps({
  geojson: Object,
  productionTotals: Object,
})

const emit = defineEmits(['update:selectedSeas'])

// Selected seas (reactive)
const selectedSeas = ref([])

// ---- Event Handlers ----

function toggleSea(seaName) {
  const index = selectedSeas.value.indexOf(seaName)
  if (index === -1) {
    selectedSeas.value.push(seaName)
  } else {
    selectedSeas.value.splice(index, 1)
  }
  emit('update:selectedSeas', [...selectedSeas.value])
}

// ---- D3 Logic ----

onMounted(() => {
  initializeSelectedSeas()
  renderChoropleth()
})

function initializeSelectedSeas() {
  selectedSeas.value = props.geojson.features.map((d) => d.properties.IHO_Sea)
  emit('update:selectedSeas', [...selectedSeas.value])
}

function renderChoropleth() {
  const container = d3.select('#choropleth-map-container')
  const width = container.node().clientWidth
  const height = 400

  const svg = container
    .append('svg')
    .attr('viewBox', `0 0 ${width} ${height}`)
    .attr('preserveAspectRatio', 'xMinYMin meet')
    .attr('width', width)
    .attr('height', height)

  // Handle resize
  new ResizeObserver((entries) => {
    for (const entry of entries) {
      svg.attr('width', entry.contentRect.width)
    }
  }).observe(container.node())

  const projection = d3.geoMercator().fitSize([width, height], props.geojson)

  const path = d3.geoPath().projection(projection)

  // Color scale
  const colorScale = createColorScale(props.productionTotals)

  const g = svg.append('g')

  drawSeas(g, path, colorScale)
  drawLabels(g, projection, colorScale)
}

function createColorScale(productionTotals) {
  const values = Object.values(productionTotals || {})
  const [minP, maxP] = d3.extent(values)

  return d3
    .scaleSequential()
    .domain([minP, maxP])
    .interpolator((t) => d3.interpolateBlues(0.2 + 0.6 * t))
}

function drawSeas(group, path, colorScale) {
  group
    .selectAll('path.sea')
    .data(props.geojson.features)
    .join('path')
    .attr('class', 'sea')
    .attr('d', path)
    .attr('stroke', '#333')
    .attr('fill', (d) => getSeaFillColor(d, colorScale))
    .style('cursor', 'pointer')
    .on('click', function (event, d) {
      const sea = d.properties.IHO_Sea
      toggleSea(sea)

      // Animate fill change
      const prod = props.productionTotals?.[sea] ?? 0
      const isSelected = selectedSeas.value.includes(sea)

      d3.select(this)
        .transition()
        .duration(300)
        .attr('fill', isSelected && prod > 0 ? colorScale(prod) : '#e0e0e0')
    })
}

function getSeaFillColor(d, colorScale) {
  const sea = d.properties.IHO_Sea
  const prod = props.productionTotals?.[sea] ?? 0
  return selectedSeas.value.includes(sea) && prod > 0 ? colorScale(prod) : '#e0e0e0'
}

function drawLabels(group, projection, colorScale) {
  const labelGroup = group
    .selectAll('text.sea-label')
    .data(props.geojson.features)
    .join('text')
    .attr('class', 'sea-label')
    .attr('text-anchor', 'middle')
    .attr('fill', 'black')
    .attr('font-size', 10)
    .attr('pointer-events', 'none')
    .attr('x', (d) => projection(d3.geoCentroid(d))[0])
    .attr('y', (d) => projection(d3.geoCentroid(d))[1])

  labelGroup.each(function (d) {
    const sea = d.properties.IHO_Sea
    const prod = props.productionTotals?.[sea] ?? 0

    d3.select(this).selectAll('*').remove()

    d3.select(this)
      .append('tspan')
      .attr('x', this.getAttribute('x'))
      .attr('dy', 0)
      .attr('font-weight', 'bold')
      .text(sea)

    d3.select(this)
      .append('tspan')
      .attr('x', this.getAttribute('x'))
      .attr('dy', 16)
      .attr('font-size', 8)
      .attr('font-weight', 'normal')
      .text(`(${prod.toFixed(1).toLocaleString()} MSm³)`)
  })
}
</script>

<template>
  <div id="choropleth-map-container" class="w-full h-auto"></div>
</template>

<style scoped>
#choropleth-map-container {
  height: 400px;
}
</style>
