import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
import requests
from io import BytesIO

# Dataset Processing

# path = 'https://github.com/CarolinaDN/DataVisualization/tree/main/Project2/Datasets/'

parties = pd.read_csv('parties_final.csv')
leadership = pd.read_csv('leadership.csv')
indicators = pd.read_csv('indexes.csv')
political_compass = pd.read_csv('political_compass.csv')

# Instanciate the app
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

# Build the layout


app.layout = html.Div(
    children=[
        # (First row) Header: - Title -  github meter codigo
        html.Div(
            children=[
                html.Div(
                    children=[
                    # Logo
                    html.Div(
                        children = [
                            html.Img(
                                src = app.get_asset_url("IMS-rgb_logo.png"),
                                id = "corona-image",
                                style = {
                                    "height": "80px",
                                    "width": "auto",
                                    "margin-left": "0px"
                                }
                            )
                        ],
                        className="one-third column",style={'textAlign': 'left'}
                        ),
                        # Title and subtitle
                        html.Div(
                            children=[
                                html.H3(
                                    children="A Glimpse into the Politics of a Country ",
                                    style={
                                        "margin-bottom": "0",
                                        "color": "white","textAlign": "center right"
                                    }
                                ),
                                html.H5(
                                    children= "Interactive Data Visualization Approach",
                                    style={
                                        "margin-bottom": "0",
                                        "color": "orange", "textAlign": "right"
                                    }
                                )
                            ]
                        ),

                    ],
                    className="two-thirds column",style={'textAlign': 'center'},
                    id='title'
                ),
                        # Github
                        html.Div(
                            children=[
                                html.H6(children="Dash Politics", style={"color": "white"}),
                                html.A(
                                    id="github-link",
                                    children=["View source code on Github"],
                                    href="https://github.com/CarolinaDN/DataVisualization/tree/main/Project2",
                                    style={"color": "orange"}
                                ),
                            ],
                            className="one-third column", id="title1"
                        ),
            ],
            id="header",
            className="row flex-display",
            style={
                "margin-bottom": "25px"
            }
        ),

        # (Second row): Dropdown - 3 image boxes: flag, head of state and head of government
        html.Div(
            children=[
                # (Column 1) Value boxes
                html.Div(
                    children=[
                        # Country selector
                        html.P(
                            children="Select Country: ",
                            className="fix_label",
                            style={
                                "color": "white"
                            }
                        ),
                        dcc.Dropdown(
                            id="country_name",
                            multi=False,
                            searchable=True,
                            value="Portugal",
                            placeholder="Select Country",
                            options=[{"label": c, "value": c} for c in (parties.country_name.unique())],
                            className="dcc_compon"
                        ),
                    ],
                    className="create_container three columns"
                ),
                # (Column 2): Flag
                html.Div(
                    children=[
                        # Title
                        html.H6(
                            children="Flag",
                            style={
                                "textAlign": "center",
                                "color": "white"
                            }
                        ),
                        # Total value
                        html.Img(id="flag_image",
                                 style={"vertical-align": "middle",
                                        "height": "100px",
                                        "width": "auto",
                                        "margin-bottom": "5px"},
                                 className='align-self-center'),

                    ], style={'textAlign': 'center'},
                    className="card_container three columns"
                ),
                # (Column 3): Head of State
                html.Div(
                    children=[
                        # Title
                        html.H6(
                            children="Head of State",
                            style={
                                "textAlign": "center",
                                "color": "white"
                            }
                        ),
                        # Total value
                        html.Img(id="state",
                                 style={"horizontal-align": "middle",
                                        "height": "100px",
                                        "width": "auto",
                                        "margin-bottom": "5px"}),
                        # Subtitle
                        html.P(
                            id="t_state",
                            style={
                                "textAlign": "center",
                                "color": "white",
                                "fontSize": 10
                            }
                        )

                    ], style={'textAlign': 'center'},
                    className="card_container three columns"
                ),
                # (Column 4): Head of Government
                html.Div(
                    children=[
                        # Title
                        html.H6(
                            children="Head of Government",
                            style={
                                "textAlign": "center",
                                "color": "white"
                            }
                        ),
                        # Total value
                        html.Img(id="government",
                                 style={"horizontal-align": "middle",
                                        "height": "100px",
                                        "width": "auto",
                                        "margin-bottom": "5px"}),
                        # Subtitle
                        html.P(
                            id="t_gov",
                            style={
                                "textAlign": "center",
                                "color": "white",
                                "fontSize": 10
                            })

                    ], style={'textAlign': 'center'},
                    className="card_container three columns"
                ),

            ],
            className="row flex-display"
        ),

        # (Third row): World Scatter - Parties Scatter
        html.Div(
            children=[
                # (Column 1) World Scatter (Pie antes)
                html.Div(
                    children=[
                        # World Scatter
                        dcc.Graph(
                            id="world_scatter",
                            config={
                                "displayModeBar": "hover"
                            }
                        )
                    ],
                    className="create_container six columns"  # ,
                     #style={
                      # "maxWidth": "400px"
                     #}
                ),

                # (Column 2) Parties Scatter (Line and bars plot antes)
                html.Div(
                    children=[
                        dcc.Graph(#style={"maxWidth": "400px"},
                            id="parties_scatter",
                            config={
                                "displayModeBar": "hover",

                            }
                        )
                    ],
                    className="create_container six columns"
                )
            ],
            className="row flex-display"
        ),
        # (Forth row): Indicators
        html.Div(
            children=[
                # (Column 1): PIB
                html.Div(
                    children=[
                        # Title
                        html.H6(
                            children="GDP per capita",
                            style={
                                "textAlign": "center",
                                "color": "white"
                            }
                        ),
                        # Total value
                        html.P(
                            id="pib",
                            style={
                                "textAlign": "center",
                                "color": "orange",
                                "fontSize": 40
                            }
                        ),
                    ],
                    className="card_container three columns"
                ),
                # (Column 2): Pop
                html.Div(
                    children=[
                        # Title
                        html.H6(
                            children="Population",
                            style={
                                "textAlign": "center",
                                "color": "white"
                            }
                        ),
                        # Total value
                        html.P(
                            id="pop",
                            style={
                                "textAlign": "center",
                                "color": "orange",
                                "fontSize": 40
                            }
                        ),
                    ],
                    className="card_container three columns"
                ),
                # (Column 3): Gender Equality
                html.Div(
                    children=[
                        # Title
                        html.H6(
                            children="Gender Equality (0-100)",
                            style={
                                "textAlign": "center",
                                "color": "white"
                            }
                        ),
                        # Total value
                        html.P(
                            id="gender",
                            style={
                                "textAlign": "center",
                                "color": "orange",
                                "fontSize": 40
                            }
                        ),
                    ],
                    className="card_container three columns"
                ),
                # (Column 4): Religious Index
                html.Div(
                    children=[
                        # Title
                        html.H6(
                            children="Religious Index (0-100)",
                            style={
                                "textAlign": "center",
                                "color": "white"
                            }
                        ),
                        # Total value
                        html.P(
                            id="religion",
                            style={
                                "textAlign": "center",
                                "color": "orange",
                                "fontSize": 40
                            }
                        ),
                    ],
                    className="card_container three columns"
                ),


            ],
            className="row flex-display"
        ),

        # (Fith row): Indicators
        html.Div(
            children=[
                # (Column 1): Unemployment
                html.Div(
                    children=[
                        # Title
                        html.H6(
                            children="Unemployment Rate",
                            style={
                                "textAlign": "center",
                                "color": "white"
                            }
                        ),
                        # Total value
                        html.P(
                            id="unemployment",
                            style={
                                "textAlign": "center",
                                "color": "orange",
                                "fontSize": 40
                            }
                        ),
                    ],
                    className="card_container three columns"
                ),
                # (Column 2): Gini Index (0-100)
                html.Div(
                    children=[
                        # Title
                        html.H6(
                            children="Gini Index (0-100)",
                            style={
                                "textAlign": "center",
                                "color": "white"
                            }
                        ),
                        # Total value
                        html.P(
                            id="gini",
                            style={
                                "textAlign": "center",
                                "color": "orange",
                                "fontSize": 40
                            }
                        ),
                    ],
                    className="card_container three columns"
                ),
                # (Column 3): Happiness Score
                html.Div(
                    children=[
                        # Title
                        html.H6(
                            children="Happiness Score (0-10)",
                            style={
                                "textAlign": "center",
                                "color": "white"
                            }
                        ),
                        # Total value
                        html.P(
                            id="happiness",
                            style={
                                "textAlign": "center",
                                "color": "orange",
                                "fontSize": 40
                            }
                        ),
                    ],
                    className="card_container three columns"
                ),
                # (Column 4): Financial Literacy
                html.Div(
                    children=[
                        # Title
                        html.H6(
                            children="Financial Literacy in Adults",
                            style={
                                "textAlign": "center",
                                "color": "white"
                            }
                        ),
                        # Total value
                        html.P(
                            id="fin_lit",
                            style={
                                "textAlign": "center",
                                "color": "orange",
                                "fontSize": 40
                            }
                        ),
                    ],
                    className="card_container three columns"
                ),


            ],
            className="row flex-display")
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)


# Build the callbacks
# flag_image
@app.callback(
    Output(
        component_id="flag_image",
        component_property="src"
    ),
    Input(
        component_id="country_name",
        component_property="value"
    )
)
def update_flag_image(country_name):
    return leadership.loc[leadership['State'] == country_name]['flag'].item()

# head state
@app.callback(
    Output(
        component_id="state",
        component_property="src"
    ),
    Input(
        component_id="country_name",
        component_property="value"
    )
)
def update_flag_image(country_name):
    return leadership.loc[leadership['State'] == country_name]['head_state_picture'].item()

# subtitle
@app.callback(
    Output(
        component_id="t_state",
        component_property="children"
    ),
    Input(
        component_id="country_name",
        component_property="value"
    )
)
def update_flag_image(country_name):
    return leadership.loc[leadership['State'] == country_name]['Head of state'].item()


# head government
@app.callback(
    Output(
        component_id="government",
        component_property="src"
    ),
    Input(
        component_id="country_name",
        component_property="value"
    )
)
def update_flag_image(country_name):
    return leadership.loc[leadership['State'] == country_name]['head_gov_picture'].item()

# subtitle
@app.callback(
    Output(
        component_id="t_gov",
        component_property="children"
    ),
    Input(
        component_id="country_name",
        component_property="value"
    )
)
def update_flag_image(country_name):
    return leadership.loc[leadership['State'] == country_name]['Head of government'].item()



# World Scatter
@app.callback(
    Output(
        component_id="world_scatter",
        component_property="figure"
    ),
    Input(
        component_id="country_name",
        component_property="value"
    )
)
def update_world_scatter(country_name):
    political_compass['size'] = 10

    # Filter the data
    x = political_compass['Economic Freedom']
    y = political_compass['Democracy Index']
    text = political_compass['Country Name']
    size = political_compass['size']

    # mask to filter by country

    mask = (political_compass['Country Name'].isin([country_name]))

    # scatter itself
    fig = px.scatter(political_compass, x, y, size_max=60, color="Continent", hover_name="Country Name")

    fig.update_traces(textposition='top center')

    fig.update_layout(title_text="World's Political Compass")
    # Mask
    fig.add_trace(px.scatter(political_compass, political_compass['Economic Freedom'][mask],
                             political_compass['Democracy Index'][mask], size=size[mask],
                             color_discrete_sequence=['black']).data[0])
    fig['layout']['yaxis']['autorange'] = "reversed"
    fig.add_shape(type='line', x0=0, x1=110, y0=6, y1=6, line=dict(color="white",width=1))
    fig.add_shape(type='line', y0=0, y1=10, x0=69.9, x1=69.9, line=dict(color="white",width=1))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(showline=True, linewidth=2, linecolor='white', showgrid=False)
    fig.update_yaxes(showline=False, linewidth=2, linecolor='white', showgrid=False)
    fig.update_layout(
      font_family="Times New Roman",
      font_color="white",
      font_size=12,
      title_font_family="Times New Roman",
      title_font_color="white",
      title_font_size=20,
      legend_title_font_color="white",
      legend_font_color='white',
      legend_font_size=12,
    )

# Return the figure
    return fig


# Parties scatter
@app.callback(
    Output(
        component_id="parties_scatter",
        component_property="figure"
    ),
    Input(
        component_id="country_name",
        component_property="value"
    )
)
def update_parties_scatter(country_name):

    x = parties[parties.country_name == country_name]['left_right']
    y = parties[parties.country_name == country_name]['liberty_authority']
    text = parties[parties.country_name == country_name]['party_name_short']
    size = parties[parties.country_name == country_name]['seats']

    # scatter itself
    fig = px.scatter(parties[parties.country_name == country_name], x, y, size_max=60, #color='family_name',
                     hover_name="party_name_short")

    fig.update_traces(marker_color="rgba(0,0,0,0)")
    fig.update_traces(textposition='top center')
    fig.add_shape(type='line', x0=0, x1=10, y0=5, y1=5, line=dict(color="white",width=1))
    fig.add_shape(type='line', y0=0, y1=10, x0=5, x1=5, line=dict(color="white",width=1))

    fig.update_layout(title_text="Country's Political Compass", title_font_color="white")

    fig.add_trace(go.Scatter(
        x=[5,5,10.5,-0.5],
        y=[10.5,-0.25,5.25,5.25],
        mode="text",
        name="Text",
        text=["Authoritarian", "Libertarian", "Right", "Left"],
        textposition="bottom center", textfont_size=10, textfont_color='white'))

    for i, row in parties[parties.country_name == country_name].iterrows():
        response = requests.get(row['flag'])
        fig.add_layout_image(
            dict(
                source=Image.open(BytesIO(response.content)),
                xref="x",
                yref="y",
                xanchor="center",
                yanchor="middle",
                x=row["left_right"],
                y=row["liberty_authority"],
                sizex=1,
                sizey=1,
                sizing="contain",
                opacity=0.8,
                layer="above"
            )
        )

    fig.update_xaxes(showline=False, showgrid=False, linewidth=2, linecolor='white', mirror=True)
    fig.update_yaxes(showline=False, showgrid=False, linewidth=2, linecolor='white', mirror=True)
    fig.update_xaxes(zeroline=False)
    fig.update_yaxes(zeroline=False)
    fig.update_layout(
        xaxis_title="Economic",
        yaxis_title="Social")
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
    fig.update_layout(
        font_color="white",
        title_font_color="white",
        legend_title_font_color="rgba(0, 0, 0, 0)",
        showlegend= False)

    return fig

# 4th row
# PIB
@app.callback(
    Output(
        component_id="pib",
        component_property="children"
    ),
    Input(
        component_id="country_name",
        component_property="value"
    )
)
def update_flag_image(country_name):
    return indicators[indicators['Country Name'] == country_name]["GDP per capita"].item(), '$'

# Pop
@app.callback(
    Output(
        component_id="pop",
        component_property="children"
    ),
    Input(
        component_id="country_name",
        component_property="value"
    )
)
def update_flag_image(country_name):
    return indicators[indicators['Country Name'] == country_name]["Population"].item()

# Gender Equality
@app.callback(
    Output(
        component_id="gender",
        component_property="children"
    ),
    Input(
        component_id="country_name",
        component_property="value"
    )
)
def update_flag_image(country_name):
    return round(indicators[indicators['Country Name'] == country_name]["Gender Equility (0-100)"].item(),2)

# Religion
@app.callback(
    Output(
        component_id="religion",
        component_property="children"
    ),
    Input(
        component_id="country_name",
        component_property="value"
    )
)
def update_flag_image(country_name):
    return indicators[indicators['Country Name'] == country_name]["Religious Index (0-100)"].item(), '%'

# 5th row
# Unemployment
@app.callback(
    Output(
        component_id="unemployment",
        component_property="children"
    ),
    Input(
        component_id="country_name",
        component_property="value"
    )
)
def update_flag_image(country_name):
    return round(indicators[indicators['Country Name'] == country_name]["Unemployment Rate (%)"].item()*100,2), '%'

# Gini
@app.callback(
    Output(
        component_id="gini",
        component_property="children"
    ),
    Input(
        component_id="country_name",
        component_property="value"
    )
)
def update_flag_image(country_name):
    return indicators[indicators['Country Name'] == country_name]["Gini Index (0-100)"].item()

# Happiness
@app.callback(
    Output(
        component_id="happiness",
        component_property="children"
    ),
    Input(
        component_id="country_name",
        component_property="value"
    )
)
def update_flag_image(country_name):
    return round(indicators[indicators['Country Name'] == country_name]["Happiness Score (0-10)"].item(),2)

# Literacy
@app.callback(
    Output(
        component_id="fin_lit",
        component_property="children"
    ),
    Input(
        component_id="country_name",
        component_property="value"
    )
)
def update_flag_image(country_name):
    return indicators[indicators['Country Name'] == country_name]["Financial Literacy in Adults (%)"].item(), '%'


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
