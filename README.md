# 🇳🇴 Norway’s Energy Story: Unveiling Insights

> **Platform:** Interactive Web Application  
> **Stack:** Vue.js 3 + D3.js v7 + Python (data wrangling)  
> **Deployment:** GitHub Pages

---

## 🎯 Project Overview

**Norway’s Energy Story** is an interactive data storytelling platform revealing how Norway transformed into a global energy powerhouse. Through dynamic, interactive charts and clean UX design, the platform explores:

- The evolution of Norway’s oil, gas, condensate, and NGL production over time
- Regional differences among the Barents, North, and Norwegian Seas
- Norway’s export flows and trading partners
- How Norway compares globally to other major energy producers
- Insights into Norway’s remaining reserves and future potential

This project is designed for **non-technical users, policymakers, students, and the general public** who want to understand both the data and its story.

---

## 📚 Narrative Sections

### Norway’s Rise

Shows Norway’s annual production of Oil, Gas, Condensate, and NGL from 1971 to the latest finalized year, measured in million Sm³ oil equivalents.

- Oil production peaked in the early 2000s and has gradually declined.
- Gas production surpassed oil around 2010 and continues to rise.
- NGL and condensate remain smaller but stable contributors.
- The chart reflects a significant shift in Norway’s energy profile, with gas emerging as the leading hydrocarbon export.

---

### Regional Dynamics

At the close of 2024, Norway’s offshore story is still overwhelmingly about the North Sea:

- The North Sea delivers close to 90% of the nation’s total output.
- The Norwegian Sea plays a supporting role.
- The Barents Sea contributes relatively minor volumes.

Looking over decades, production volumes are lower than the early-2000s peak, but have held up thanks to the rise of gas. In short, production is steady but gas-heavy, and still overwhelmingly a North Sea story.

Features:

- Choropleth map showing total production per sea region.
- Interactive bar charts revealing field-level production within each sea region.

---

### Export Machine

Norway’s petroleum exports have grown steadily, with noticeable peaks driven mostly by natural gas:

- In 2024, oil remains Norway’s largest export by volume, primarily to European markets like the Netherlands and the UK.
- Condensate and NGL exports are smaller but significant.
- Norway’s oil production is modest globally, but its gas exports are crucial for European supply security.

Charts included:

- **Sankey Diagram:** visualizes flows from each petroleum product to export destinations.
- **Stacked Bar Chart:** shows how each country’s imports split among oil, gas, NGL, and condensate.
- **Bubble Map:** displays proportional export volumes by country on a geographic map.

---

### Global Comparison

This section puts Norway into context globally:

- Norway remains a significant European producer but smaller on the global stage compared to giants like the USA, Russia, and Saudi Arabia.
- Global trends reveal shifts in production dynamics among OPEC and non-OPEC countries.

Charts include:

- **Butterfly Chart:** compares Norway side-by-side with top producers in the latest year.
- **Dumbbell Chart:** shows change in total production from 2000 to 2024 for each country.
- **Slope Chart:** visualizes rank changes among countries over time.

---

### Future Outlook

Currently focuses on **Norway’s remaining reserves** rather than a dedicated renewable energy view.

- The North Sea still dominates, holding about 70% of the country’s total oil and gas reserves.
- The Norwegian Sea comes next, with around 18%.
- The Barents Sea trails behind at roughly 11%.
- Oil makes up the largest chunk in the North Sea, though there’s also significant gas.
- The Barents and Norwegian Seas carry meaningful volumes, especially gas.

All in all, Norway’s future energy story remains closely tied to the North Sea, but there’s potential for further development in the north if markets and technology make it worthwhile.

_(Note: Future renewable-focused visualizations may be added in future versions of this project.)_

---

## 📊 Visualizations Overview

| Narrative Section | Charts Implemented               | Purpose                                        |
| ----------------- | -------------------------------- | ---------------------------------------------- |
| Norway’s Rise     | Multi-line chart                 | Production trends from 1971–2024               |
| Regional Dynamics | Choropleth map + bar chart       | Production differences by sea region and field |
| Export Machine    | Sankey, stacked bar, bubble map  | Product exports by country and volume          |
| Global Comparison | Butterfly, dumbbell, slope chart | Norway vs. global producers                    |
| Future Outlook    | Donut chart                      | Remaining reserves distribution                |

---

## 📚 Data Sources

- Norwegian Petroleum Directorate (NPD)
- SODIR
- World energy datasets
- Custom CSVs prepared with Python
- **Shapefile Data:**

  > Flanders Marine Institute (2024). The intersect of the Exclusive Economic Zones and IHO sea areas, version 5. Available online at https://www.marineregions.org/. https://doi.org/10.14284/699

  This dataset is licensed under a Creative Commons Attribution 4.0 International License.  
  **Note:** This project does _not_ redistribute the original shapefile. Instead, it includes a processed GeoJSON derived from the original data.

---

## 🧩 Project Structure

```
/public
  └── assets/
      └── data/
          ├── *.csv
          ├── *.geojson
/src
  └── components/
        └── charts/
        └── UI/
  └── App.vue
  └── main.js
```

---

## ⚙️ How to Run Locally

Clone the repo:

```bash
git clone https://github.com/sersoel/norway-energy-story.git
cd norway-energy-story
npm install
npm run dev:full
```

Visit:

```
http://localhost:5173
```

---

## 🎨 UX & Design Principles

- Progressive disclosure: start simple, let users dig deeper
- Colorblind-friendly palettes following WCAG AA
- Interactive tooltips and transitions for engagement
- Lazy-loaded charts for performance optimization
- Semantic, modular Vue components
- Narrative-driven chart choices inspired by Munzner and Schwabish
- Designed for clarity and non-technical audiences

---

## 🗂 Academic References

- Tamara Munzner — _Visualization Analysis & Design_
- Jonathan Schwabish — _Better Data Visualizations_
- Andy Kirk — _Data Visualisation Handbook_
- Scott Murray — _Interactive Data Visualization for the Web_
- Cole Nussbaumer Knaflic — _Storytelling with Data_

---

## ✉️ Contact

- [GitHub](https://github.com/Sersoel/)
- [LinkedIn](https://www.linkedin.com/in/soheil-samadian)

---

## 📜 License

MIT License

---

_Data last updated: 15 July 2025_
