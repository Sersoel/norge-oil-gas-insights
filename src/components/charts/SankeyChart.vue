<template>
  <!-- semantic wrapper for the caption + relative positioning for the tooltip -->
  <figure ref="container" class="relative w-full max-w-3xl mx-auto">
    <figcaption class="text-center font-semibold text-gray-800 mb-2">
      2024 Oil & NGL / Condensate Exports (million tonnes)
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
import { sankey, sankeyLinkHorizontal } from 'd3-sankey'
import { ref, onMounted, onUnmounted } from 'vue'

/* ────────────── CONFIG ────────────── */
const height = 520 // chart height
const csvUrl = new URL('/data/processed/oil_ngl_condensate_export_2024.csv', import.meta.url)

/* ────────────── REFS ────────────── */
const svg = ref(null)
const container = ref(null)
const tooltip = ref(null)

/* ────────────── UTILS ────────────── */
const format = d3.format(',') // “12,345”
const showTip = (txt, evt) => {
  tooltip.value.textContent = txt
  const { pageX: x, pageY: y } = evt
  Object.assign(tooltip.value.style, {
    left: x + 10 + 'px',
    top: y + 10 + 'px',
    opacity: 1,
  })
}
const hideTip = () => {
  tooltip.value.style.opacity = 0
}

/* ────────────── MAIN ────────────── */
onMounted(async () => {
  /* 1 – Load data ------------------------------------------------- */
  const raw = await d3.csv(csvUrl, d3.autoType)

  /* 2 – Links array from CSV rows -------------------------------- */
  const links = raw.flatMap((d) => {
    const arr = []
    if (d.oil > 0) arr.push({ source: 'Oil', target: d.country, value: d.oil })
    if (d.ngl_condensate > 0)
      arr.push({ source: 'NGL & Condensate', target: d.country, value: d.ngl_condensate })
    return arr
  })

  /* 3 – Nodes + index map ---------------------------------------- */
  const nodeNames = Array.from(new Set(links.flatMap((l) => [l.source, l.target])))
  const nodes = nodeNames.map((name) => ({ name }))
  const nodeIndex = new Map(nodes.map((d, i) => [d.name, i]))

  /* 4 – Remap links to indices ----------------------------------- */
  const skLinks = links.map((l) => ({
    source: nodeIndex.get(l.source),
    target: nodeIndex.get(l.target),
    value: l.value,
  }))

  /* 5 – Color scale ------------------------------------ */
  const color = d3
    .scaleOrdinal()
    .domain(nodeNames)
    .range(nodeNames.map((_, i) => d3.interpolateRainbow(i / nodeNames.length)))

  /* 6 – Layout ---------------------------------------------------- */
  const { clientWidth: w } = container.value
  const sankeyGen = sankey().nodeWidth(22).nodePadding(12).size([w, height])

  const { nodes: skNodes, links: skLinksLaid } = sankeyGen({
    nodes: nodes.map((d) => ({ ...d })), // clone for mutability
    links: skLinks,
  })

  /* 7 – SVG scaffold --------------------------------------------- */
  const svgEl = d3
    .select(svg.value)
    .attr('viewBox', [0, 0, w, height])
    .attr('font-family', 'sans-serif')

  // Embedded title (helps when exporting the SVG)
  svgEl
    .append('text')
    .attr('x', w / 2)
    .attr('y', 18)
    .attr('text-anchor', 'middle')
    .attr('font-weight', 600)
  // .text('2024 Oil & NGL/Condensate Exports')

  /* 8 – Links ----------------------------------------------------- */
  svgEl
    .append('g')
    .attr('fill', 'none')
    .selectAll('path')
    .data(skLinksLaid)
    .join('path')
    .attr('d', sankeyLinkHorizontal())
    .attr('stroke', (d) => color(d.source.name))
    .attr('stroke-width', (d) => Math.max(1, d.width))
    .attr('stroke-opacity', 0.35)
    .on('mouseenter', (evt, d) =>
      showTip(`${d.source.name} → ${d.target.name}: ${format(d.value)}`, evt),
    )
    .on('mousemove', showTip)
    .on('mouseleave', hideTip)

  /* 9 – Nodes ----------------------------------------------------- */
  svgEl
    .append('g')
    .selectAll('rect')
    .data(skNodes)
    .join('rect')
    .attr('x', (d) => d.x0)
    .attr('y', (d) => d.y0)
    .attr('width', (d) => d.x1 - d.x0)
    .attr('height', (d) => d.y1 - d.y0)
    .attr('fill', (d) => color(d.name))
    .attr('stroke', '#000')
    .on('mouseenter', (evt, d) => showTip(`${d.name}: ${format(d.value)}`, evt))
    .on('mousemove', showTip)
    .on('mouseleave', hideTip)

  /* 10 – Labels --------------------------------------------------- */
  svgEl
    .append('g')
    .attr('font-size', 12)
    .selectAll('text')
    .data(skNodes)
    .join('text')
    .attr('x', (d) => (d.x0 < w / 2 ? d.x1 + 6 : d.x0 - 6))
    .attr('y', (d) => (d.y0 + d.y1) / 2)
    .attr('dy', '0.35em')
    .attr('text-anchor', (d) => (d.x0 < w / 2 ? 'start' : 'end'))
    .text((d) => `${d.name} (${format(d.value)})`)
})

/* 11 – Clean-up --------------------------------------- */
onUnmounted(() => tooltip.value?.remove?.())
</script>

<style scoped>
figure {
  /* keeps the figure height consistent */
  height: 600px;
  width: 100%;
  overflow: visible;
}
</style>
