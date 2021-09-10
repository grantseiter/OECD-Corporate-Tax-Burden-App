import os
import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import base64

image_filename = "assets/aei_logo.png"
encoded_image = base64.b64encode(open(image_filename, "rb").read())

pio.templates.default = "plotly_white"

APP_PATH = os.path.abspath(os.path.dirname(__file__))

# Data

revenue = pd.read_csv("data/treasury-estimates.csv")
output = pd.read_csv("data/output.csv")

# Code


def get_text_data():
    return


def get_style_data_conditional(rowval):
    style_data_conditional = [
        {
            "if": {"row_index": rowval},
            "backgroundColor": "rgb(240, 240, 240)",
        },
    ]
    return style_data_conditional


def make_bar_figure(rate, ratetitle, ratelabel):
    """
    Function creates bar charts with rate inputs for top section
    """
    data = output.sort_values(by=[rate], ascending=True).reset_index(drop=True)
    oecd_avg = data[rate].mean()
    btm = data.name[0]
    mid = data.name[12]
    top = data.name[36]
    usloc = int(data[data["name"] == "United States"].index[0])

    colors = ["#008CCC"] * 100
    colors[usloc] = "#014E7F"

    bar_figure = go.Figure(
        data=go.Bar(
            x=data["name"],
            y=data[rate],
            marker_color=colors,
            name=ratelabel,
        )
    )

    bar_figure.add_trace(
        go.Scatter(
            x=[btm, mid, top],
            y=[oecd_avg, oecd_avg, oecd_avg],
            mode="lines+text",
            name=ratelabel,
            text=["", "OECD Average", ""],
            textposition="top center",
            textfont=dict(color="#FF5C68"),
            line=dict(
                color="#FF5C68",
                dash="dash",
            ),
            hovertemplate="(OECD Average, %{y})",
            hoverlabel=dict(bgcolor="#FF5C68"),
        )
    )

    layout = go.Layout(
        showlegend=False,
        title=ratetitle + " in the OECD, 2022 ",
        yaxis=dict(
            gridcolor="#F2F2F2",
            tickformat=".0%",
        ),
        plot_bgcolor="white",
    )

    bar_figure.update_layout(layout)

    return bar_figure


# Initialize App

app = dash.Dash(__name__)

