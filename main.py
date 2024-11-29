#create two variables for diplay and data fetch
#make a table component for last_heard

import dash
from dash import dcc, html,ctx,dash_table
from dash.dependencies import Input, Output,State
import plotly.graph_objects as go
import random
import requests
import pandas as pd
from datetime import datetime,timedelta,timezone
import dash
from dash import dcc, html

from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pytz
from dash_extensions import EventListener
# Create Dash app
app = dash.Dash(__name__)
event = {"event": "click", "props": ["shiftKey"]} 
ist_timezone = pytz.timezone("Asia/Kolkata")
src=[]
target=[]
value=[]
lables=[]
node_colors=[]
link_colors=[]
base_url="http://10.1.19.105:5000/energygrid2?"
color_code2="#4f0099"
color_code1="#e6ccff"
red="rgb(255, 153, 153)"
dark_red='rgb(255, 133, 102)'
purple='#e6ccff'
dark_purple='rgb(230, 153, 255)'
base_url="http://10.1.19.105:5000/energygrid2?"
base_url2="http://10.1.19.105:5000/tempgrid2?"
def make_req_url(t1,t2):
    url=base_url+'where={"$and":[{"_created":{"$gte":"'+t1+'"}},{"_created":{"$lt":"'+t2+'"}}]}&max_results=1440'
    return url


# Initial layout


# Create Dash app
app = dash.Dash(__name__)
initial_data = {
    "lab": ["Node A", "Node B", "Node C", "Node D"],
    "src": [0, 1, 0, 2],
    "tar": [2, 3, 3, 3],
    "val": [10, 5, 7, 3],
    "link_colors": ["rgba(100, 149, 237, 0.5)"] * 4,
    "node_colors": [], 
}
# App layout
app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "padding": "20px", "maxWidth": "1200px", "margin": "auto"},
    children=[
        html.H1("Dynamic Sankey Diagram Dashboard", style={"textAlign": "center", "marginTop": "20px"}),

        # Data Stores
        dcc.Store(id="open-time-store"),
        dcc.Store(id="display-time-store"),
        dcc.Store(id="initial"),
        dcc.Store(id="sankey-store", data={}),
        dcc.Store(id="branch-store", data=[]),
        dcc.Store(id="groups-store", data=[{}]),

        # Row for Buttons and Sankey Graph
        html.Div(
            style={"display": "flex", "alignItems": "center", "justifyContent": "center", "marginTop": "20px"},
            children=[
                # Left Button
                html.Button(
                    "◀",
                    id="left-button",
                    style={
                        "padding": "10px 15px",
                        "fontSize": "18px",
                        "borderRadius": "5px",
                        "backgroundColor": "#007bff",
                        "color": "white",
                        "border": "none",
                        "cursor": "pointer",
                    },
                ),
                # Sankey Graph
                  EventListener(
        html.Div([
             dcc.Graph(id="sankey-graph", style={"marginTop": "20px"})
                 
        ]),
        events=[event], logging=True, id="el", style={'flex': '1','width':'100%'}
    ),
                # Right Button
                html.Button(
                    "▶",
                    id="right-button",
                    style={
                        "padding": "10px 15px",
                        "fontSize": "18px",
                        "borderRadius": "5px",
                        "backgroundColor": "#28a745",
                        "color": "white",
                        "border": "none",
                        "cursor": "pointer",
                    },
                ),
            ],
        ),

        # Time Display
        html.Div(
            id="time-display",
            style={"textAlign": "center", "fontSize": "18px", "marginTop": "10px"},
        ),

        # Dropdown for Action Selection
        html.Div(
            [
                html.Label("Select Action:", style={"fontSize": "16px", "fontWeight": "bold", "display": "block"}),
                dcc.Dropdown(
                    id="action-dropdown",
                    options=[
                        {"label": "Highlight", "value": "highlight"},
                        {"label": "Hide", "value": "hide"},
                        {"label": "Un-hide", "value": "unhide"},
                        {"label": "Un-highlight", "value": "unhighlight"},
                        {"label": "Group", "value": "group"},
                        {"label": "Un-group", "value": "ungroup"},
                    ],
                    placeholder="Select an action",
                    style={"width": "50%", "margin": "10px auto"},
                ),
            ],
            style={"textAlign": "center", "marginTop": "20px"},
        ),

        # Error Display
        html.Div(
            id="error-display",
            style={"textAlign": "center", "fontSize": "18px", "marginTop": "10px", "color": "red"},
        ),

        # Data Table
        html.Div(
            style={"marginTop": "30px"},
            children=[
                html.H2("Sensor Data", style={"textAlign": "center", "marginBottom": "20px"}),
                dash_table.DataTable(
                    id="data-table",
                    columns=[
                        {"name": "Sensor_ID", "id": "id"},
                        {"name": "Last Heard", "id": "date"},
                    ],
                    style_table={"overflowX": "auto", "margin": "0 auto", "width": "80%"},
                    style_cell={
                        "textAlign": "center",
                        "padding": "10px",
                        "border": "1px solid #ddd",
                        "fontSize": "14px",
                    },
                    style_header={
                        "fontWeight": "bold",
                        "backgroundColor": "#f4f4f4",
                        "border": "1px solid #ddd",
                    },
                ),
            ],
        ),

        # Interval Component
        dcc.Interval(
            id="interval-component",
            interval=5 * 60 * 1000,  # 5 minutes
            n_intervals=0,
        ),
        dcc.Store(id="data-store"),
    ],
)




