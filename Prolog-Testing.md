### Test Setup

**Load the Rules File:**

- At the Prolog prompt (`?-`), load your `recommendation_rules.pl` file:
  ```
  [recommendation_rules].
  ```

3. **Check Initial State:**
   - It's a good practice to start with a clean state.

### Actual Test Cases

#### Standard Test Cases

Here are some example test cases to cover a range of functionality:

1. **Test Case 1: Basic Soccer Facility Recommendation**

   - **Description ->** Recommend a soccer facility in La Paternal for a moderate budget.
   - **Query:**
     ```
     recommend_facility(soccer, la_paternal, moderate, all_levels, Facility).
     ```
   - **Expected Result:** A list of soccer facilities in La Paternal with a moderate budget.
   - **Actual Result:** Facility = club_atletico_argentinos_juniors

2. **Test Case 2: Time Availability**

   - **Description:** Recommend a tennis facility in Palermo available all day.
   - **Query:**
     ```
     recommend_facility(tennis, palermo, moderate, all_levels, all_day, Facility).
     ```
   - **Expected Result:** Tennis facilities in Palermo available all day.
   - **Actual Result:** Facility = club_gimnasia_y_esgrima_de_buenos_aires .

3. **Test Case 3: Indoor/Outdoor Preference**

   - **Description:** Recommend an outdoor rugby facility in Villa Crespo.
   - **Query:**
     ```
     recommend_facility(rugby, villa_crespo, moderate, all_levels, all_day, outdoor, Facility).
     ```
   - **Expected Result:** Outdoor rugby facilities in Villa Crespo.
   - **Actual Result:** Facility = club_atletico_atlanta_rugby .

4. **Test Case 4: Multiple Results query**

   - **Description:** Recommend a soccer facility in specific location.
   - **Query:**

     ```
     recommend_facility(soccer, palermo, moderate, all_levels, Facility).

     ```

   - **Expected Result:** List of the recommended soccer facilities.
   - **Actual Result:**
     Facility = club_gimnasia_y_esgrima_de_buenos_aires ;
     Facility = asociacion_argentina_de_tenis ;
     Facility = club_gimnasia_y_esgrima_de_buenos_aires ;
     Facility = asociacion_argentina_de_tenis ;

#### Edge Test Cases

1. **Test Case 4: Non-Existent Sport**

   - **Description:** Attempt to find a facility for a non-existent sport.
   - **Query:**
     ```
     recommend_facility(quantum_leaping, palermo, moderate, all_levels, Facility).
     ```
   - **Expected Result:** No matching facilities or false
   - **Actual Result:** false.

2. **Test Case 5: Extremely Specific Request**
   - **Description:** Request a facility with very specific criteria.
   - **Query:**
     ```
     recommend_facility(polo, palermo, high_end, all_levels, all_day, outdoor, group_individual, competitive_recreational, equipment_rental, yes, Facility).
     ```
   - **Expected Result:** Specific facilities that match these criteria or `false` if none exist.
   - **Actual Result:** Facility = campo_argentino_de_polo .