# Create App Layout
app.layout = html.Div(
    [
        # HEADER
        html.Div(
            [
                html.H6(
                    "BETA VERSION 0.1.1 –– PEASE DO NOT CITE WITHOUT PERMISSON DATA IS NOT FINAL –– RELEASE v1-2021-09-10",
                    style={
                        "margin-top": "0",
                        "font-weight": "bold",
                        "color": "red",
                        "text-align": "center",
                    },
                ),
            ],
            className="description_container twelve columns",
        ),
        html.Div(
            [
                html.Img(
                    src="data:image/png;base64,{}".format(encoded_image.decode()),
                    height=80,
                )
            ]
        ),
        dcc.Markdown(
            """
            ## Tax Burden on Multinational Corporations in the OECD
            """
            """
            *Modeling by <a href="https://www.aei.org/profile/kyle-pomerleau/" children="Kyle Pomerleau" style="color:#4f5866;text-decoration:none" target="blank" />. Dashboard design by <a href="https://github.com/grantseiter/" children="Grant M. Seiter" style="color:#4f5866;text-decoration:none" target="blank" />.*
            """,
            style={"max-width": "1000px"},
            dangerously_allow_html=True,
        ),
        html.Div(
            [
                html.P(
                    "The Biden administration and congressional Democrats have proposed significant changes to the tax treatment of US multinational corporations aimed at raising revenue and curbing profit shifting and base erosion. This dashboard summarizes major components of the administration's corporate tax proposals and allows users to visualize different measures of corporate tax burden in OECD nations under current law.",
                    style={"text-align": "justify"},
                ),
            ],
            className="twelve columns",
        ),
        # BIDEN PROPOSALS SECTION
        html.Div(
            [
                html.H6(
                    "Summary of the Biden Administration's Corporate Tax Proposals",
                    style={"text-align": "justify", "font-weight": "bold"},
                ),
                html.Label(
                    "Select a proposal, below, to view more details.",
                    style={"font-style": "italic", "font-size": "90%"},
                ),
                dcc.Dropdown(
                    id="variable_selection",
                    options=[
                        {"label": "All Proposals", "value": "ALL"},
                        {
                            "label": "Raise the Corporate Income Tax from 21 to 28 Percent",
                            "value": "CTR",
                        },
                        {
                            "label": "Reform GILTI, Limit Inversions, and Disallow Deductions Attributable to Exempt Income",
                            "value": "GILTI",
                        },
                        {
                            "label": "Repeal FDII and Replace with R&D Incentive",
                            "value": "FDII",
                        },
                        {"label": "Replace BEAT with SHIELD", "value": "SHIELD"},
                        {"label": "Impose a 15 Percent Book Tax", "value": "BOOK"},
                    ],
                    value="ALL",
                    clearable=False,
                    searchable=False,
                    className=" input_container twelve columns",
                ),
                html.Div(
                    [
                        dash_table.DataTable(
                            id="revenue_table",
                            columns=[{"name": i, "id": i} for i in revenue.columns],
                            data=revenue.to_dict("records"),
                            style_cell={"textAlign": "center"},
                            style_header={
                                "backgroundColor": "white",
                                "fontWeight": "bold",
                            },
                            style_cell_conditional=[
                                {
                                    "if": {
                                        "column_id": "Revenue Impact (Billions of Dollars)"
                                    },
                                    "textAlign": "left",
                                },
                            ],
                        ),
                    ],
                    className="description_container seven columns",
                ),
                # html.Div([dcc.Graph(id="table")],className="seven columns"),
                dcc.Markdown(
                    id="prop_text",
                    className="four columns",
                    style={"text-align": "justify", "margin-bottom": "10px"},
                    dangerously_allow_html=True,
                ),
                html.P(
                    "Source: Revenue Estimates are from US Department of Treasury; Policy Descriptions are from Author.",
                    className="control_label twelve columns",
                    style={
                        "text-align": "right",
                        "font-style": "italic",
                        "font-size": "80%",
                    },
                ),
            ],
            className="description_container twelve columns",
        ),
        html.Hr(),
        # COMPARING TAX RATES SECTION
        html.Div(
            [
                html.H6(
                    "Comparing Effective Corporate Tax Rates in OECD Nations",
                    style={
                        "margin-top": "0",
                        "font-weight": "bold",
                        "text-align": "justify",
                    },
                ),
                dcc.Markdown(
                    """
                Three measures of a jurisdiction's corporate tax burden are its statutory corporate tax rate, marginal effective corporate tax rate (METR), and average effective corporate tax rate (AETR). Differences in effective rates affect profit-shifting incentives, the incentive to invest, and the incentive for firms to locate headquarters in the United States.  
                """,
                    className="twelve columns",
                    style={"text-align": "justify"},
                    dangerously_allow_html=True,
                ),
                html.Label(
                    "Toggle the tabs, below, to view estimates of each measure.",
                    className="twelve columns",
                    style={
                        "font-style": "italic",
                        "font-size": "90%",
                        "margin-bottom": "10px",
                    },
                ),
                dcc.Markdown(
                    """            
                 **Statutory Corporate Tax Rates** measure the tax burden on profits, or in the case of multinational corporations, the incentive to locate profits in different jurisdictions.

                 **Marginal Effective Corporate Tax Rates (METRs)** measure the tax burden on marginal investment, or an investment that breaks even in present value. This rate can affect the decision to increase or decrease the level of an investment.
                 
                 **Average Effective Corporate Tax Rates (AETRs)** measure the tax burden on discrete investment, or an investment that is expected to earn an above-normal return. This rate can affect the choice between two or more mutually exclusive investments, or in the case of multinational corporations, the decision to locate investment in different jurisdictions.  
                """,
                    className="results_container three columns",
                    style={"text-align": "justify", "margin-bottom": "10px"},
                    dangerously_allow_html=True,
                ),
                html.Div(
                    [
                        dcc.Tabs(
                            id="bar_figure_tabs",
                            value="stat_tab",
                            children=[
                                dcc.Tab(
                                    label="Statutory Rate",
                                    value="stat_tab",
                                    className="custom_tab",
                                    selected_className="custom_tab_selected",
                                ),
                                dcc.Tab(
                                    label="Marginal Rate (METR)",
                                    value="metr_tab",
                                    className="custom-tab",
                                    selected_className="custom_tab_selected",
                                ),
                                dcc.Tab(
                                    label="Average Rate (AETR)",
                                    value="aetr_tab",
                                    className="custom-tab",
                                    selected_className="custom_tab_selected",
                                ),
                            ],
                        )
                    ],
                    className="custom_tabs_container eight columns",
                ),
                html.Div(
                    [
                        dcc.Graph(id="bar_figure"),
                    ],
                    className="eight columns",
                ),
                html.P(
                    "Source: Author's calculations.",
                    className="control_label twelve columns",
                    style={
                        "text-align": "right",
                        "font-style": "italic",
                        "font-size": "80%",
                    },
                ),
                # ASSET/FINANCING BIAS SUBSECTION
                html.Div(
                    [
                        dcc.Markdown(
                            """
                    ** Differences in Effective Rates by Form of Financing **

                    These rates vary by asset and by form of financing in many jurisdictions, creating a tax-favored bias for some investments and their financing mechanisms.
                    """,
                            className="twelve columns",
                            style={"text-align": "justify"},
                            dangerously_allow_html=True,
                        ),
                        html.Label(
                            "Select or search for one or more countries in the dropdown, below.",
                            style={"font-style": "italic", "font-size": "90%"},
                        ),
                        dcc.Dropdown(
                            id="fin-drop",
                            options=[
                                {"label": "Australia", "value": "AUS"},
                                {"label": "Austria", "value": "AUT"},
                                {"label": "Belgium", "value": "BEL"},
                                {"label": "Canada", "value": "CAN"},
                                {"label": "Chile", "value": "CHL"},
                                {"label": "Colombia", "value": "COL"},
                                {"label": "Czech Republic", "value": "CZE"},
                                {"label": "Denmark", "value": "DNK"},
                                {"label": "Estonia", "value": "EST"},
                                {"label": "Finland", "value": "FIN"},
                                {"label": "France", "value": "FRA"},
                                {"label": "Germany", "value": "DEU"},
                                {"label": "Greece", "value": "GRC"},
                                {"label": "Hungary", "value": "HUN"},
                                {"label": "Iceland", "value": "ISL"},
                                {"label": "Ireland", "value": "IRL"},
                                {"label": "Israel", "value": "ISR"},
                                {"label": "Italy", "value": "ITA"},
                                {"label": "Japan", "value": "JPN"},
                                {"label": "Korea", "value": "KOR"},
                                {"label": "Latvia", "value": "LVA"},
                                {"label": "Lithuania", "value": "LTU"},
                                {"label": "Luxembourg", "value": "LUX"},
                                {"label": "Mexico", "value": "MEX"},
                                {"label": "Netherlands", "value": "NLD"},
                                {"label": "New Zealand", "value": "NZL"},
                                {"label": "Norway", "value": "NOR"},
                                {"label": "Poland", "value": "POL"},
                                {"label": "Portugal", "value": "PRT"},
                                {"label": "Slovak Republic", "value": "SVK"},
                                {"label": "Slovenia", "value": "SVN"},
                                {"label": "Spain", "value": "ESP"},
                                {"label": "Sweden", "value": "SWE"},
                                {"label": "Switzerland", "value": "CHE"},
                                {"label": "Turkey", "value": "TUR"},
                                {"label": "United Kingdom", "value": "GBR"},
                                {"label": "United States", "value": "USA"},
                            ],
                            multi=True,
                            clearable=False,
                            searchable=True,
                            value=["USA"],
                            placeholder="Select...",
                            className="twelve columns",
                            style={
                                "justify-content": "center",
                                "margin-bottom": "20px",
                            },
                        ),
                        # html.Div(
                        #     [
                        #         dcc.Tabs(
                        #             id="fin_tabs",
                        #             value="fin_sum_tab",
                        #             children=[
                        #                 dcc.Tab(
                        #                     label="OECD Summary Statistics",
                        #                     value="fin_sum_tab",
                        #                     className="custom_tab",
                        #                     selected_className="custom_tab_selected",
                        #                 ),
                        #                 dcc.Tab(
                        #                     label="Country-by-Country",
                        #                     value="fin_cntry_tab",
                        #                     className="custom-tab",
                        #                     selected_className="custom_tab_selected",
                        #                 ),
                        #             ],
                        #         )
                        #     ],
                        #     className="custom_tabs_container twelve columns",
                        # ),
                        html.Div(
                            [dcc.Graph(id="fig_tab2")],
                            className="twelve columns",
                            style={"margin-bottom": "20px"},
                        ),
                        html.Hr(),
                        dcc.Markdown(
                            """
                    ** Differences in Effective Rates by Asset Type **

                    These rates vary by asset and by form of financing in many jurisdictions, creating a tax-favored bias for some investments and their financing mechanisms.
                    """,
                            className="twelve columns",
                            style={"text-align": "justify"},
                            dangerously_allow_html=True,
                        ),
                        html.Label(
                            "Select or search for a country in the dropdown, below.",
                            style={"font-style": "italic", "font-size": "90%"},
                        ),
                        dcc.Dropdown(
                            id="asset-drop",
                            options=[
                                {"label": "Australia", "value": "AUS"},
                                {"label": "Austria", "value": "AUT"},
                                {"label": "Belgium", "value": "BEL"},
                                {"label": "Canada", "value": "CAN"},
                                {"label": "Chile", "value": "CHL"},
                                {"label": "Colombia", "value": "COL"},
                                {"label": "Czech Republic", "value": "CZE"},
                                {"label": "Denmark", "value": "DNK"},
                                {"label": "Estonia", "value": "EST"},
                                {"label": "Finland", "value": "FIN"},
                                {"label": "France", "value": "FRA"},
                                {"label": "Germany", "value": "DEU"},
                                {"label": "Greece", "value": "GRC"},
                                {"label": "Hungary", "value": "HUN"},
                                {"label": "Iceland", "value": "ISL"},
                                {"label": "Ireland", "value": "IRL"},
                                {"label": "Israel", "value": "ISR"},
                                {"label": "Italy", "value": "ITA"},
                                {"label": "Japan", "value": "JPN"},
                                {"label": "Korea", "value": "KOR"},
                                {"label": "Latvia", "value": "LVA"},
                                {"label": "Lithuania", "value": "LTU"},
                                {"label": "Luxembourg", "value": "LUX"},
                                {"label": "Mexico", "value": "MEX"},
                                {"label": "Netherlands", "value": "NLD"},
                                {"label": "New Zealand", "value": "NZL"},
                                {"label": "Norway", "value": "NOR"},
                                {"label": "Poland", "value": "POL"},
                                {"label": "Portugal", "value": "PRT"},
                                {"label": "Slovak Republic", "value": "SVK"},
                                {"label": "Slovenia", "value": "SVN"},
                                {"label": "Spain", "value": "ESP"},
                                {"label": "Sweden", "value": "SWE"},
                                {"label": "Switzerland", "value": "CHE"},
                                {"label": "Turkey", "value": "TUR"},
                                {"label": "United Kingdom", "value": "GBR"},
                                {"label": "United States", "value": "USA"},
                            ],
                            clearable=False,
                            searchable=True,
                            value="OECD",
                            placeholder="Select...",
                            className="twelve columns",
                            style={
                                "justify-content": "center",
                                "margin-bottom": "20px",
                            },
                        ),
                        # html.Div(
                        #     [
                        #         dcc.Tabs(
                        #             id="asset_tabs",
                        #             value="asset_sum_tab",
                        #             children=[
                        #                 dcc.Tab(
                        #                     label="OECD Summary Statistics",
                        #                     value="asset_sum_tab",
                        #                     className="custom_tab",
                        #                     selected_className="custom_tab_selected",
                        #                 ),
                        #                 dcc.Tab(
                        #                     label="Country-by-Country",
                        #                     value="asset_cntry_tab",
                        #                     className="custom-tab",
                        #                     selected_className="custom_tab_selected",
                        #                 ),
                        #             ],
                        #         )
                        #     ],
                        #     className="custom_tabs_container twelve columns",
                        # ),
                        html.Div(
                            [dcc.Graph(id="fig_tab3")],
                            className="twelve columns",
                        ),
                    ],
                    className="effect_container twelve columns",
                ),
                # [
                #     # tax treatment dropdown
                #     html.Label("Tax Treatment"),
                #     dcc.Dropdown(
                #         id="treatment",
                #         options=[
                #             {"label": "Overall", "value": "overall"},
                #             {"label": "Corporate", "value": "corporate"},
                #             {"label": "Non-Corporate", "value": "non-corporate"},
                #         ],
                #         value="overall",
                #     ),
                # ],
                # className="three columns",
                # style={"justify-content": "center"},
                # ),
                #     html.P("Data Source: Revenue Estimates are from US Department of Treasury; EATRs are from Author.", className="control_label",style={"text-align": "right", "font-style": "italic", "font-size": "80%"}),
            ],
            className="description_container twelve columns",
        ),
        # FOOTER
        html.Hr(),
        html.Div(
            [
                dcc.Markdown(
                    """
                **Note:**
                This dashboard is an extension of research presented in X (Pomerleau, 2021). The code that powers this data visualization can be found
                <a href="https://github.com/grantseiter/" children="here" style="color:#008CCC" target="blank" />.
                Feedback or questions? Contact us <a href="mailto:Grant.Seiter@AEI.org" children="here" style="color:#008CCC" />.
                """,
                    dangerously_allow_html=True,
                )
            ],
            className="footer twelve columns",
        ),
    ]
)


