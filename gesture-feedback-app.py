
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!  IMPORT   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#%%
from dash import Dash, html, dcc, Input, Output, State, callback_context
import plotly.graph_objects as go
import plotly.express as px
import util
import plot
from multiprocessing import Process, Value, Array
import ctypes
from skimage import io


#%%
app = Dash(__name__)
capture_state = Value(ctypes.c_bool,False) # Shared variable that is used as a flag from the GUI
gesture_count_array = Array("i",[0,0,0,0]) # Shared variable that is used as a flag from the GUI
settings_dict = util.read_settings()
print(settings_dict)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!   LAYOUT   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



app.layout = html.Div(id="main-div", children=[
    html.Div(id = "title-div",children = [
        html.Button("capture","capture-button"),
        html.Button("reset","reset-button"),
        html.H2(id='confirm-capture'),
        dcc.Graph(id="gesture-image"),
        html.H1(id = "title-id",children='GIVE ME FEEDBACK!'),
        html.H2(id='confirm-reset',hidden=True)
    ]),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        ),
    dcc.Graph(id="reactions-figure")
    ])


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!              !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!   CALLBACS   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!              !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!   display image   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@app.callback(
    Output("gesture-image","figure"),
    Input('interval-component', 'n_intervals')
)

def update_image(updated):
    """
    TO DO : Display an image of the last shown gesture / Or maybe hightlight the latest shown image
    *  Have 3 images each with one of the gestures highlighted
    """
    image_path = settings_dict["gestures_img"] # replace with your own image
    img = io.imread(image_path)
    fig = px.imshow(img)

    fig.update_layout( # customize font and legend orientation & position
        legend = dict(
            title=None,
            orientation = "h"
        ),
        yaxis={'visible': False, 'showticklabels': False},
        xaxis={'visible': False, 'showticklabels': False},
        # width = 1920/divide,height = 1080/divide,
        plot_bgcolor = "white"

    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    
    return fig

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!   capture   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@app.callback(
    Output("confirm-capture","children"),
    Input("capture-button","n_clicks"),
    prevent_initial_callbacks = True
)

def capture_video(capture):
    
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    capture_state_str = "Capture State: False"
    
    global capture_state
    
    if "capture-button" in changed_id:
        
        # change capture state
        with capture_state.get_lock():
            capture_state.value = not capture_state.value
        capture_state_str = f"Capture State: {capture_state.value}"
        # print(capture_state.value)
    return capture_state_str

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!   reset counter   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@app.callback(
    Output("confirm-reset","children"),
    Input("reset-button","n_clicks"),
    prevent_initial_callbacks = True
)

def capture_video(reset):
    
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    capture_state_str = "Reset State: False"
    
    global gesture_count_array
    
    if "reset-button" in changed_id:
        for elem in range(4):
            gesture_count_array[elem] = 0
    return capture_state_str


    
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!   display figure   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@app.callback(
    Output("reactions-figure","figure"),
    Input('interval-component', 'n_intervals')
)

def update_figure(updated):
    global gesture_count_array
    

    gesture_counts_list = [gesture_count_array[elem] for elem in range(3)]
    print(gesture_counts_list)

    columns=["Peace","Rock On","Thumb Up"]#, "Other"]

    data = [go.Bar(
    x = columns,
    y = gesture_counts_list
    )]


    layout = go.Layout(dict(
                        plot_bgcolor = "white",
                        paper_bgcolor = "white",
                        font_size = 30,
                        font_color = "#449afd"
                        ))


    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    
    return fig


if __name__ == '__main__':
    p2 = Process(target=plot.capture_from_web_cam, args=(capture_state,gesture_count_array,))
    p2.start()
    # app.run_server(debug=True)
    app.run_server(debug=False)