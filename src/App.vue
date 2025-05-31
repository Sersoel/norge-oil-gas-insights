<template>
  <main class="max-w-6xl mx-auto">
    <IntroSection />

    <StorySection sectionId="norway-rise" title="Norway’s Rise">
      <p>[MultiLineChart]</p>
      <LineChart />
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
