<template>
  <!-- Semantic wrapper: gives us a caption + relative positioning for the tooltip -->
  <figure ref="container" class="relative w-full max-w-3xl mx-auto">
    <figcaption class="text-center font-semibold text-gray-800 mb-2">
      2023 Oil Production – OPEC vs non-OPEC (million barrels per day)
    </figcaption>

    <!-- the chart -->
    <svg ref="svg" :height="height" class="block w-full h-auto"></svg>

    <!-- shared tooltip -->
    <div
      ref="tooltip"
      class="pointer-events-none fixed z-50 rounded bg-gray-900 text-white text-xs px-2 py-1 opacity-0 transition-opacity"
    ></div>
  </figure>
</template>

<script setup>
import * as d3 from 'd3'
import { ref, onMounted, onUnmounted } from 'vue'

/* ---------------------------------------------------------------- *\
|*  CONFIG                                                          *|
\* ---------------------------------------------------------------- */
const height = 460
const margin = { top: 20, right: 40, bottom: 50, left: 140 }

// 🔗  Adjust the path below to where your CSV lives in your Vite/Nuxt project
const csvUrl = new URL('/data/processed/top12_oil_producers_2023.csv', import.meta.url)

/* ---------------------------------------------------------------- *\
|*  REFS                                                            *|
\* ---------------------------------------------------------------- */
const svg = ref(null)
const container = ref(null)
const tooltip = ref(null)

/* ---------------------------------------------------------------- *\
|*  TOOLTIP HELPERS                                                 *|
\* ---------------------------------------------------------------- */
const fmt = d3.format(',.2f') // 12.34 → "12.34"

const hideTip = () => (tooltip.value.style.opacity = 0)

const showTip = (html) => {
  tooltip.value.innerHTML = html
  tooltip.value.style.opacity = 1
}

const moveTip = (evt) => {
  const { pageX: x, pageY: y } = evt
  Object.assign(tooltip.value.style, {
    left: x + 12 + 'px',
    top: y + 12 + 'px',
  })
}

/* ---------------------------------------------------------------- *\
|*  MAIN                                                            *|
\* ---------------------------------------------------------------- */
onMounted(async () => {
  /* 1 – Load + tidy data ----------------------------------------- */
  const raw = await d3.csv(csvUrl, d3.autoType)

  const tidy = raw
    .map((d) => {
      const production = d.non_opec ?? d.opec_members
      if (production == null) return null
      return {
        country: d.country.trim(),
        production: +production,
        group: d.opec_members ? 'OPEC' : 'non-OPEC',
      }
    })
    .filter(Boolean)
    .sort((a, b) => d3.descending(a.production, b.production))

  /* 2 – Dimensions + scales -------------------------------------- */
  const { clientWidth: w } = container.value
  const innerW = w - margin.left - margin.right
  const innerH = height - margin.top - margin.bottom

  const x = d3
    .scaleLinear()
    .domain([0, d3.max(tidy, (d) => d.production)])
    .nice()
    .range([0, innerW])

  const y = d3
    .scaleBand()
    .domain(tidy.map((d) => d.country))
    .range([0, innerH])
    .padding(0.75)

  const color = d3.scaleOrdinal().domain(['OPEC', 'non-OPEC']).range(['#1976d2', '#d32f2f']) // Blue for OPEC, Red for non-OPEC

  /* 3 – SVG scaffold --------------------------------------------- */
  const svgEl = d3
    .select(svg.value)
    .attr('viewBox', [0, 0, w, height])
    .attr('font-family', 'system-ui, sans-serif')

  const g = svgEl.append('g').attr('transform', `translate(${margin.left},${margin.top})`)

  /* 4 – Stems ----------------------------------------------------- */
  g.selectAll('line')
    .data(tidy)
    .join('line')
    .attr('x1', x(0))
    .attr('x2', (d) => x(d.production))
    .attr('y1', (d) => y(d.country))
    .attr('y2', (d) => y(d.country))
    .attr('stroke', '#cccccc')
    .attr('stroke-width', 2)

  /* 5 – Dots ------------------------------------------------------ */
  g.selectAll('circle')
    .data(tidy)
    .join('circle')
    .attr('cx', (d) => x(d.production))
    .attr('cy', (d) => y(d.country))
    .attr('r', 7)
    .attr('fill', (d) => color(d.group))
    .on('mouseenter', (evt, d) => {
      showTip(`${d.country}: ${fmt(d.production)} Mb/d (${d.group})`)
      moveTip(evt)
    })
    .on('mousemove', moveTip)
    .on('mouseleave', hideTip)

  /* 6 – Axes ------------------------------------------------------ */
  const yAxis = d3.axisLeft(y)
  const xAxis = d3
    .axisBottom(x)
    .ticks(5)
    .tickFormat((d) => `${d}`)

  g.append('g').attr('class', 'y-axis').call(yAxis)

  g.append('g').attr('class', 'x-axis').attr('transform', `translate(0,${innerH})`).call(xAxis)

  /* 7 – Axis label ---------------------------------------------- */
  g.append('text')
    .attr('x', innerW / 2)
    .attr('y', innerH + 38)
    .attr('text-anchor', 'middle')
    .attr('font-weight', 600)
    .text('Million barrels per day (2023)')

  /* 8 – Legend ---------------------------------------------------- */
  const legend = svgEl
    .append('g')
    .attr('transform', `translate(${w - margin.right - 120},${margin.top})`)

  ;['OPEC', 'non-OPEC'].forEach((grp, i) => {
    const row = legend.append('g').attr('transform', `translate(60, ${i * 22 + 150})`)

    row.append('rect').attr('width', 14).attr('height', 14).attr('fill', color(grp))

    row.append('text').attr('x', 22).attr('y', 12).text(grp)
  })
})

/* 9 – Cleanup ---------------------------------------------------- */
onUnmounted(() => tooltip.value?.remove?.())
</script>

<style scoped>
figure {
  height: 600px;
  width: 55%;
  overflow: visible;
}

.axis path,
.axis line {
  stroke: #d0d0d0;
}
</style>
