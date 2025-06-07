<template>
  <main class="max-w-6xl mx-auto">
    <IntroSection />

    <StorySection sectionId="norway-rise" title="Norway’s Rise">
      <p>-</p>
      <p>[MultiLineChart]</p>
      <p class="text-sm text-gray-600 mb-4">
        This chart shows Norway’s annual production of Oil, Gas, Condensate, and NGL from 1971 to
        the latest finalized year, measured in million Sm³ oil equivalents. Oil production peaked in
        the early 2000s and has gradually declined, while gas production surpassed oil around 2010
        and continues to rise. Although NGL and condensate make up a smaller portion of the total,
        their output has remained relatively stable. Overall, the chart reflects a significant shift
        in Norway’s energy profile, with gas emerging as the country’s leading hydrocarbon export.
      </p>
      <LineChart />
      <p>-</p>
    </StorySection>

    <StorySection sectionId="regional-dynamics" title="Regional Dynamics">
      <p>[ChoroplethMap, BarChart]</p>
    </StorySection>

    <StorySection sectionId="export-machine" title="Export Machine">
      <p>[SankeyChart, StackedBarChart, BubbleMap]</p>
    </StorySection>

    <StorySection sectionId="global-comparison" title="Global Comparison">
      <p>[Butterfly & Dumbbell Chart, SlopeChart]</p>
    </StorySection>

    <StorySection sectionId="future-outlook" title="Future Outlook">
      <p>[Line + Donut Chart]</p>
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
</script>
