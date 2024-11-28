# Dynamic Sankey Diagram Dashboard

This project is a dynamic dashboard built using Dash, Plotly, and Dash Bootstrap Components. The dashboard displays a **Sankey Diagram** to visualize energy flow dynamically, along with a table showing the "Last Heard" timestamps for connected sensors.

---

- Sankey diagrams are a data visualisation technique or flow diagram that emphasizes flow/movement/change from one state to another or one time to another, in which the width of the arrows is proportional to the flow rate of the depicted extensive property.
- Here sankey diagram is used to represent energy consumed by different ACs/Buildings/Blocks in a College Campus.

<img width="940" alt="ss1" src="https://github.com/yatee-singh/sankey-diagram/assets/101913573/3ab2597d-3cc6-4832-b365-2a5cbf392d5c">

---
## Main Components and Working of the Project

The project is designed as an interactive visualization tool that incorporates real-time data and user interactions to analyze and display connections between sensor devices. Below is a breakdown of its key components and their functionalities:

---

### 1. **Sankey Diagram**
The Sankey diagram is the core visual component of the project, providing a graphical representation of flows between nodes. 

#### Features:
- **Nodes**: Represent sensor devices or data sources.
- **Links**: Represent the data flow between nodes, with link thickness proportional to the data volume.
- **Interactivity**: Users can interact with nodes and links to:
  - Highlight specific connections.
  - Hide or unhide selected links.
  - Group or ungroup nodes for simplified or detailed views.

#### Working:
- Data is fetched from a backend source or a predefined dataset.
- Links and nodes are dynamically rendered to reflect the latest updates.
- User interactions trigger visual or structural updates to the diagram.

---

### 2. **Real-Time Data Updates**
The system integrates real-time data fetching to ensure the displayed information is up-to-date.

#### Features:
- **Interval Updates**: Data is refreshed every 5 minutes automatically.
- **User-Triggered Refresh**: Allows users to manually fetch the latest data if required.
- **Device-Specific Data**: Each device's current status and metrics are displayed in the device table.

#### Working:
- A background process or API call fetches data from connected sensors or a database.
- The fetched data updates the visualization and device table without requiring a page refresh.

---

### 3. **Device Table**
A tabular component that complements the Sankey diagram by showing detailed information about each device.

#### Features:
- Lists all active sensors and their latest fetched data.
- Displays metrics such as:
  - Device status (active/inactive).
  - Timestamp of the last update.
  - Any anomalies or alerts associated with the device.
- Allows for quick reference and troubleshooting.

---

### 4. **User Interaction Controls**
The project provides various controls to customize the visualization:

#### Navigation Buttons:
- **Left Button**: Moves the time window backward by 5 minutes, allowing users to view historical data.
- **Right Button**: Moves the time window forward by 5 minutes to return to the latest data.

#### Dropdown Actions:
- **Highlight**: Brings attention to a selected link or set of links in the Sankey diagram.
- **Hide/Unhide**: Enables toggling the visibility of certain connections for a clearer view.
- **Group/Ungroup**: Lets users group related nodes into a single node or split them for a detailed view.

---

### Workflow
1. **Initialization**:
   - The project loads the initial data and renders the Sankey diagram along with the device table.
2. **Real-Time Updates**:
   - Every 5 minutes, new data is fetched, and the visualization is updated.
3. **User Interactions**:
   - Users interact with the Sankey diagram using controls like navigation buttons and dropdown actions.
4. **Analysis and Reporting**:
   - Users analyze connections and sensor performance using the visual and tabular data.

---

This setup ensures a dynamic and user-friendly interface for analyzing and monitoring sensor data flow effectively.


---

## Installation

### Prerequisites

Ensure you have the following installed:
- Python 3.7+
- Required Python libraries:
  ```bash
  pip install dash plotly pandas dash-bootstrap-components requests pytz dash-extensions

## Dependencies:
- Python (3.11) [python](https://www.python.org/downloads/)
- dash (2.1.30) [install dash](https://dash.plotly.com/installation)
- pandas (1.5.2) [install pandas](https://pandas.pydata.org/pandas-docs/version/1.3.2/getting_started/install.html)
- plotly (5.16.1) [install plotly](https://plotly.com/python/getting-started/)
- numpy (1.24.1) [install numpy](https://www.geeksforgeeks.org/how-to-install-numpy-on-windows/)
- dash_extensions (1.0.4) [install dash-dependencies](https://www.dash-extensions.com/getting_started/installation)

# Working

- The dashboard provides the user 6 operations to customize the sankey diagram:
<img width="820" alt="ss8" src="https://github.com/yatee-singh/sankey-diagram/assets/101913573/7a08c170-dae9-4336-bfe4-feff6dd6c5ea">

# 1. Highlighting and Un-highlighting
- You have to select the link to be highlighted and choose "Highlight from the drop-down menu"

<img width="944" alt="ss2" src="https://github.com/yatee-singh/sankey-diagram/assets/101913573/7b72e93c-7a16-4303-91e1-322687dc11e9">

<img width="943" alt="ss3" src="https://github.com/yatee-singh/sankey-diagram/assets/101913573/5f326443-4ea1-48ac-9688-1715579408d0">

# 2. Hiding
- User has to select the link to be removed
<img width="941" alt="ss4" src="https://github.com/yatee-singh/sankey-diagram/assets/101913573/b423f8dd-ef07-4b51-9444-750c2e68cfca">

# 3. Un-hide
- User has to simply select un-hide from the from drop-down menu to reveal all the hidden links

  

# 4. Grouping and Un-grouping
- User need to click on all the links to be grouped while holding the shift key and then choose Group.
- To un-group user can click on anywhere on the group and click on un-group
  
<img width="941" alt="ss10" src="https://github.com/yatee-singh/sankey-diagram/assets/101913573/10efe3c7-c8af-46bb-a153-c1a2bc68ca2f">
<img width="940" alt="ss11" src="https://github.com/yatee-singh/sankey-diagram/assets/101913573/01f2d261-7670-4311-bf1f-770c3842f7fb">

# Filtering data by time

- User can change the time-stamp of the data being visualised by clicking the left and right buttons
- Left button goes back 5hours in time, whereas right button goes 5hours forward in time
- Right button gets disabled when no data is available
- 
 <img width="940" alt="ss7" src="https://github.com/yatee-singh/sankey-diagram/assets/101913573/5da3409b-5ad9-4d2c-ad0c-fceb4ed69e67">

# Last heard data

- Gives a report about the recent data received from each sensor
- Fetches an aggregate of two months of data, finds the unique devices in them and sorts the latest data for each device 

<img width="568" alt="sop1" src="https://github.com/yatee-singh/sankey-diagram/assets/101913573/93771f5e-5b5a-4954-bf0d-4b4b1f90b15a">

## Running the script on server
- Copy the file main.py to the server.
- Install all the dependencies mentioned above.
  
- ### Possible errors while installing dependencies:
  -  [pip install fail - Error compiling Cython](https://github.com/numpy/numpy/issues/24377)
  -  [importerror "No Module named Setuptools"](https://stackoverflow.com/questions/14426491/python-3-importerror-no-module-named-setuptools)
 
- ### Running script without ssh connection
    - install [screen](https://phoenixnap.com/kb/how-to-use-linux-screen-with-commands#:~:text=1%20Commands%20to%20Start%20Screen.%20The%20tool%20will,Reattach%20to%20Screen.%20...%205%20Customizing%20Screen.%20)
    - start a new screen session ( $screen )
    - Run the python prograMM ( $python3 main.py )
    - Detach from the session ( Ctrl + a followed by d)
    - Exit ssh connection.
      




