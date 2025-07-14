<template>
  <main class="info max-w-screen-xl mx-auto px-8">
    <IntroSection />

    <StorySection
      sectionId="norway-rise"
      title="Norway’s Rise"
      class="max-w-screen-xl mx-auto px-8"
    >
      <p>-</p>
      <!-- <p>[MultiLineChart, StackedBarChart]</p> -->
      <p class="text-sm text-gray-600 mb-4">
        This chart shows Norway’s annual production of Oil, Gas, Condensate, and NGL from 1971 to
        the latest finalized year, measured in million Sm³ oil equivalents. Oil production peaked in
        the early 2000s and has gradually declined, while gas production surpassed oil around 2010
        and continues to rise. Although NGL and condensate make up a smaller portion of the total,
        their output has remained relatively stable. Overall, the chart reflects a significant shift
        in Norway’s energy profile, with gas emerging as the country’s leading hydrocarbon export.
      </p>
      <LineChart />
      <zoomableStackedBarChart />
    </StorySection>

    <StorySection sectionId="regional-dynamics" title="Regional Dynamics">
      <!-- <p>[ChoroplethMap, BarChart]</p> -->
      <p>-</p>
      <h3>Production per seas</h3>
      <p class="text-gray-600 mb-4 w-full">
        At the close of 2024, Norway’s offshore story is still all about the North Sea: it delivers
        close to nine-tenths of the nation’s total output, with the Norwegian Sea playing a
        supporting role and the Barents Sea barely moving the needle. Looking down the decades,
        overall volumes are off their early-2000s oil peak, yet they’ve held up because gas -now the
        biggest slice of the pie- has risen as oil wanes. In short, production is steady but
        gas-heavy, and it’s still overwhelmingly a North Sea game.
      </p>
      <div
        style="display: flex; flex-direction: row; gap: 32px; align-items: flex-start; width: 100vw"
      >
        <div style="flex: 0 0 400px; min-width: 400px">
          <div style="flex: 0"></div>
          <ChoroplethMap
            v-if="geojson"
            :geojson="geojson"
            :productionTotals="productionTotals"
            @update:selectedSeas="selectedSeas = $event"
          />
        </div>
        <div style="flex: 2">
          <BarChartRegion :selectedSeas="selectedSeas" />
        </div>
      </div>
      <HeatMap />
    </StorySection>

    <StorySection sectionId="export-machine" title="Export Machine">
      <p>-</p>
      <!-- <p>[SankeyChart, StackedBarChart, LollipopChart]</p> -->
      <p>
        From these charts, we can see that Norway’s petroleum exports have grown steadily over the
        decades, with noticeable peaks in recent years driven mostly by natural gas. In 2024, oil
        remains Norway’s biggest export by volume, going mainly to European neighbors like the
        Netherlands and the UK, while condensate and NGL exports are smaller but still significant.
        Globally, Norway’s oil production is modest compared to giants like the U.S. and Saudi
        Arabia, placing it among the lower producers on the 2023 list. Altogether, the graphs show
        how Norway’s petroleum industry plays a steady but smaller role in the global market, while
        remaining crucial for European energy supplies.
      </p>
      <StackedBarChart />
      <div
        style="display: flex; flex-direction: row; gap: 32px; align-items: flex-start; width: 100vw"
      >
        <div style="flex: 0 0 400px; min-width: 400px">
          <SankeyChart />
        </div>
        <div style="flex: 2">
          <LollipopChart />
        </div>
      </div>
    </StorySection>

    <!-- <StorySection sectionId="global-comparison" title="Global Comparison">
      <p>[Butterfly & Dumbbell Chart, SlopeChart]</p>
    </StorySection> -->

    <StorySection sectionId="future-outlook" title="Future Outlook">
      <p>-</p>
      <!-- <p>[PieChart]</p> -->
      <div
        style="display: flex; flex-direction: row; gap: 32px; align-items: flex-start; width: 100vw"
      >
        <div style="flex: 0 0 400px; min-width: 400px">
          <PieChartRemainingReserves />
        </div>
        <div style="flex: 2">
          <h2>Remaining reserves</h2>
          <p style="max-width: 58%">
            Looking at Norway’s remaining reserves as of the end of 2024, it’s clear the North Sea
            still rules the game, holding about 70% of the country’s total oil and gas resources.
            The Norwegian Sea comes next, with around 18% of the reserves, and the Barents Sea
            trails behind at roughly 11%. Oil makes up the biggest chunk in the North Sea, but
            there’s also a solid amount of gas there. The Barents and Norwegian Seas, while smaller
            players, still carry meaningful volumes, especially gas in the Norwegian Sea. All in
            all, Norway’s future energy story stays strongly tied to the North Sea, but there’s
            potential for more development up north if markets and technology make it worthwhile.
          </p>
        </div>
      </div>
    </StorySection>

    <Footer />
    <AboutSection />
  </main>
</template>

<script setup>
import IntroSection from './components/UI/IntroSection.vue'
import StorySection from './components/UI/StorySection.vue'
import AboutSection from './components/UI/AboutSection.vue'
import Footer from './components/UI/Footer.vue'

import LineChart from './components/charts/LineChart.vue'
import zoomableStackedBarChart from './components/charts/zoomableStackedBarChart.vue'
import ChoroplethMap from './components/charts/ChoroplethMap.vue'
import BarChartRegion from './components/charts/BarChartRegion.vue'
import HeatMap from './components/charts/HeatMap.vue'

import geojsonUrl from '/data/processed/sea_production.geojson?url'
import productionPerSea from '/data/processed/production_per_sea.csv?raw'

import StackedBarChart from './components/charts/StackedBarChart.vue'
import SankeyChart from './components/charts/SankeyChart.vue'
import LollipopChart from './components/charts/LollipopChart.vue'

import PieChartRemainingReserves from './components/charts/PieChartRemainingReserves.vue'

import { ref, onMounted } from 'vue'
import * as d3 from 'd3'

const selectedSeas = ref([])

const geojson = ref(null)

const productionTotals = ref({})

onMounted(async () => {
  const res = await fetch(geojsonUrl)
  geojson.value = await res.json()
})

onMounted(() => {
  const csvData = d3.csvParse(productionPerSea)
  const totals = {}

  csvData.forEach((row) => {
    const sea = row.area
    const total = +row.total_oil_equivalents || 0

    totals[sea] = (totals[sea] || 0) + total
  })

  productionTotals.value = totals
})
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
  font-family: system-ui, sans-serif;
}
.info {
  max-width: 80%;
  height: 500px;
  margin: 0 auto; /* horizontal centering */
  /* display: flex; */
  justify-content: center; /* horizontal alignment of children */
  align-items: center; /* vertical alignment of children */
  overflow: visible;
}
</style>