def fetch_updated_data():
    """Simulate fetching updated data with device_id and timestamp."""
    AC=["862174063954226", "862174063958375", "862174063940126"]
    TEMP=["862174063931455","860181065147800","862174063935829"]
    
    def make_req_url1(dev_id):
        url=base_url+'where={"Sensor_ID":"'+dev_id+'"}&sort=[("_created", -1)]&max_results=1'
        return url

    def make_req_url2(dev_id):
        url=base_url2+'where={"Sensor_ID":"'+dev_id+'"}&sort=[("_created", -1)]&max_results=1'
        return url
    data={'date':[],'id':[]}

    for dev_id in AC:
        url=make_req_url1(dev_id)
        r = requests.get(url) 
        data['id'].append(dev_id)
    # print(url)
        if r.status_code == 200:
            res=r.json()
            df = pd.DataFrame.from_dict(pd.json_normalize(res['_items']), orient='columns')
        # data[dev_id]=df['_created'].to_string()
            #print(df['_created'])
            date=datetime.strptime(df['Time_Stamp'].to_string()[5:15] + ' '+df['Time_Stamp'].to_string()[16:24] , "%Y-%m-%d %H:%M:%S")
            date = date.replace(tzinfo=timezone.utc)
            ist_date=date.astimezone(ist_timezone)
            print(ist_date)
            data['date'].append(ist_date)
        
        else:
            print("Failed to fetch data from the API. Status code:", r.status_code)
    
    for dev_id in TEMP:
        url=make_req_url2(dev_id)
        r = requests.get(url) 
        data['id'].append(dev_id)
    # print(url)
        if r.status_code == 200:
            res=r.json()
            print(res)
            df = pd.DataFrame.from_dict(pd.json_normalize(res['_items']), orient='columns')
        # data[dev_id]=df['_created'].to_string()
            #print(df['_created'])

            date=datetime.strptime(df['utc_datetime'].to_string()[5:15] + ' '+df['utc_datetime'].to_string()[16:24] , "%Y-%m-%d %H:%M:%S")
            ist_date=date.astimezone(ist_timezone)
            print(ist_date)
            data['date'].append(ist_date)
        
        else:
            print("Failed to fetch data from the API. Status code:", r.status_code)

    df2=pd.DataFrame(data)
 
    df_sorted = df2.sort_values(by='date', ascending=False)
    print(df2['date'])
    df_sorted['date'] = df_sorted['date'].dt.strftime("%B %d, %Y %I:%M %p %Z")
    print(df_sorted)
    json_serializable_data = df_sorted.to_dict(orient="records")
    print(json_serializable_data    )
    return json_serializable_data




