The **attached file (`utils_generate_river_flow.py`)** generates **enhanced river flow data** for **Sections 9 and 10** of the **French Broad River**, incorporating **realistic seasonal trends, flood risks, and additional rafting-related metrics**.

---

### **📊 Generated River Data Fields**
| Field                 | Description |
|-----------------------|-------------|
| `date`               | The date for which the river data applies (May 24 – Sept 2, 2024). |
| `river_flow`         | Flow rate in **cubic feet per second (cfs)** (800 - 4000+ cfs). |
| `water_level`        | Water height in **feet** (2.5 - 7.0 ft). |
| `water_temperature`  | Water temperature in **Fahrenheit** (55 - 75°F). |
| `rapid_difficulty`   | Class rating based on river flow (`Class II`, `Class III`, `Class IV`). |
| `recent_precipitation` | Rainfall in **inches** over the past 24 hours (0 - 2.5 in). |
| `river_condition`    | Safety assessment (`Safe`, `Moderate Risk`, `High Risk`, `Flood Stage`). |
| `water_visibility`   | **Clarity** based on river flow & rainfall (`Clear`, `Moderate`, `Poor`). |
| `debris_level`       | **Floating debris level** based on rainfall (`Low`, `Moderate`, `High`). |

---

### **🔎 How It Works**
1. **Flow Rate (`river_flow`)**
   - **Spring (May–June):** Higher due to **snowmelt/runoff** (1200-4000 cfs).
   - **Peak Summer (July–August):** Typically lower (800-2800 cfs).
   - **Transition Periods (May/Sept):** Moderate levels (1000-3200 cfs).
   - **10% chance of extreme spikes** (**+1000-2000 cfs**) simulating **storm-driven surges**.

2. **Water Level (`water_level`)**
   - Random float **between 2.5 - 7.0 feet**.
   - Correlates with flow rate.

3. **Rapid Difficulty (`rapid_difficulty`)**
   - **< 1000 cfs** → `Class II` (Beginner Rapids)
   - **1000 - 2500 cfs** → `Class III` (Intermediate Rapids)
   - **> 2500 cfs** → `Class IV` (Advanced Rapids)

4. **Flood Risk (`river_condition`)**
   - **> 4000 cfs or > 2.0 inches of rain** → `"Flood Stage"` 🚨
   - **3000 - 4000 cfs or >1.5 inches of rain** → `"High Risk"`
   - **2000 - 3000 cfs** → `"Moderate Risk"`
   - **< 2000 cfs** → `"Safe"`

5. **Water Visibility (`water_visibility`)**
   - **Clear:** Low flow, little rain.
   - **Moderate:** Mid-range flow, moderate rain.
   - **Poor:** **High flow or >1.5 inches of rain**.

6. **Debris Level (`debris_level`)**
   - **Low:** Minimal rainfall.
   - **Moderate:** **0.5 - 1.5 inches of rain**.
   - **High:** **>1.5 inches of rain** (floating branches, debris).

---

### **📂 Example River Data Entry**
```json
{
    "date": "2024-06-22",
    "river_flow": 3900,
    "water_level": 6.3,
    "water_temperature": 69,
    "rapid_difficulty": "Class IV",
    "recent_precipitation": 1.8,
    "river_condition": "High Risk",
    "water_visibility": "Poor",
    "debris_level": "High"
}
```
### **🌊 Breakdown**
- **Flow Rate:** 3900 cfs → `Class IV Rapids` (Very challenging).
- **Water Level:** 6.3 ft → High but not extreme.
- **Precipitation:** 1.8 inches → Heavy rainfall.
- **Flood Condition:** `"High Risk"` 🚨.
- **Water Visibility:** `"Poor"` (due to flow + rain).
- **Debris Level:** `"High"` (floating obstacles).

---

### **📌 Summary**
The script **simulates realistic river conditions** for rafting:
✅ **Seasonal water flow trends** (spring melt, summer drop).  
✅ **Extreme weather events** (flooding, rapid spikes).  
✅ **Hydrology impacts** (water clarity & debris).  
✅ **Dynamic risk levels** (safe to flood stage).  

This **enhanced dataset** will improve **rafting trip planning** and **safety analysis**. 🌊🚣‍♂️  