@app.callback(
    Output("prop_text", "children"),
    Input("variable_selection", "value"),
)
def update(variable_selection):
    if variable_selection == "ALL":
        text = """
        **Summary of All Proposals**

        Under the administration’s proposals, US-headquartered corporations would face worldwide taxation on all their profits. Profits earned in the United States would face a tax rate of 28 percent, and all foreign profits would face a minimum tax rate of 21 percent under a reformed version of GILTI (global intangible low-taxed income). In addition, the administration would introduce new anti–base erosion provisions (SHIELD: Stopping Harmful Inversions and Ending Low-Tax Developments) and a new minimum tax on book profits. It is also pursuing a multilateral agreement aimed at reforming the tax treatment of multinational corporations throughout the world.

        Over the period 2022-2031, the administration's proposals would raise over $2 trillion in revenue.
        """
    if variable_selection == "CTR":
        text = """
        **Summary of the Corporate Tax Rate Proposal**

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi id congue enim. Morbi eget felis a leo ultricies semper. Donec et libero pellentesque, pharetra neque id, ultricies sem. Etiam pulvinar tristique viverra. Etiam at neque consequat, pharetra purus et, malesuada quam. Mauris et ex ultrices, tristique diam eu, molestie justo. Vivamus dapibus elit rhoncus nisl convallis tempus. Quisque aliquet metus quis lectus euismod, at commodo nulla volutpat. Phasellus et nisi id odio sodales condimentum. Vestibulum facilisis sagittis ultricies. Maecenas sit amet metus at mauris varius porttitor non ut ante.

        Over the period 2022-2031, increasing the corporate tax rate from 21% to 28% would raise $858 billion in revenue.
        """
    if variable_selection == "GILTI":
        text = """
        **Summary of the GILTI Reform Proposal**

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi id congue enim. Morbi eget felis a leo ultricies semper. Donec et libero pellentesque, pharetra neque id, ultricies sem. Etiam pulvinar tristique viverra. Etiam at neque consequat, pharetra purus et, malesuada quam. Mauris et ex ultrices, tristique diam eu, molestie justo. Vivamus dapibus elit rhoncus nisl convallis tempus. Quisque aliquet metus quis lectus euismod, at commodo nulla volutpat. Phasellus et nisi id odio sodales condimentum. Vestibulum facilisis sagittis ultricies. Maecenas sit amet metus at mauris varius porttitor non ut ante.

        Over the period 2022-2031, the administration's GILTI reform proposal would raise $534 billion in revenue.
        """
    if variable_selection == "FDII":
        text = """
        **Summary of the FDII Repeal Proposal**

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi id congue enim. Morbi eget felis a leo ultricies semper. Donec et libero pellentesque, pharetra neque id, ultricies sem. Etiam pulvinar tristique viverra. Etiam at neque consequat, pharetra purus et, malesuada quam. Mauris et ex ultrices, tristique diam eu, molestie justo. Vivamus dapibus elit rhoncus nisl convallis tempus. Quisque aliquet metus quis lectus euismod, at commodo nulla volutpat. Phasellus et nisi id odio sodales condimentum. Vestibulum facilisis sagittis ultricies. Maecenas sit amet metus at mauris varius porttitor non ut ante.

        Over the period 2022-2031, the FDII repeal proposal would be offset by research and development incentives.
        """
    if variable_selection == "SHIELD":
        text = """
        **Summary of the SHIELD Proposal**

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi id congue enim. Morbi eget felis a leo ultricies semper. Donec et libero pellentesque, pharetra neque id, ultricies sem. Etiam pulvinar tristique viverra. Etiam at neque consequat, pharetra purus et, malesuada quam. Mauris et ex ultrices, tristique diam eu, molestie justo. Vivamus dapibus elit rhoncus nisl convallis tempus. Quisque aliquet metus quis lectus euismod, at commodo nulla volutpat. Phasellus et nisi id odio sodales condimentum. Vestibulum facilisis sagittis ultricies. Maecenas sit amet metus at mauris varius porttitor non ut ante.

        Over the period 2022-2031, the administration's SHIELD proposal would raise $390 billion in revenue.
        """
    if variable_selection == "BOOK":
        text = """
        **Summary of the Book Tax Proposal**

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi id congue enim. Morbi eget felis a leo ultricies semper. Donec et libero pellentesque, pharetra neque id, ultricies sem. Etiam pulvinar tristique viverra. Etiam at neque consequat, pharetra purus et, malesuada quam. Mauris et ex ultrices, tristique diam eu, molestie justo. Vivamus dapibus elit rhoncus nisl convallis tempus. Quisque aliquet metus quis lectus euismod, at commodo nulla volutpat. Phasellus et nisi id odio sodales condimentum. Vestibulum facilisis sagittis ultricies. Maecenas sit amet metus at mauris varius porttitor non ut ante.

        Over the period 2022-2031, the administration's book tax propoasl would raise $148 billion in revenue.
        """
    return text