def make_sankey_data(data):
    src=[]
    tar=[]
    val=[]
    lab=[]
    sankey_data = {
    "lab": [],
    "src": [],
    "tar": [],
    "val": [],
    "link_colors": [] ,
    "node_colors": [], 
}
    df = pd.DataFrame.from_dict(pd.json_normalize(data['_items']), orient='columns')
    lab=list(df.Device_ID.unique())
    lab.insert(0,"MAIN_SUPPLY")
    sankey_data["lab"]=lab
    #cretes power consumed column
    df['power'] = pd.to_numeric(df['Real_power'], errors='coerce')
    df['power'].fillna(0, inplace=True)

    #finds avg power consumption
    averaged_columns=df.groupby(['Device_ID'])[df.select_dtypes(include='number').columns].mean()

    #loads data for sankey diagram creation


    for r in averaged_columns.iterrows():
        
        src.append(0)
        tar.append(lab.index(r[0]))
        val.append(r[1]['power'])
    
    sankey_data["src"]=src
    sankey_data["tar"]=tar
    sankey_data["val"]=val
    link_color = [color_code1]*len(src)# color of the links
    node_colors = [color_code2]*len(lab)
    sankey_data["link_colors"]=link_color
    sankey_data["node_colors"]=node_colors
    return sankey_data

# Callback to update the Sankey diagram and interval value
@app.callback(
    [Output("sankey-store", "data"),Output("time-display", "children"),Output("error-display", "children"),Output('open-time-store', 'data',allow_duplicate=True)
     ,Output('display-time-store', 'data',allow_duplicate=True),Output('initial', 'data',allow_duplicate=True)],
    [Input('left-button', 'n_clicks'),
     Input('right-button', 'n_clicks')
     ,Input("interval-component", "n_intervals")],
 
     State('open-time-store', 'data'),
     State('display-time-store', 'data'),
     State('initial', 'data'),
    prevent_initial_call='initial_duplicate'
)

