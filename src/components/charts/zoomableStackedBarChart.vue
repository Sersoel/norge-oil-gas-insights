<template>
  <div ref="chartContainer" class="w-full h-[500px] relative">
    <svg ref="svg" class="absolute top-0 left-0 w-full h-full"></svg>
  </div>
</template>

<script setup>
import * as d3 from 'd3'
import { ref, onMounted } from 'vue'

const svg = ref(null)
const chartContainer = ref(null)

onMounted(async () => {
  const margin = { left: 70, right: 70, top: 40, bottom: 40 }
  const container = chartContainer.value

  const containerWidth = container.clientWidth
  const containerHeight = container.clientHeight
  const width = containerWidth - margin.left - margin.right
  const height = containerHeight - margin.top - margin.bottom

  // Load CSV data
  const data = await d3.csv(
    new URL('/data/processed/NorskPetroleum.csv', import.meta.url),
    (d) => ({
      Year: d.Year,
      Oil: isNaN(+d.Oil) ? 0 : +d.Oil,
      Condensate: isNaN(+d.Condensate) ? 0 : +d.Condensate,
      NGL: isNaN(+d.NGL) ? 0 : +d.NGL,
      Gas: isNaN(+d.Gas) ? 0 : +d.Gas,
      Total: isNaN(+d.TotalOilEquivalents) ? 0 : +d.TotalOilEquivalents,
    }),
  )

  console.log('Data Loaded:', data)

  renderChart(data)

  // Redraw on resize
  d3.select(window).on('resize', async () => {
    d3.select(svg.value).selectAll('*').remove()
    const resizedData = await d3.csv(
      new URL('/data/processed/annual_historical_production.csv', import.meta.url),
      (d) => ({
        Year: d.Year,
        Oil: isNaN(+d.Oil) ? 0 : +d.Oil,
        Condensate: isNaN(+d.Condensate) ? 0 : +d.Condensate,
        NGL: isNaN(+d.NGL) ? 0 : +d.NGL,
        Gas: isNaN(+d.Gas) ? 0 : +d.Gas,
        Total: isNaN(+d.TotalOilEquivalents) ? 0 : +d.TotalOilEquivalents,
      }),
    )
    renderChart(resizedData)
  })

  function renderChart(data) {
    const products = ['Oil', 'Condensate', 'NGL', 'Gas']
    const years = data.map((d) => d.Year)

    const barColor = d3
      .scaleOrdinal()
      .domain(products)
      .range(['#333333', '#795548', '#9c27b0', '#00bcd4'])

    const x = d3.scaleBand().domain(years).range([0, width]).padding(0.3)

    const y = d3
      .scaleLinear()
      .domain([0, d3.max(data, (d) => d.Total)])
      .nice()
      .range([height, 0])

    const stackedData = d3.stack().keys(products)(data)

    const svgEl = d3
      .select(svg.value)
      .attr('viewBox', [0, 0, containerWidth, containerHeight])
      .attr('style', 'max-width: 100%; height: auto;')

    svgEl
      .append('text')
      .attr('x', width / 2 + margin.left)
      .attr('y', margin.top / 2)
      .attr('text-anchor', 'middle')
      .attr('font-size', 24)
      .attr('font-weight', 'bold')
      .text('Annual Norsk Petroleum Production')

    const barGroups = svgEl
      .append('g')
      .attr('class', 'bars')
      .attr('transform', `translate(${margin.left},${margin.top})`)

    const groups = barGroups
      .selectAll('g')
      .data(stackedData)
      .join('g')
      .attr('fill', (d) => barColor(d.key))

    const bars = groups
      .selectAll('rect')
      .data((d) => d)
      .join('rect')
      .attr('x', (d) => x(d.data.Year))
      .attr('y', (d) => y(d[1]))
      .attr('width', x.bandwidth())
      .attr('height', (d) => y(d[0]) - y(d[1]))

    // Tooltip
    const tooltip = d3
      .select(chartContainer.value)
      .append('div')
      .style('opacity', 0)
      .style('position', 'absolute')
      .style('pointer-events', 'none')
      .style('background', 'rgba(0,0,0,0.8)')
      .style('color', '#fff')
      .style('padding', '8px')
      .style('font-size', '12px')
      .style('border-radius', '5px')
      .style('z-index', 10)

    bars.on('mousemove', (event, d) => {
      const productName = d3.select(event.currentTarget.parentNode).datum().key
      const productsValue = d[1] - d[0]

      tooltip
        .html(`Product: ${productName}<br>Value: ${productsValue.toFixed(2)}`)
        .style('left', `${event.pageX + 14}px`)
        .style('top', `${event.pageY - 28}px`)
        .transition()
        .duration(100)
        .style('opacity', 1)
    })
    bars.on('mouseleave', () => {
      tooltip.transition().duration(300).style('opacity', 0)
    })

    // Axis X
    const xAxis = d3.axisBottom(x)
    const xAxisGroup = barGroups
      .append('g')
      .attr('class', 'axis-X')
      .attr('transform', `translate(0, ${height})`)
      .call(xAxis)

    xAxisGroup.selectAll('text').attr('transform', 'rotate(-45)').style('text-anchor', 'end')

    // Axis Y
    const yAxis = d3.axisLeft(y).ticks(6)
    const yAxisGroup = barGroups.append('g').attr('class', 'axis-Y').call(yAxis)

    // Y-axis label
    svgEl
      .append('text')
      .attr('x', -height / 2 - margin.top)
      .attr('y', margin.left - 40)
      .attr('transform', 'rotate(-90)')
      .attr('text-anchor', 'middle')
      .style('font-size', '14px')
      .text('Oil Equivalent Production (Mtoe)')

    svgEl
      .append('text')
      .attr('x', width / 2 + margin.left)
      .attr('y', height + margin.top + margin.bottom)
      .attr('text-anchor', 'middle')
      .style('font-size', '14px')
      .text('Year')

    // Legend
    const reversedProducts = products.slice().reverse()
    const legend = svgEl
      .append('g')
      .attr('transform', `translate(${margin.left + 50}, ${margin.top + 40})`)

    reversedProducts.forEach((product, index) => {
      const legendItem = legend.append('g').attr('transform', `translate(0, ${index * 25})`)

      legendItem.append('rect').attr('width', 20).attr('height', 20).attr('fill', barColor(product))

      legendItem.append('text').attr('x', 30).attr('y', 15).style('font-size', '12px').text(product)
    })

    // Zoom behavior
    const extent = [
      [margin.left, margin.top],
      [width - margin.right, height - margin.bottom],
    ]

    const zoom = d3
      .zoom()
      .scaleExtent([1, 5])
      .translateExtent(extent)
      .extent(extent)
      .on('zoom', (event) => {
        x.range([0, width - margin.right].map((d) => event.transform.applyX(d)))
        svgEl
          .selectAll('.bars rect')
          .attr('x', (d) => x(d.data.Year))
          .attr('width', x.bandwidth())
        svgEl.selectAll('.axis-X').call(xAxis)
      })

    svgEl.call(zoom)
  }
})
</script>

<style scoped>
svg {
  height: 500px;
  width: 100%;
  overflow: visible;
}

.tooltip {
  transition: opacity 0.15s ease;
}
</style>