@app.callback(
    Output("revenue_table", "style_data_conditional"),
    Input("variable_selection", "value"),
)
def update(variable_selection):
    if variable_selection == "ALL":
        rowval = 7
    if variable_selection == "CTR":
        rowval = 0
    if variable_selection == "GILTI":
        rowval = 1
    if variable_selection == "FDII":
        rowval = 2
    if variable_selection == "SHIELD":
        rowval = 3
    if variable_selection == "BOOK":
        rowval = 5
    return get_style_data_conditional(rowval)


@app.callback(
    Output("bar_figure", "figure"),
    Input("bar_figure_tabs", "value"),
)
def update(bar_figure_tabs):
    if bar_figure_tabs == "stat_tab":
        rate = "statutory_corptax"
        ratetitle = "Statutory Corporate Tax Rates"
        ratelabel = "Corporate Rate"
    if bar_figure_tabs == "metr_tab":
        rate = "metr_overall"
        ratetitle = "Marginal Effective Corporate Tax Rates (METRs)"
        ratelabel = "METR"
    if bar_figure_tabs == "aetr_tab":
        rate = "aetr_overall"
        ratetitle = "Average Effective Corporate Tax Rates (AETRs)"
        ratelabel = "AETR"

    bar_figure = make_bar_figure(rate, ratetitle, ratelabel)

    return bar_figure


server = app.server
# turn debug=False for production
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)
