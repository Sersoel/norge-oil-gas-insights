<template>
  <!-- Responsive stacked bar + line chart -->
  <svg ref="svgRef" class="chart" />
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as d3 from 'd3'

/* ────────────── Constants ────────────── */
const CSV_URL = new URL(
  '/data/processed/Export value of Norwegian petroleum, 1971-2023.csv',
  import.meta.url,
)
const PRODUCTS = ['CrudeOil', 'NaturalGas', 'Condensate'] as const
const LINE_LABEL = 'Total exports' // legend label for the blue line
const fmtInt = d3.format(',')
const LINE_COLOR = 'steelblue'

/* ────────────── State ────────────── */
const svgRef = ref<SVGSVGElement | null>(null)
let resizeObserver: ResizeObserver | null = null

/* ────────────── Lifecycle ────────────── */
onMounted(async () => {
  const raw = await d3.csv(CSV_URL.href, d3.autoType)
  const data = raw.filter((d) => d.Year && PRODUCTS.every((k) => k in d))

  if (svgRef.value) renderChart(data)
  resizeObserver = new ResizeObserver(() => svgRef.value && renderChart(data))
  resizeObserver.observe(svgRef.value!.parentElement!)
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  d3.select('body').selectAll('div.vue-stacked-tooltip').remove()
})

/* ────────────── Render ────────────── */
function renderChart(data: Array<any>) {
  if (!svgRef.value || !svgRef.value.parentElement) return

  const svg = d3.select(svgRef.value)
  svg.selectAll('*').remove()

  const { width: containerW } = svgRef.value.parentElement.getBoundingClientRect()
  const chartHeight = 500
  const margin = { top: 70, right: 180, bottom: 80, left: 100 }
  const innerW = containerW - margin.left - margin.right
  const innerH = chartHeight - margin.top - margin.bottom

  svg.attr('viewBox', `0 0 ${containerW} ${chartHeight}`)

  /* Root group */
  const g = svg.append('g').attr('transform', `translate(${margin.left},${margin.top})`)

  /* Scales */
  const x = d3
    .scaleBand<string>()
    .domain(data.map((d) => d.Year))
    .range([0, innerW])
    .padding(0.25)

  const y = d3
    .scaleLinear()
    .domain([0, d3.max(data, (d) => d.TotalExportsOfGoods) || 0])
    .nice()
    .range([innerH, 0])

  const color = d3
    .scaleOrdinal<string>()
    .domain(PRODUCTS as unknown as string[])
    .range(['#333333', '#6B8E23', '#795548'])

  /* Axes */
  g.append('g')
    .attr('transform', `translate(0,${innerH})`)
    .call(d3.axisBottom(x))
    .selectAll('text')
    .attr('transform', 'rotate(-45)')
    .style('text-anchor', 'end')

  g.append('g').call(d3.axisLeft(y).tickFormat(fmtInt))

  /* Stacked Bars */
  const stacked = d3.stack().keys(PRODUCTS as unknown as string[])(data)

  const tooltip = d3
    .select('body')
    .selectAll('div.vue-stacked-tooltip')
    .data([null])
    .join('div')
    .attr('class', 'vue-stacked-tooltip')
    .style('position', 'absolute')
    .style('pointer-events', 'none')
    .style('opacity', 0)
    .style('background', '#000a')
    .style('color', '#fff')
    .style('padding', '6px 10px')
    .style('border-radius', '6px')
    .style('font-size', '12px')

  const layers = g
    .selectAll('g.layer')
    .data(stacked)
    .join('g')
    .attr('class', 'layer')
    .attr('fill', (d) => color(d.key))

  layers
    .selectAll('rect')
    .data((d) => d)
    .join('rect')
    .attr('x', (d) => x(d.data.Year)!)
    .attr('y', (d) => y(d[1]))
    .attr('height', (d) => y(d[0]) - y(d[1]))
    .attr('width', x.bandwidth())
    .on('mousemove', (event, d) => {
      const key = (d3.select(event.currentTarget.parentNode as SVGGElement).datum() as any).key
      tooltip
        .style('opacity', 1)
        .html(`<strong>${key}</strong><br>${fmtInt(d[1] - d[0])}`)
        .style('left', `${event.pageX + 15}px`)
        .style('top', `${event.pageY - 28}px`)
    })
    .on('mouseleave', () => tooltip.style('opacity', 0))

  /* Overlay Line */
  const line = d3
    .line<any>()
    .x((d) => x(d.Year)! + x.bandwidth() / 2)
    .y((d) => y(d.TotalExportsOfGoods))

  g.append('path')
    .datum(data)
    .attr('fill', 'none')
    .attr('stroke', LINE_COLOR)
    .attr('stroke-width', 2.5)
    .attr('d', line)

  // Add invisible circles for tooltip on line points
  g.selectAll('.total-exports-point')
    .data(data)
    .join('circle')
    .attr('class', 'total-exports-point')
    .attr('cx', (d) => x(d.Year)! + x.bandwidth() / 2)
    .attr('cy', (d) => y(d.TotalExportsOfGoods))
    .attr('r', 10)
    .style('fill', 'transparent')
    .style('pointer-events', 'all')
    .on('mousemove', (event, d) => {
      tooltip
        .style('opacity', 1)
        .html(
          `
        <strong>${LINE_LABEL}</strong><br>
        Year: ${d.Year}<br>
        Total: ${fmtInt(d.TotalExportsOfGoods)}
      `,
        )
        .style('left', `${event.pageX + 15}px`)
        .style('top', `${event.pageY - 28}px`)
    })
    .on('mouseleave', () => tooltip.style('opacity', 0))

  /* Legend */
  const legend = g
    .append('g')
    .attr('class', 'legend')
    .attr('transform', `translate(${innerW + 20}, 0)`)

  ;(PRODUCTS as readonly string[]).forEach((product, idx) => {
    const row = legend.append('g').attr('transform', `translate(0, ${idx * 26})`)
    row.append('rect').attr('width', 20).attr('height', 20).attr('fill', color(product)!)
    row.append('text').attr('x', 26).attr('y', 15).attr('fill', '#000').text(product)
  })

  // Add legend entry for total-exports line
  const lineRow = legend.append('g').attr('transform', `translate(0, ${PRODUCTS.length * 26})`)
  lineRow
    .append('line')
    .attr('x1', 0)
    .attr('x2', 20)
    .attr('y1', 10)
    .attr('y2', 10)
    .attr('stroke', LINE_COLOR)
    .attr('stroke-width', 3)
  lineRow.append('text').attr('x', 26).attr('y', 14).attr('fill', '#000').text(LINE_LABEL)

  /* Titles */
  svg
    .append('text')
    .attr('x', containerW / 2)
    .attr('y', margin.top / 2)
    .attr('text-anchor', 'middle')
    .attr('font-size', 20)
    .attr('font-weight', 'bold')
    .attr('fill', '#000')
    .text('Export value of Norwegian petroleum, 1971-2023')

  svg
    .append('text')
    .attr('x', containerW / 2)
    .attr('y', chartHeight - margin.bottom / 3)
    .attr('text-anchor', 'middle')
    .attr('font-size', 14)
    .attr('fill', '#000')
    .text('Year')

  svg
    .append('text')
    .attr('x', -(chartHeight / 2))
    .attr('y', margin.left / 3)
    .attr('transform', 'rotate(-90)')
    .attr('text-anchor', 'middle')
    .attr('font-size', 14)
    .attr('fill', '#000')
    .text('CrudeOil Equivalent Production (Mtoe)')
}
</script>

<style scoped>
svg {
  width: 100%;
  height: 500px;
  overflow: visible;
}
</style>