def update_sankey_and_interval(decrease_clicks,increase_clicks,n_intervals,stored_time,display_time,initial):
    
    print(decrease_clicks,increase_clicks,n_intervals,display_time,initial)
    error=""
    if(n_intervals ==0 and initial!="false"):
        print(initial)
        current_time = datetime.now(timezone.utc)
        current_time_display = datetime.now()
        current_time += timedelta(minutes=5)
        t1=current_time-timedelta(minutes=5)
        t2=current_time
        url=make_req_url((t1-timedelta(minutes=3)).strftime('%a, %d %b %Y %H:%M:%S GMT'),(t2-timedelta(minutes=3)).strftime('%a, %d %b %Y %H:%M:%S GMT'))
        r = requests.get(url) 
        if r.status_code == 200:
            data = r.json()
        else:
            print("Failed to fetch data from the API. Status code:", r.status_code)
            error="Failed to fetch data from the API. Status code:"
    
        sankey_data={}
        if data['_items']!=[]:
            sankey_data=make_sankey_data(data)
            
        else:
            error="No data for the given time"

        stored_time=current_time.strftime('%Y-%m-%d %H:%M:%S')
        display_time=current_time_display.strftime('%Y-%m-%d %H:%M:%S')
        print("111111111111",stored_time)
        
        return [sankey_data,f"{display_time}",error,stored_time,display_time,"false"]
        
    elif "left-button" == ctx.triggered_id or "right-button" == ctx.triggered_id :
        print("22222222")
        current_time = datetime.strptime(stored_time, '%Y-%m-%d %H:%M:%S')
        current_time_display=datetime.strptime(display_time, '%Y-%m-%d %H:%M:%S')

    
        if "left-button" == ctx.triggered_id:
            current_time-=timedelta(minutes=5)
            current_time_display-=timedelta(minutes=5)
            t1=current_time-timedelta(minutes=5)
            t2=current_time
        
        else:
            current_time+=timedelta(minutes=5)
            current_time_display+=timedelta(minutes=5)
            t1=current_time-timedelta(minutes=5)
            t2=current_time

            
        url=make_req_url((t1-timedelta(minutes=3)).strftime('%a, %d %b %Y %H:%M:%S GMT'),(t2-timedelta(minutes=3)).strftime('%a, %d %b %Y %H:%M:%S GMT'))
        print("URLLLLLLLLL IUSSSSSSSS",url)

        #fetching data and making lab,sec,tar,val
        r = requests.get(url) 
    
        print(url)
        if r.status_code == 200:
            data = r.json()
        else:
            print("Failed to fetch data from the API. Status code:", r.status_code)
            error="Failed to fetch data from the API. Status code:"
        
        sankey_data={}
        if data['_items']!=[]:
            sankey_data = make_sankey_data(data)
        else:
            error="No data for the given time"
        print(len(src))

        stored_time=current_time.strftime('%Y-%m-%d %H:%M:%S')
        display_time=current_time_display.strftime('%Y-%m-%d %H:%M:%S')

        return [sankey_data,f" {display_time}",error,stored_time,display_time,"false"]

        
    
    else:
        print("333333333")
        current_time = datetime.strptime(stored_time, '%Y-%m-%d %H:%M:%S')
        current_time_display=datetime.strptime(display_time, '%Y-%m-%d %H:%M:%S')
        current_time += timedelta(minutes=5)
        current_time_display+=timedelta(minutes=5)
        t1=current_time-timedelta(minutes=5)
        t2=current_time
        url=make_req_url((t1-timedelta(minutes=3)).strftime('%a, %d %b %Y %H:%M:%S GMT'),(t2-timedelta(minutes=3)).strftime('%a, %d %b %Y %H:%M:%S GMT'))
        
        print("URLLLLLLLLL IUSSSSSSSS",url)



        #fetching data and making lab,sec,tar,val
        r = requests.get(url) 
        if r.status_code == 200:
            data = r.json()
        else:
            print("Failed to fetch data from the API. Status code:", r.status_code)
            error="Failed to fetch data from the API. Status code:"
    
        sankey_data={}
        if data['_items']!=[]:
            sankey_data=make_sankey_data(data)
            
        else:
            error="No data for the given time"
        stored_time=current_time.strftime('%Y-%m-%d %H:%M:%S')
        display_time=current_time_display.strftime('%Y-%m-%d %H:%M:%S')

        return [sankey_data, f"{display_time}",error,stored_time,display_time,"false"]

    
@app.callback(
    Output("data-store", "data"),
    Input("interval-component", "n_intervals"),
    State("data-store", "data"),  # Access current store state
)
def manage_data_updates(n_intervals, current_data):
    """
    Fetch initial data on the first interval (n_intervals == 0).
    For subsequent intervals, fetch updated data.
    """
   
        # Merge updated data with existing data
    updated_data = fetch_updated_data()
        
    return updated_data  # Append new data to the existing data

# Callback to update the table with data from dcc.Store
@app.callback(
    Output("data-table", "data"),
    Input("data-store", "data"),
)
def update_table(store_data):
    """Update the table with data from the Store."""
    print(store_data)
    if store_data is None:
        return []
    return store_data

@app.callback(
    Output("sankey-store", "data",allow_duplicate=True),
    Output("branch-store", "data",allow_duplicate=True),
    Output("groups-store", "data",allow_duplicate=True),
    [Input("action-dropdown", "value"), Input("sankey-graph", "clickData")],
    State("sankey-store", "data"),
    State("branch-store", "data"),
    State("groups-store", "data"),
    State("el", "event"),
    prevent_initial_call='initial_duplicate'
)

