# Storytelling Structure: Norway’s Energy Story

## Project Goal
Design a web-based interactive platform to visualize the evolution and future of Norway’s oil and gas sector for general audiences. The platform should be accessible, clean, and informative—focused on storytelling through data visualization.

---

## Narrative Arc (Inspired by Munzner’s Design Process)

### 1. Norway’s Rise: From Discovery to Dominance
**Question:** How has Norway’s energy production grown over time?  
**Chart Type:** Multi-line time series chart (1971–2024)

---

### 2. Regional Dynamics: Barents, North, and Norwegian Seas
**Question:** How does production differ by region and field?  
**Chart Type:** Choropleth map + bar chart comparisons

---

### 3. Export Machine: Where and What is Exported?
**Question:** What products are exported and to which destinations?  
**Chart Type:** Sankey diagram + stacked bar chart + bubble map

---

### 4. Global Comparison: Norway vs. the World
**Question:** How does Norway compare to other major producers?  
**Chart Type:** Butterfly chart + slope chart + dumbbell plot

---

### 5. Future Outlook: Sustainability & Transition
**Question:** Is Norway moving toward renewables?  
**Chart Type:** Line chart (CO₂, wind capacity trends) + donut chart

---

## Visual Page Structure (UX-Driven Layout)

This section outlines the Vue component-based layout matching the narrative arc.

```vue
<IntroSection />
  |-> Title, subtitle, data sources, and project overview

<StorySection id="norway-rise" />
  |-> Multi-line time series chart (year-wise production)

<StorySection id="regional-dynamics" />
  |-> Choropleth map + region-wise bar chart toggle

<StorySection id="export-machine" />
  |-> Sankey diagram + export bar chart + bubble map

<StorySection id="global-comparison" />
  |-> Butterfly + slope + dumbbell chart comparisons

<StorySection id="future-outlook" />
  |-> Renewables vs. fossil line chart + donut breakdown

<AboutSection />
  |-> Team members, acknowledgments, license