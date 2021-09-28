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

stylesheets = ["styles.css"]

image_filename = "assets/aei_logo.png"
encoded_image = base64.b64encode(open(image_filename, "rb").read())

pio.templates.default = "plotly_white"

APP_PATH = os.path.abspath(os.path.dirname(__file__))

# Data
output = pd.read_csv("data/output.csv")

# Code
def make_bar_figure(rate, ratetitle, ratelabel, stat_marker):
    """
    Function creates bar chart for section one.
    """
    data = output[0:39]
    data = data.sort_values(by=[rate], ascending=True).reset_index(drop=True)
    oecd_avg = np.average(data[rate], weights=data["weight"])
    btm = data.name[0]
    mid = data.name[12]
    top = data.name[38]
    usloc = int(data[data["name"] == "United States (Current Law)"].index[0])
    ushloc = int(data[data["name"] == "United States (House)"].index[0])
    usbloc = int(data[data["name"] == "United States (Biden)"].index[0])

    colors = ["#008CCC"] * 100
    colors[usloc] = "#00D56F"
    colors[ushloc] = "#FFB400"
    colors[usbloc] = "#FF8100"
    stat_colors = ["#67C5F0"] * 100
    stat_colors[usloc] = "#00D56F"
    stat_colors[ushloc] = "#FFB400"
    stat_colors[usbloc] = "#FF8100"

    bar_figure = go.Figure(
        data=go.Bar(
            x=data["name"],
            y=data[rate],
            marker_color=colors,
            name=ratelabel,
        )
    )

    if stat_marker:
        bar_figure.add_trace(
            go.Scatter(
                x=data["name"],
                y=data["statutory_tax_rate"],
                mode="markers",
                marker_color=stat_colors,
                name="Statutory Rate",
            )
        )

    bar_figure.add_trace(
        go.Scatter(
            x=[btm, mid, top],
            y=[oecd_avg, oecd_avg, oecd_avg],
            mode="lines+text",
            name=ratelabel,
            text=["", "OECD Average " + ratelabel, ""],
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
        title=ratetitle
        + " in the OECD, Current Law and Proposals "
        + "<br><sup><i>Hover over data to view more information.</i></sup>",
        yaxis=dict(
            gridcolor="#F2F2F2",
            tickformat=".1%",
        ),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
    )

    bar_figure.update_layout(layout)

    return bar_figure


def make_country_figure(country1, country2, measure, measurename, measuretitle):
    """
    Function creates scatter chart for section two.
    """
    df = output[0:40]
    data1 = (df.loc[(df["country"] == country1)]).reset_index(drop=True)
    data2 = (df.loc[(df["country"] == country2)]).reset_index(drop=True)

    data1_assets = data1[
        [
            "country",
            "name",
            measure + "_land",
            measure + "_inventory",
            measure + "_ip",
            measure + "_buildings",
            measure + "_machines",
        ]
    ]
    data2_assets = data2[
        [
            "country",
            "name",
            measure + "_land",
            measure + "_inventory",
            measure + "_ip",
            measure + "_buildings",
            measure + "_machines",
        ]
    ]
    data1_assets = data1_assets.rename(
        columns={
            measure + "_machines": "Machines",
            measure + "_buildings": "Buildings",
            measure + "_ip": "Intellectual Property",
            measure + "_land": "Land",
            measure + "_inventory": "Inventory",
        }
    )
    data2_assets = data2_assets.rename(
        columns={
            measure + "_machines": "Machines",
            measure + "_buildings": "Buildings",
            measure + "_ip": "Intellectual Property",
            measure + "_land": "Land",
            measure + "_inventory": "Inventory",
        }
    )
    data1_assets = pd.melt(data1_assets, id_vars=["country", "name"])
    data2_assets = pd.melt(data2_assets, id_vars=["country", "name"])

    def make_fig(country1, country2, measure, measurename, measuretitle):
        """
        creates the Plotly traces
        """
        assets_trace1 = go.Scatter(
            x=data1_assets["value"],
            y=data1_assets["variable"],
            marker=dict(
                size=20,
                color="#008CCC",
            ),
            mode="markers",
            name=data1_assets["name"][0],
            marker_symbol="circle",
        )
        assets_trace2 = go.Scatter(
            x=data2_assets["value"],
            y=data2_assets["variable"],
            marker=dict(
                size=20,
                color="#FFB400",
            ),
            mode="markers",
            name=data2_assets["name"][0],
            marker_symbol="circle",
        )

        layout = go.Layout(
            title="<i>"
            + data1_assets["name"][0]
            + " vs. "
            + data2_assets["name"][0]
            + ",</i>"
            + " "
            + measuretitle
            + " by Asset and Form of Financing"
            + "<br><sup><i>Hover over data to view more information. Toggle legend items to show or hide elements.</i></sup>",
            xaxis=dict(
                tickformat=".1%",
                gridcolor="#F2F2F2",
                zeroline=False,
            ),
            yaxis=dict(gridcolor="#8E919A", linecolor="#F2F2F2", type="category"),
            paper_bgcolor="#F2F2F2",
            plot_bgcolor="#F2F2F2",
            height=400,
        )

        fig = go.Figure(data=[assets_trace1, assets_trace2], layout=layout)
        return fig

    country_figure = make_fig(
        country1,
        country2,
        measure,
        measurename,
        measuretitle,
    )

    return country_figure


def make_financing_figure(rate, ratetitle, ratelabel_bar, ratelabel_point):
    """
    Function creates bar chart for section three.
    """
    data = output[0:39]
    data = data.sort_values(by=[rate + "_debt_bias"], ascending=True).reset_index(
        drop=True
    )
    oecd_avg = np.average(data[rate + "_debt_bias"], weights=data["weight"])
    btm = data.name[0]
    mid = data.name[12]
    top = data.name[38]
    usloc = int(data[data["name"] == "United States (Current Law)"].index[0])
    ushloc = int(data[data["name"] == "United States (House)"].index[0])
    usbloc = int(data[data["name"] == "United States (Biden)"].index[0])

    colors = ["#008CCC"] * 100
    colors[usloc] = "#00D56F"
    colors[ushloc] = "#FFB400"
    colors[usbloc] = "#FF8100"
    stat_colors = ["#8E919A"] * 100
    stat_colors[usloc] = "#00D56F"
    stat_colors[ushloc] = "#FFB400"
    stat_colors[usbloc] = "#FF8100"

    fig_bar = go.Bar(
        x=data["name"],
        y=data[rate + "_debt_bias"],
        marker_color=colors,
        name=ratelabel_bar,
    )
    fig_equity = go.Scatter(
        x=data["name"],
        y=data[rate + "_equity_overall"],
        mode="markers",
        marker_symbol="circle",
        marker_size=8,
        marker_color=stat_colors,
        marker_line_color="#8E919A",
        marker_line_width=2,
        name=ratelabel_point + " on Equity <br>Financed Investment",
    )
    fig_debt = go.Scatter(
        x=data["name"],
        y=data[rate + "_debt_overall"],
        mode="markers",
        marker_symbol="square-open",
        marker_size=8,
        marker_color=stat_colors,
        marker_line_width=2,
        name=ratelabel_point + " on Debt <br>Financed Investment",
    )
    fig_oecd = go.Scatter(
        x=[btm, mid, top],
        y=[oecd_avg, oecd_avg, oecd_avg],
        mode="lines+text",
        name="OECD Average<br>" + ratelabel_bar,
        text=["", "OECD Average " + ratelabel_bar, ""],
        textposition="top center",
        textfont=dict(color="#FB0023"),
        line=dict(
            color="#FB0023",
            dash="dash",
        ),
        hovertemplate="(OECD Average, %{y})",
        hoverlabel=dict(bgcolor="#FB0023"),
    )
    layout = go.Layout(
        title=ratelabel_bar
        + ", Measured by "
        + ratetitle
        + " in the OECD, Current Law and Proposals"
        + "<br><sup><i>Hover over data to view more information. Toggle legend items to show or hide elements.</i></sup>",
        yaxis=dict(
            gridcolor="#F2F2F2",
            tickformat=".1%",
            zerolinecolor="#F2F2F2",
        ),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        height=600,
    )
    financing_figure = go.Figure(
        data=[fig_equity, fig_debt, fig_bar, fig_oecd], layout=layout
    )
    return financing_figure


def make_alternative_figure(rate, ratetitle, ratelabel, alternative, axisrange):
    """
    Function creates bar chart for section four.
    """
    data = output[0:39]
    data_alt = output[40:]
    data = data.sort_values(by=[rate], ascending=True).reset_index(drop=True)
    oecd_avg = np.average(data[rate], weights=data["weight"])
    btm = data.name[0]
    mid = data.name[12]
    top = data.name[38]

    usloc = int(data[data["name"] == "United States (Current Law)"].index[0])
    ushloc = int(data[data["name"] == "United States (House)"].index[0])
    usbloc = int(data[data["name"] == "United States (Biden)"].index[0])

    hoverlabel = ""

    if alternative != "CL":
        if alternative == "BONUS":
            cl_alt = data_alt[data_alt["country"] == "USA_1"]
            cl_alt = cl_alt.set_index([pd.Index([usloc])])
            data.loc[cl_alt.index] = np.nan
            data = data.combine_first(cl_alt)
            h_alt = data_alt[data_alt["country"] == "USA_H1"]
            h_alt = h_alt.set_index([pd.Index([ushloc])])
            data.loc[h_alt.index] = np.nan
            data = data.combine_first(h_alt)
            b_alt = data_alt[data_alt["country"] == "USA_B1"]
            b_alt = b_alt.set_index([pd.Index([usbloc])])
            data.loc[b_alt.index] = np.nan
            data = data.combine_first(b_alt)
            hoverlabel = "100% Bonus Depreciation"
        if alternative == "RND":
            cl_alt = data_alt[data_alt["country"] == "USA_2"]
            cl_alt = cl_alt.set_index([pd.Index([usloc])])
            data.loc[cl_alt.index] = np.nan
            data = data.combine_first(cl_alt)
            h_alt = data_alt[data_alt["country"] == "USA_H2"]
            h_alt = h_alt.set_index([pd.Index([ushloc])])
            data.loc[h_alt.index] = np.nan
            data = data.combine_first(h_alt)
            b_alt = data_alt[data_alt["country"] == "USA_B2"]
            b_alt = b_alt.set_index([pd.Index([usbloc])])
            data.loc[b_alt.index] = np.nan
            data = data.combine_first(b_alt)
            hoverlabel = "100% Bonus Depreciation<br>and R&D Expensing"
        if alternative == "EBITDA":
            cl_alt = data_alt[data_alt["country"] == "USA_3"]
            cl_alt = cl_alt.set_index([pd.Index([usloc])])
            data.loc[cl_alt.index] = np.nan
            data = data.combine_first(cl_alt)
            h_alt = data_alt[data_alt["country"] == "USA_H3"]
            h_alt = h_alt.set_index([pd.Index([ushloc])])
            data.loc[h_alt.index] = np.nan
            data = data.combine_first(h_alt)
            b_alt = data_alt[data_alt["country"] == "USA_B3"]
            b_alt = b_alt.set_index([pd.Index([usbloc])])
            data.loc[b_alt.index] = np.nan
            data = data.combine_first(b_alt)
            hoverlabel = "100% Bonus Depreciation,<br>R&D Expensing,<br>and 30% EBITDA Limitation"
        if alternative == "FDII":
            cl_alt = data_alt[data_alt["country"] == "USA_4"]
            cl_alt = cl_alt.set_index([pd.Index([usloc])])
            data.loc[cl_alt.index] = np.nan
            data = data.combine_first(cl_alt)
            h_alt = data_alt[data_alt["country"] == "USA_H4"]
            h_alt = h_alt.set_index([pd.Index([ushloc])])
            data.loc[h_alt.index] = np.nan
            data = data.combine_first(h_alt)
            b_alt = data_alt[data_alt["country"] == "USA_B4"]
            b_alt = b_alt.set_index([pd.Index([usbloc])])
            data.loc[b_alt.index] = np.nan
            data = data.combine_first(b_alt)
            hoverlabel = "100% Bonus Depreciation,<br>R&D Expensing,<br>30% EBITDA Limitation,<br>and FDII"

    data = data.sort_values(by=[rate], ascending=True).reset_index(drop=True)
    btm = data.name[0]
    mid = data.name[12]
    top = data.name[38]

    usloc = int(data[data["name"] == "United States (Current Law)"].index[0])
    ushloc = int(data[data["name"] == "United States (House)"].index[0])
    usbloc = int(data[data["name"] == "United States (Biden)"].index[0])

    colors = ["#008CCC"] * 100
    colors[usloc] = "#00D56F"
    colors[ushloc] = "#FFB400"
    colors[usbloc] = "#FF8100"
    stat_colors = ["#67C5F0"] * 100
    stat_colors[usloc] = "#00D56F"
    stat_colors[ushloc] = "#FFB400"
    stat_colors[usbloc] = "#FF8100"

    alternative_figure = go.Figure(
        data=go.Bar(
            x=data["name"],
            y=data[rate],
            marker_color=colors,
            name=ratelabel,
        )
    )

    alternative_figure.add_trace(
        go.Scatter(
            x=[btm, mid, top],
            y=[oecd_avg, oecd_avg, oecd_avg],
            mode="lines+text",
            name=ratelabel,
            text=["", "OECD Average " + ratelabel, ""],
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

    if alternative != "CL":
        alternative_figure.add_trace(
            go.Scatter(
                x=[
                    "United States (Current Law)",
                    "United States (House)",
                    "United States (Biden)",
                ],
                y=[
                    data[rate][usloc] + 0.015,
                    data[rate][ushloc] + 0.015,
                    data[rate][usbloc] + 0.015,
                ],
                mode="markers",
                marker_symbol="asterisk",
                marker_size=8,
                marker_line_color=["#00D56F", "#FFB400", "#FF8100"],
                marker_line_width=1,
                name="Alternative Policy",
                hovertemplate="<b>This Estimate Includes:</b><br>" + hoverlabel,
            )
        )

    layout = go.Layout(
        showlegend=False,
        title=ratetitle
        + " in the OECD, Current Law, Proposals, and Alternative Policies"
        + "<br><sup><i>Hover over data to view more information.</i></sup>",
        yaxis=dict(
            gridcolor="#8E919A",
            zerolinecolor="#8E919A",
            tickformat=".1%",
            range=axisrange,
        ),
        paper_bgcolor="#F2F2F2",
        plot_bgcolor="#F2F2F2",
        height=500,
    )

    alternative_figure.update_layout(layout)

    return alternative_figure


# Initialize App
app = dash.Dash(
    url_base_pathname=os.environ.get("URL_BASE_PATHNAME", "/"),
    external_stylesheets=stylesheets,
)

# Create App Layout
app.layout = html.Div(
    [
        # HEADER
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
            ## The Tax Burden on Corporations and Proposals to Reform the US Tax System
            """
            """
            *Modeling by <a href="https://www.aei.org/profile/kyle-pomerleau/" children="Kyle Pomerleau" style="color:#4f5866;text-decoration:none" target="blank" />. Dashboard development by <a href="https://grantseiter.com/" children="Grant M. Seiter" style="color:#4f5866;text-decoration:none" target="blank" />.*
            """,
            style={"max-width": "1000px"},
            dangerously_allow_html=True,
        ),
        html.Div(
            [
                dcc.Markdown(
                    """
                    The Biden Administration and Democratic lawmakers in Congress are now considering proposals to raise the tax burden on corporations in the United States. Their proposals would increase the corporate income tax rate from 21 percent to a rate between 25 percent and 28 percent. In addition, they have proposed reforming the tax treatment of foreign profits of US multinational corporations and repealing or reforming FDII. Their goals are to increase federal revenue, increase the tax burden on capital income, and reduce profit shifting by US multinational corporations. 
                    
                    This dashboard compares the tax burden on corporations in the United States under current law to the corporate tax burdens of 36 member nations of the Organisation for Economic Co-operation and Development (OECD). It also considers two leading proposals to reform US corporate income taxation and several alternative changes to policy.
                    """,
                    style={"text-align": "justify"},
                ),
            ],
            className="twelve columns",
        ),
        # COMPARING TAX RATES (SECTION ONE)
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
                Corporate tax systems are complex and vary significantly throughout the OECD. There is no single measure of the corporate tax burden that captures every aspect of a corporate income tax. This analysis focuses on three measures: the combined statutory corporate income tax rate, the marginal effective corporate tax rate (METR), and the average effective corporate tax rate (AETR). Each measure represents a different component of a corporation’s tax burden and can be used to evaluate how a corporate income tax may distort behavior.
                """,
                    className="twelve columns",
                    style={"text-align": "justify"},
                    dangerously_allow_html=True,
                ),
                html.Label(
                    "Toggle the tabs below to view estimates of each measure.",
                    className="twelve columns",
                    style={
                        "font-style": "italic",
                        "font-size": "90%",
                        "margin-bottom": "10px",
                    },
                ),
                dcc.Markdown(
                    """            
                 **The Statutory Corporate Income Tax Rate** is the rate at which each dollar of corporate taxable income is taxed. Statutory corporate tax rates in the OECD include both central (federal) corporate rates and sub-central (state and local) tax rates. The statutory corporate tax rate impacts the incentive to locate profits in a given jurisdiction.

                **The Marginal Effective Tax Rate (METR)** measures the tax burden on marginal investment for an investment that breaks even in present value. The METR incorporates the statutory tax rate, deductions and credits that corporations receive for new investments, special lower tax rates for certain types of income, and deductions for financing costs (interest payments or equity payments). The METR measures the impact a corporate tax has on the level of investment in a country.
                 
                **The Average Effective Tax Rate (AETR)** measures the tax burden on new investments that earn above-normal returns or economic rents. Like the METR, the AETR considers both the statutory corporate tax rate, deductions, credits, and other special provisions that a tax system may provide. This rate can affect the decision to locate investment in different jurisdictions. 
                """,
                    className="results_container three columns",
                    style={
                        "text-align": "justify",
                        "margin-bottom": "10px",
                        "font-size": "90%",
                    },
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
                dcc.Markdown(
                    id="analysis_text",
                    className="eight columns",
                    style={"text-align": "justify"},
                    dangerously_allow_html=True,
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
                # ASSET BIAS (SECTION TWO)
                html.Div(
                    [
                        dcc.Markdown(
                            """
                    ** Effective Tax Rates by Asset Type **

                    Effective tax rates in the OECD vary significantly by type of asset. Some countries provide accelerated depreciation for certain assets. Effective tax rates also can be impacted by special lower tax rates on certain assets. For example, several countries provide special lower tax rates on intellectual property (IP) products through patent boxes. The United States provides a lower tax rate on imputed returns to IP through FDII.

                    Under current law, the US marginal effective tax rate on buildings (19 percent), inventories (25.8 percent), and land (17.5 percent) are all higher than the OECD averages. The US METR on IP (13.8 percent) is significantly higher than the OECD average, under the current-law specification, which assumes that the requirement to amortize research and development expenses (slated to take effect in 2022) is in place. That requirement is unique to the United States. Proposals in the United States to increase the corporate tax burden would raise the METR on all assets.

                    The US average effective tax rate under current law on each asset is roughly in line with the OECD average except for intellectual property. The higher-than-average AETR on IP reflects the amortization of research and development costs under current law. IP still faces a slightly lower AETR than other assets in the United States, however, due to FDII. Under either proposal to increase the US corporate tax burden, AETRs on all assets would be the highest or close to the highest in the OECD. 
                    """,
                            className="twelve columns",
                            style={"text-align": "justify"},
                            dangerously_allow_html=True,
                        ),
                        html.Label(
                            "Select an effective tax rate to display in the figure below.",
                            style={"font-style": "italic", "font-size": "90%"},
                            className="twelve columns",
                        ),
                        dcc.Dropdown(
                            id="country_drop_rate",
                            options=[
                                {
                                    "label": "Marginal Effective Tax Rate (METR)",
                                    "value": "metr",
                                },
                                {
                                    "label": "Average Effective Tax Rate (AETR)",
                                    "value": "aetr",
                                },
                            ],
                            value="metr",
                            clearable=False,
                            searchable=False,
                            className="twelve columns",
                            style={
                                "justify-content": "center",
                                "margin-bottom": "5px",
                            },
                        ),
                        html.Label(
                            "Select two different countries to compare.",
                            style={"font-style": "italic", "font-size": "90%"},
                            className="twelve columns",
                        ),
                        dcc.Dropdown(
                            id="country_drop_value1",
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
                                {"label": "OECD Average", "value": "OECD"},
                                {"label": "Poland", "value": "POL"},
                                {"label": "Portugal", "value": "PRT"},
                                {"label": "Slovakia", "value": "SVK"},
                                {"label": "Slovenia", "value": "SVN"},
                                {"label": "Spain", "value": "ESP"},
                                {"label": "Sweden", "value": "SWE"},
                                {"label": "Switzerland", "value": "CHE"},
                                {"label": "Turkey", "value": "TUR"},
                                {"label": "United Kingdom", "value": "GBR"},
                                {
                                    "label": "United States (Current Law)",
                                    "value": "USA",
                                },
                                {"label": "United States (House)", "value": "USA_H"},
                                {"label": "United States (Biden)", "value": "USA_B"},
                            ],
                            multi=False,
                            clearable=False,
                            searchable=True,
                            value="USA",
                            className="six columns",
                            style={
                                "justify-content": "center",
                            },
                        ),
                        dcc.Dropdown(
                            id="country_drop_value2",
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
                                {"label": "OECD Average", "value": "OECD"},
                                {"label": "Poland", "value": "POL"},
                                {"label": "Portugal", "value": "PRT"},
                                {"label": "Slovakia", "value": "SVK"},
                                {"label": "Slovenia", "value": "SVN"},
                                {"label": "Spain", "value": "ESP"},
                                {"label": "Sweden", "value": "SWE"},
                                {"label": "Switzerland", "value": "CHE"},
                                {"label": "Turkey", "value": "TUR"},
                                {"label": "United Kingdom", "value": "GBR"},
                                {
                                    "label": "United States (Current Law)",
                                    "value": "USA",
                                },
                                {"label": "United States (House)", "value": "USA_H"},
                                {"label": "United States (Biden)", "value": "USA_B"},
                            ],
                            multi=False,
                            clearable=False,
                            searchable=True,
                            value="OECD",
                            className="six columns",
                            style={
                                "justify-content": "center",
                            },
                        ),
                        html.Div(
                            [dcc.Graph(id="country_figure")],
                            className="twelve columns",
                            style={
                                "justify-content": "center",
                            },
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
                    ],
                    className="effect_container twelve columns",
                ),
                # FINANCING BIAS (SECTION THREE)
                html.Div(
                    [
                        dcc.Markdown(
                            """
                    ** Effective Tax Rates by Source of Financing  **

                    Corporations can finance new projects through equity by using either retained earnings or issuing new shares. Alternatively, corporations can finance new investments with debt by issuing bonds. Equity payments made to shareholders (dividends) are not deductible against taxable income, while interest on debt is deductible against taxable income. Debt-financed investment is therefore tax-preferred. Some countries have policies that offset the traditional bias in favor of debt, such as allowances for corporate equity, limitations on interest expense, or cash-flow taxes (which mostly avoid the debt-equity bias by disallowing interest deductions).

                    Under current law, the US corporate tax creates a 29-percentage point bias in favor of debt-financed investment as measured by METRs (7.1 percentage points as measured by AETRs). This is slightly below the OECD average of 31.8 percent (7.3 percent for AETRs) and is in line with most countries. However, the Biden and House Ways and Means proposals would increase the bias in favor of debt-financed investment by increasing the value of the interest deduction (because the deductions would be claimed at the new higher corporate tax rates) and raising the tax burden on equity-financed investment. Under the House Ways and Means proposal, the bias in favor of debt (35.0 percent for METRs and 8.6 percent for AETRs) would be slightly higher than the OECD average (31.8 percent and 7.3 percent). Under Biden’s proposal, the bias in favor of debt (36.9 percent and 9 percent) would also be slightly above the OECD average.
                    """,
                            className="twelve columns",
                            style={"text-align": "justify"},
                            dangerously_allow_html=True,
                        ),
                        html.Label(
                            "Select a different effective tax rate to display in the figure below.",
                            style={"font-style": "italic", "font-size": "90%"},
                            className="twelve columns",
                        ),
                        dcc.Dropdown(
                            id="financing_drop_rate",
                            options=[
                                {
                                    "label": "Marginal Effective Tax Rate (METR)",
                                    "value": "metr",
                                },
                                {
                                    "label": "Average Effective Tax Rate (AETR)",
                                    "value": "aetr",
                                },
                            ],
                            value="metr",
                            clearable=False,
                            searchable=False,
                            className="twelve columns",
                            style={
                                "justify-content": "center",
                                "margin-bottom": "5px",
                            },
                        ),
                        html.Div(
                            [dcc.Graph(id="financing_figure")],
                            className="twelve columns",
                            style={
                                "justify-content": "center",
                            },
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
                    ],
                    className="effect2_container twelve columns",
                ),
                # ALTERNATIVE POLICIES (SECTION FOUR)
                html.Div(
                    [
                        dcc.Markdown(
                            """
                        ** Impact of Alternative Policies on Effective Tax Rates in the United States **

                         The effective tax rate estimates for the OECD countries, above, reflect current law and exclude temporary policies scheduled to change over the next decade. For the United States, the estimates exclude 100 percent bonus depreciation, which is scheduled to phase out over five years starting in 2023 and include amortization of research and development costs and tighter limitations on net interest expenses, which are scheduled to change in 2022. Likewise, the deduction for FDII is set to 21.875 percent, which is its scheduled value in 2026. Extending temporary proposals and maintaining FDII at current policy levels would have a significant impact on the tax burden on investment in the United States. The interactive figure below allows users to consider the impact of maintaining these alternative policies on effective tax rates in the United States.
                        """,
                            className="twelve columns",
                            style={"text-align": "justify"},
                            dangerously_allow_html=True,
                        ),
                        html.Label(
                            "Use the buttons and toggle the tabs to update US effective tax rates in the figure below. The impact of each policy includes the sum of the previous policies.",
                            style={
                                "font-style": "italic",
                                "font-size": "90%",
                                "margin-bottom": "10px",
                            },
                            className="twelve columns",
                        ),
                        html.Div(
                            [
                                dcc.RadioItems(
                                    id="alternative_radio_value",
                                    options=[
                                        {"label": "Current Law", "value": "CL"},
                                        {
                                            "label": "(1) Maintain 100% Bonus Depreciation",
                                            "value": "BONUS",
                                        },
                                        {
                                            "label": "(2) Maintain R&D Expensing",
                                            "value": "RND",
                                        },
                                        {
                                            "label": "(3) Maintain 30% EBITDA Limitation",
                                            "value": "EBITDA",
                                        },
                                        {"label": "(4) Maintain FDII", "value": "FDII"},
                                    ],
                                    value="CL",
                                    labelStyle={
                                        "width": "160%",
                                        "display": "inline-block",
                                    },
                                ),
                                dcc.Markdown(
                                    id="alternative_text",
                                    style={
                                        "text-align": "justify",
                                        "margin-top": "20px",
                                        "margin-bottom": "20px",
                                    },
                                    dangerously_allow_html=True,
                                ),
                            ],
                            className="three columns",
                        ),
                        html.Div(
                            [
                                dcc.Tabs(
                                    id="alternative_figure_tabs",
                                    value="metr_tab",
                                    children=[
                                        dcc.Tab(
                                            label="Marginal Rate (METR)",
                                            value="metr_tab",
                                            className="custom-tab",
                                            selected_className="custom_tab2_selected",
                                        ),
                                        dcc.Tab(
                                            label="Average Rate (AETR)",
                                            value="aetr_tab",
                                            className="custom-tab",
                                            selected_className="custom_tab2_selected",
                                        ),
                                    ],
                                ),
                            ],
                            className="custom_tabs_container eight columns",
                        ),
                        html.Div(
                            [
                                dcc.Graph(id="alternative_figure"),
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
                    ],
                    className="effect_container twelve columns",
                ),
            ],
            className="description_container twelve columns",
        ),
        # FOOTER
        html.Hr(),
        html.Div(
            [
                dcc.Markdown(
                    """
                **Notes:** This dashboard is an extension of research presented in *The Tax Burden on Corporations: A Comparison of OECD Countries and Proposals to Reform the US Tax System* (Pomerleau, forthcoming). The code that powers this data visualization can be found
                <a href="https://github.com/grantseiter/OECD-Corporate-Tax-Burden-App" children="here" style="color:#008CCC" target="blank" />.
                Feedback or questions? Contact us <a href="mailto:Grant.Seiter@AEI.org" children="here" style="color:#008CCC" />.

                Effective tax rates on corporate investment were estimated using a framework developed by Devereux and Griffith (1999) and by generally following the method outlined in Spengel et. Al. (2019). These rates are forward-looking and measure the tax burden that a corporation expects to pay on new domestic investment in each jurisdiction. The parameters used to estimate effective tax rates reflect current law in each country and are set to their long-run values. As such, this analysis ignores several temporary changes made to corporate taxes in response to the COVID-19 pandemic. The full methodology is detailed in *The Tax Burden on Corporations: A Comparison of OECD Countries and Proposals to Reform the US Tax System* (Pomerleau, forthcoming). 
                    
                For more details on additional corporate tax reforms put forth by the Biden Administration and lawmakers in congress, see <a href="https://www.aei.org/research-products/report/bidens-reforms-to-the-tax-treatment-of-us-multinational-corporations-the-knowns-and-unknowns/" children="Biden’s Reforms to the Tax Treatment of US Multinational Corporations: The Knowns and Unknowns" style="color:#008CCC;font-style:italic" target="blank" /> (Pomerleau, 2021).
                """,
                    dangerously_allow_html=True,
                    style={
                        "font-size": "90%",
                        "margin-bottom": "10px",
                    },
                ),
                html.Div(
                    [
                        html.Button(
                            "Download Data as CSV",
                            id="btn_csv",
                            style={
                                "font-size": "90%",
                                "margin-bottom": "20px",
                            },
                        ),
                        dcc.Download(id="download-dataframe-csv"),
                    ]
                ),
            ],
            className="footer twelve columns",
        ),
    ]
)

# Callbacks
@app.callback(
    Output("bar_figure", "figure"),
    Input("bar_figure_tabs", "value"),
)
def update(bar_figure_tabs):
    if bar_figure_tabs == "stat_tab":
        rate = "statutory_tax_rate"
        ratetitle = "Statutory Corporate Tax Rates"
        ratelabel = "Statutory Rate"
        stat_marker = False
    if bar_figure_tabs == "metr_tab":
        rate = "metr_overall"
        ratetitle = "Marginal Effective Corporate Tax Rates (METRs)"
        ratelabel = "METR"
        stat_marker = True
    if bar_figure_tabs == "aetr_tab":
        rate = "aetr_overall"
        ratetitle = "Average Effective Corporate Tax Rates (AETRs)"
        ratelabel = "AETR"
        stat_marker = True

    bar_figure = make_bar_figure(rate, ratetitle, ratelabel, stat_marker)

    return bar_figure


@app.callback(
    Output("analysis_text", "children"),
    Input("bar_figure_tabs", "value"),
)
def update(bar_figure_tabs):
    if bar_figure_tabs == "stat_tab":
        text = """
        If the US federal corporate income tax rate is increased to 28 percent, as proposed in Biden’s proposal, the United States would have the highest combined statutory corporate tax rate in the OECD at 32.3 percent. The House Ways and Means proposal, which would raise the federal tax rate to 26.5, percent would increase the United States’ combined statutory corporate tax rate to 30.9 percent, which would be among the highest, but still below Portugal. 
        """
    if bar_figure_tabs == "metr_tab":
        text = """
        The proposals to raise the corporate tax burden in the United States would increase the tax burden on new corporate investment in the United States to one of the highest in the OECD. Under the Biden proposal, the METR would be 23.7 percent, which would be the highest in the OECD. The House Ways and Means proposal would increase the METR to 22.4 percent, which would only be lower than Japan (22.9 percent).
        """
    if bar_figure_tabs == "aetr_tab":
        text = """
        The Biden Administration proposal would raise the AETR to 29.5 percent. This would be the highest among all OECD nations and 6.7 percentage points above the OECD average. The House Ways and Means proposal would raise the US AETR to 28 percent. This would also result in the highest AETR among OECD nations.
        """
    return text


@app.callback(
    Output("country_figure", "figure"),
    Input("country_drop_rate", "value"),
    Input("country_drop_value1", "value"),
    Input("country_drop_value2", "value"),
)
def update(country_drop_rate, country_drop_value1, country_drop_value2):
    if country_drop_rate == "metr":
        country1 = country_drop_value1
        country2 = country_drop_value2
        measure = country_drop_rate
        measurename = "METR"
        measuretitle = "METRs"
    if country_drop_rate == "aetr":
        country1 = country_drop_value1
        country2 = country_drop_value2
        measure = country_drop_rate
        measurename = "AETR"
        measuretitle = "AETRs"
    country_figure = make_country_figure(
        country1, country2, measure, measurename, measuretitle
    )

    return country_figure


@app.callback(
    Output("financing_figure", "figure"),
    Input("financing_drop_rate", "value"),
)
def update(financing_drop_rate):
    if financing_drop_rate == "metr":
        rate = financing_drop_rate
        ratetitle = "METRs"
        ratelabel_bar = "Debt-Equity Bias"
        ratelabel_point = "METR"
    if financing_drop_rate == "aetr":
        rate = financing_drop_rate
        ratetitle = "AETRs"
        ratelabel_bar = "Debt-Equity Bias"
        ratelabel_point = "AETR"
    financing_figure = make_financing_figure(
        rate, ratetitle, ratelabel_bar, ratelabel_point
    )

    return financing_figure


@app.callback(
    Output("alternative_figure", "figure"),
    Input("alternative_radio_value", "value"),
    Input("alternative_figure_tabs", "value"),
)
def update(alternative_radio_value, alternative_figure_tabs):
    if alternative_figure_tabs == "metr_tab":
        rate = "metr_overall"
        ratetitle = "METRs"
        ratelabel = "METR"
        alternative = alternative_radio_value
        axisrange = [-0.20, 0.20]
    if alternative_figure_tabs == "aetr_tab":
        rate = "aetr_overall"
        ratetitle = "AETRs"
        ratelabel = "AETR"
        alternative = alternative_radio_value
        axisrange = [0.00, 0.31]

    alternative_figure = make_alternative_figure(
        rate, ratetitle, ratelabel, alternative, axisrange
    )

    return alternative_figure


@app.callback(
    Output("alternative_text", "children"),
    Input("alternative_radio_value", "value"),
    Input("alternative_figure_tabs", "value"),
)
def update(alternative_radio_value, alternative_figure_tabs):
    if alternative_figure_tabs == "metr_tab":
        if alternative_radio_value == "CL":
            text = """
            Under current law, the tax treatment of certain capital expenses, research and development, interest expense, and intellectual property are scheduled to change over the next few years. These changes contribute to the United States' relatively high effective tax rate on new investment.  
            """
        if alternative_radio_value == "BONUS":
            text = """
            Maintaining 100 percent bonus depreciation would have a large impact on the METR on new investment in the United States. 100 percent bonus depreciation would reduce the METR on investment by 5.3 percentage points under current law, 6.2 percentage points under the House Ways and Means proposal, and 6.5 percentage points under Biden’s proposal. 
            """
        if alternative_radio_value == "RND":
            text = """
            Maintaining expensing of research and development costs would reduce the METR on new investment in the United States. However, the impact would be slightly smaller than that of bonus depreciation (0.9 percentage points under current law, 1.1 under the House Ways and Means proposal, and 1.3 under Biden's proposal).
            """
        if alternative_radio_value == "EBITDA":
            text = """
            Canceling the switch from 30 percent of EBITDA to 30 percent of earnings before interest and taxes (EBIT) for the net interest deduction would reduce the METR on new investment by roughly the same extent as maintaining expensing for research and development costs.
            """
        if alternative_radio_value == "FDII":
            text = """
            Maintaining current policy FDII would have a negligible impact on the marginal tax rate on new investment. If research and development is already expensed, the METR on new investment is already zero. Reducing the rate has no impact on the incentive to invest in research and development. 
            """
    if alternative_figure_tabs == "aetr_tab":
        if alternative_radio_value == "CL":
            text = """
            Under current law, the tax treatment of certain capital expenses, research and development, interest expense, and intellectual property are scheduled to change over the next few years. These changes contribute to the United States' relatively high effective tax rate on new investment.  
            """
        if alternative_radio_value == "BONUS":
            text = """
            Maintaining 100 percent bonus depreciation would have a smaller impact on the AETR on new investment compared to its impact on the METR. 100 percent bonus depreciation would reduce the AETR on investment by 1.4 percentage points under current law and 1.7 percentage points under the House Ways and Means and Biden proposals. 
            """
        if alternative_radio_value == "RND":
            text = """
            Maintaining expensing of research and development costs would have a smaller impact on the AETR on new investment compared to its impact on the METR. The policy would reduce the AETR on investment by 0.2 percentage points under current law and 0.3 percentage points under the House Ways and Means and Biden proposals.
            """
        if alternative_radio_value == "EBITDA":
            text = """
            Canceling the switch from 30 percent of EBITDA to 30 percent of earnings before interest and taxes (EBIT) for the net interest deduction would have a smaller impact on the AETR on new investment compared to its impact on the METR. It would reduce the AETR on new investment by roughly the same extent as maintaining expensing for research and development costs.
            """
        if alternative_radio_value == "FDII":
            text = """
            Maintaining current policy FDII would reduce the AETR more than it would reduce the METR on new investment because the FDII deduction reduces the effective statutory tax rate on IP income. The policy would reduce the AETR on investment by 0.1 percentage points under current law and the House Ways and Means proposal and 0.3 percentage points under the Biden proposal.
            """
    return text


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(output[0:39].to_csv, "OECD-Effective-Tax-Rates.csv")


# Endcode
server = app.server
# Turn debug=False for production
if __name__ == "__main__":
    app.run_server(debug=False, use_reloader=True)
