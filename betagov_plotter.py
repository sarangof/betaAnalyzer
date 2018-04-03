#import bokeh
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.plotly as ply

"""
sns.set_style("whitegrid")
sns.palplot(sns.color_palette("husl"))
csfont = {'fontname':'Georgia'}
hfont = {'fontname':'Cambria'}

plt.rcParams["font.family"] = "serif"

"""

def change_width(ax, new_value) :
    for patch in ax.patches :
        current_width = patch.get_width()
        diff = current_width - new_value

        # we change the bar width
        patch.set_width(new_value)

        # we recenter the bar
        patch.set_x(patch.get_x() + diff * .5)
        
def betagov_plot(title, x_var, y_var, x_label,y_label, file_name, width_param, hue=None, order=None):

    fig, ax = plt.subplots(figsize=(4,4))
    sns.barplot(x_var,
                y_var,
                palette="Blues_d",
                ax=ax,
                estimator=np.mean,
                errwidth=2,
                saturation=1,
                hue=hue,
                order=order);

    bplot = sns.barplot(hue=data['version'],
                    y=data['Average score'],
                    x=data['grade'],
                    palette="Blues_d",
                    ax=ax,
                    estimator=np.mean,
                    order=['Third','Fourth','Fifth'],
                    errwidth=2,
                    saturation=1);

    plt.ylabel(y_label,size=18, **csfont);
    plt.title('', **csfont)
    plt.xlabel(x_label,size=18, **csfont);
    plt.xticks(fontsize=13, **csfont)
    plt.ylim([0,100.]);
    plt.tight_layout();

    ttl = ax.title
    ttl.set_position([.5, 1.03])

    change_width(ax, width_param)

    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x()+p.get_width()/2.,
                4,
                '{:1.1f}'.format(height),
                ha="center",
               color='white',
               size=12,
                fontweight='bold') 

    plt.savefig(file_name+'.png');

    return fig


app = dash.Dash()
#app.css.append_css({'external_url': 'http://betagov.org/css/style.css'})
#app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})

df = pd.read_csv('https://raw.githubusercontent.com/sarangof/betaAnalyzer/master/betaAnalyser_sample.csv')
title = 'Average score'
x_label = 'Group'
y_label = 'Average score'
# CLEARLY NEED TO MODIFY THIS.  -- Clearly don't remember why.
x_var = df['Group']
y_var = df['Outcome B']
file_name = 'Test_scores'
width_param = .45


available_indicators = df.columns.values

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Group'
            ),

        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Outcome B'
            ),
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='beta-graphic'),
])

@app.callback(
    dash.dependencies.Output('beta-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name):
    return {
        'data': #[py.iplot_mpl(betagov_plot(title, x_var, y_var, x_label, y_label, file_name, width_param, hue, order))]
            [go.Bar(
            x=df[xaxis_column_name].values,
            y=df[yaxis_column_name].values
                )]
    }


if __name__ == '__main__':
    app.run_server()