def update_diagram(operation,clickData,sankey_data,branch_store,groups,e):
        branches=branch_store
        print("hey")
     
        if(clickData!=None):
            branch=clickData['points'][0]['index'] 
        
            if e !=None:
                shift=e['shiftKey']
                #print("shift : ",shift)
                if(shift==True):
                    # lc1[branch]='rgba(31,119,180,0.8)'
                    if(branch not in branches):
                        branches.append(branch)
                        for a in branches:
                            if(sankey_data["link_colors"][a]==red):
                                sankey_data["link_colors"][a]=dark_red
                            else:
                                sankey_data["link_colors"][a]=dark_purple
                print(branch)
                if(shift==False):
                    branches=[branch]
                    if(branch!=None):
                        if(sankey_data["link_colors"][branch]==red):
                        
                            sankey_data["link_colors"][branch]=dark_red
                        elif(sankey_data["link_colors"][branch]==dark_red):
                        
                            sankey_data["link_colors"][branch]=red
                        elif(sankey_data["link_colors"][branch]==dark_purple):
                        
                            sankey_data["link_colors"][branch]=purple
                        else : 
                            sankey_data["link_colors"][branch]=dark_purple
            
        if(operation=='highlight'):
    #inc opacity and change color of link for highlighting
            for a in branches:
                sankey_data["link_colors"][a]=red
              
            if(branches!=[]):
                branches.clear()
        
            
        
    
        if(operation=='hide'):
        # make opacity 0 for hiding
                for a in branches:
                    sankey_data["link_colors"][a]='rgba(31,119,180,0.0)'
                    
                    #node_colors[a+1]='rgba(31,119,180,0.0)'
                if(branches!=[]):
                    branches.clear()
                    
                    
                    
                if(branches!=[]):
                    branches.clear()
            
        
        if(operation=='unhighlight'): 
                for a in branches:
                    sankey_data["link_colors"][a]=purple 
                    
                if(branches!=[]):
                    branches.clear()
        
        
        if(operation=='unhide'):
        #    lc1[branch]='#6E0CED'
            length = len(sankey_data["link_colors"])
            for i in range(length):
                if(sankey_data["link_colors"][i]=='rgba(31,119,180,0.0)'):
                    sankey_data["link_colors"][i]=color_code1
                    
            if(branches!=[]):
                    branches.clear()

        if(operation=="group"):
            new_name=""
          
            targets=[]
            branches.sort()
            

            #stores the name and index of nodes to be grouped
            for a in branches:
                new_name+=sankey_data["lab"][sankey_data["tar"][a]]+' '
                targets.append(sankey_data["tar"][a])

            sankey_data["lab"].append(new_name)
            node_colors.append(color_code2)
            groups.append({new_name:targets}) #adds group to dict to un-group later

            new_ind=len(sankey_data["lab"])-1
            lent=len(src)
            #replaces all the selected nodes with group
            for i in range(lent):
                if src[i] in targets:
                    src[i]=new_ind
                if sankey_data["tar"][i] in targets:
                    sankey_data["tar"]=new_ind 
            
            if(branches!=[]):
                    branches.clear()
            
        if (operation=="Un-grouping"):
            
            grp_name=sankey_data["lab"][sankey_data["tar"][branches[0]]]#gets group name
            print(grp_name)
            targets=groups[grp_name]#extracts the original nodes of the group
            print(targets)
            length=len(src)
            k=0

            #replaces the group with original nodes
            for i in range(length):
                if sankey_data["lab"][sankey_data["src"][i]] ==grp_name:
                    if(k<len(targets)):
                        src[i]=targets[k]
                        #print(src[i],targets[k])
                        k+=1
                if sankey_data["lab"][sankey_data["tar"][i]] ==grp_name:
                    if(k<len(targets)):
                        sankey_data["tar"][i]=targets[k]
                        #print(tar[i],targets[k])
                        k+=1
            if(branches!=[]):
                    branches.clear()
            
                    
        
    
   
        print(branches,operation)
        return sankey_data,branches,groups
        

# Callback to update the Sankey diagram based on stored data
@app.callback(
    Output("sankey-graph", "figure"),
    Input("sankey-store", "data"),
)



def update_sankey(data):
    if data["lab"]==[]:
        return []
    updated_fig =go.Figure(
        go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=data["lab"],
                color=data["node_colors"]
            ),
            link=dict(
                source=data["src"],
                target=data["tar"],
                value=data["val"],
                color=data["link_colors"]
            )
        ))
    return updated_fig

if __name__ == "__main__":
    app.run_server(debug=True,port=8052)
