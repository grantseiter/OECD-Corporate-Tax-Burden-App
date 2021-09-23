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

# revenue = pd.read_csv("data/treasury-estimates.csv")
parameters = pd.read_csv("data/parameters.csv")
output = pd.read_csv("data/output.csv")

# Code


def get_text_data():
    return


# def get_style_data_conditional(rowval):
#     style_data_conditional = [
#         {
#             "if": {"row_index": rowval},
#             "backgroundColor": "rgb(240, 240, 240)",
#         },
#     ]
#     return style_data_conditional


def make_bar_figure(rate, ratetitle, ratelabel, stat_marker):
    """
    Function creates bar charts with rate inputs for top section
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
            tickformat=".0%",
        ),
        plot_bgcolor="white",
    )

    bar_figure.update_layout(layout)

    return bar_figure


def make_asset_figure(country, measure, measuretitle):
    """
    Function creates scatter charts with rate inputs for by asset section
    """

    def make_data(country, measure, measuretitle):
        """
        filter data and calculate summary statistics
        """
        df = output[0:39]
        df2 = pd.DataFrame()
        oecd = pd.DataFrame()
        oecd["country"] = ["OECD"]
        oecd["name"] = ["OECD Average"]
        oecd[measure + "_land"] = [
            np.average(df[measure + "_land"], weights=df["weight"])
        ]
        oecd[measure + "_inventory"] = [
            np.average(df[measure + "_inventory"], weights=df["weight"])
        ]
        oecd[measure + "_ip"] = [np.average(df[measure + "_ip"], weights=df["weight"])]
        oecd[measure + "_buildings"] = [
            np.average(df[measure + "_buildings"], weights=df["weight"])
        ]
        oecd[measure + "_machines"] = [
            np.average(df[measure + "_machines"], weights=df["weight"])
        ]
        oecd = oecd.round(3)
        oecd = oecd.rename(
            columns={
                measure + "_machines": "Machines",
                measure + "_buildings": "Buildings",
                measure + "_ip": "Intellectual Property",
                measure + "_land": "Land",
                measure + "_inventory": "Inventory",
            }
        )
        if isinstance(country, str):
            df2 = df.loc[(df["country"] == "USA")]
            df2 = df2.append(df.loc[(df["country"] == "USA_H")])
            df2 = df2.append(df.loc[(df["country"] == "USA_B")])
            if country != "USA":
                df2 = df2.append(df.loc[(df["country"] == country)])
        else:
            df2 = df.loc[(df["country"] == "USA")]
            df2 = df2.append(df.loc[(df["country"] == "USA_H")])
            df2 = df2.append(df.loc[(df["country"] == "USA_B")])
            if "AUS" in country:
                df2 = df2.append(df.loc[(df["country"] == "AUS")])
            if "AUT" in country:
                df2 = df2.append(df.loc[(df["country"] == "AUT")])
            if "BEL" in country:
                df2 = df2.append(df.loc[(df["country"] == "BEL")])
            if "CAN" in country:
                df2 = df2.append(df.loc[(df["country"] == "CAN")])
            if "CHE" in country:
                df2 = df2.append(df.loc[(df["country"] == "CHE")])
            if "CHL" in country:
                df2 = df2.append(df.loc[(df["country"] == "CHL")])
            if "COL" in country:
                df2 = df2.append(df.loc[(df["country"] == "COL")])
            if "CZE" in country:
                df2 = df2.append(df.loc[(df["country"] == "CZE")])
            if "DEU" in country:
                df2 = df2.append(df.loc[(df["country"] == "DEU")])
            if "DNK" in country:
                df2 = df2.append(df.loc[(df["country"] == "DNK")])
            if "ESP" in country:
                df2 = df2.append(df.loc[(df["country"] == "ESP")])
            if "EST" in country:
                df2 = df2.append(df.loc[(df["country"] == "EST")])
            if "FIN" in country:
                df2 = df2.append(df.loc[(df["country"] == "FIN")])
            if "FRA" in country:
                df2 = df2.append(df.loc[(df["country"] == "FRA")])
            if "GBR" in country:
                df2 = df2.append(df.loc[(df["country"] == "GBR")])
            if "GRC" in country:
                df2 = df2.append(df.loc[(df["country"] == "GRC")])
            if "HUN" in country:
                df2 = df2.append(df.loc[(df["country"] == "HUN")])
            if "IRL" in country:
                df2 = df2.append(df.loc[(df["country"] == "IRL")])
            if "ISL" in country:
                df2 = df2.append(df.loc[(df["country"] == "ISL")])
            if "ISR" in country:
                df2 = df2.append(df.loc[(df["country"] == "ISR")])
            if "ITA" in country:
                df2 = df2.append(df.loc[(df["country"] == "ITA")])
            if "JPN" in country:
                df2 = df2.append(df.loc[(df["country"] == "JPN")])
            if "KOR" in country:
                df2 = df2.append(df.loc[(df["country"] == "KOR")])
            if "LTU" in country:
                df2 = df2.append(df.loc[(df["country"] == "LTU")])
            if "LUX" in country:
                df2 = df2.append(df.loc[(df["country"] == "LUX")])
            if "LVA" in country:
                df2 = df2.append(df.loc[(df["country"] == "LVA")])
            if "MEX" in country:
                df2 = df2.append(df.loc[(df["country"] == "MEX")])
            if "NLD" in country:
                df2 = df2.append(df.loc[(df["country"] == "NLD")])
            if "NOR" in country:
                df2 = df2.append(df.loc[(df["country"] == "NOR")])
            if "NZL" in country:
                df2 = df2.append(df.loc[(df["country"] == "NZL")])
            if "POL" in country:
                df2 = df2.append(df.loc[(df["country"] == "POL")])
            if "PRT" in country:
                df2 = df2.append(df.loc[(df["country"] == "PRT")])
            if "SVK" in country:
                df2 = df2.append(df.loc[(df["country"] == "SVK")])
            if "SVN" in country:
                df2 = df2.append(df.loc[(df["country"] == "SVN")])
            if "SWE" in country:
                df2 = df2.append(df.loc[(df["country"] == "SWE")])
            if "TUR" in country:
                df2 = df2.append(df.loc[(df["country"] == "TUR")])

        df2 = df2[
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
        df2 = df2.rename(
            columns={
                measure + "_machines": "Machines",
                measure + "_buildings": "Buildings",
                measure + "_ip": "Intellectual Property",
                measure + "_land": "Land",
                measure + "_inventory": "Inventory",
            }
        )
        data = pd.concat([df2, oecd])
        data = pd.melt(data, id_vars=["country", "name"])
        return data

    data = make_data(country, measure, measuretitle).reset_index(drop=True)

    def make_figure(country, measure, measuretitle):
        """
        creates the Plotly traces
        """
        usloc0 = int(data[data["name"] == "United States (Current Law)"].index[0])
        usloc1 = int(data[data["name"] == "United States (Current Law)"].index[1])
        usloc2 = int(data[data["name"] == "United States (Current Law)"].index[2])
        usloc3 = int(data[data["name"] == "United States (Current Law)"].index[3])
        usloc4 = int(data[data["name"] == "United States (Current Law)"].index[4])
        ushloc0 = int(data[data["name"] == "United States (House)"].index[0])
        ushloc1 = int(data[data["name"] == "United States (House)"].index[1])
        ushloc2 = int(data[data["name"] == "United States (House)"].index[2])
        ushloc3 = int(data[data["name"] == "United States (House)"].index[3])
        ushloc4 = int(data[data["name"] == "United States (House)"].index[4])
        usbloc0 = int(data[data["name"] == "United States (Biden)"].index[0])
        usbloc1 = int(data[data["name"] == "United States (Biden)"].index[1])
        usbloc2 = int(data[data["name"] == "United States (Biden)"].index[2])
        usbloc3 = int(data[data["name"] == "United States (Biden)"].index[3])
        usbloc4 = int(data[data["name"] == "United States (Biden)"].index[4])
        oecdloc0 = int(data[data["name"] == "OECD Average"].index[0])
        oecdloc1 = int(data[data["name"] == "OECD Average"].index[1])
        oecdloc2 = int(data[data["name"] == "OECD Average"].index[2])
        oecdloc3 = int(data[data["name"] == "OECD Average"].index[3])
        oecdloc4 = int(data[data["name"] == "OECD Average"].index[4])

        colors = ["#008CCC"] * 100
        colors[usloc0] = "#00D56F"
        colors[usloc1] = "#00D56F"
        colors[usloc2] = "#00D56F"
        colors[usloc3] = "#00D56F"
        colors[usloc4] = "#00D56F"
        colors[ushloc0] = "#FFB400"
        colors[ushloc1] = "#FFB400"
        colors[ushloc2] = "#FFB400"
        colors[ushloc3] = "#FFB400"
        colors[ushloc4] = "#FFB400"
        colors[usbloc0] = "#FF8100"
        colors[usbloc1] = "#FF8100"
        colors[usbloc2] = "#FF8100"
        colors[usbloc3] = "#FF8100"
        colors[usbloc4] = "#FF8100"
        colors[oecdloc0] = "#FB0023"
        colors[oecdloc1] = "#FB0023"
        colors[oecdloc2] = "#FB0023"
        colors[oecdloc3] = "#FB0023"
        colors[oecdloc4] = "#FB0023"

        oecd_trace = go.Scatter(
            x=data["value"],
            y=data["variable"],
            marker=dict(size=18, color=colors),
            mode="markers",
            marker_symbol="line-ns",
            marker_line_width=4,
            marker_line_color=colors,
            hovertemplate=data["name"]
            + "<br>"
            + data["variable"]
            + "<br><b>%{x:.1%}<extra></extra><br>",
            showlegend=False,
        )
        legend_OECD = go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(size=10, color="#FB0023"),
            legendgroup="legend",
            showlegend=True,
            name="OECD Average",
        )
        legend_USA = go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(size=10, color="#00D56F"),
            legendgroup="legend",
            showlegend=True,
            name="US (Current Law)",
        )
        legend_USA_H = go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(size=10, color="#FFB400"),
            legendgroup="legend",
            showlegend=True,
            name="US (House)",
        )
        legend_USA_B = go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(size=10, color="#FF8100"),
            legendgroup="legend",
            showlegend=True,
            name="US (Biden)",
        )
        layout = go.Layout(
            title=measuretitle
            + " by Asset, Selected Countries and OECD Average, Current Law and Proposals"
            + "<br><sup><i>Hover over data to view more information.</i></sup>",
            xaxis=dict(
                tickformat=".0%",
                gridcolor="#F2F2F2",
                zeroline=False,
            ),
            yaxis=dict(gridcolor="#8E919A", linecolor="#F2F2F2", type="category"),
            paper_bgcolor="#F2F2F2",
            plot_bgcolor="#F2F2F2",
        )
        asset_figure = go.Figure(
            data=[oecd_trace, legend_OECD, legend_USA, legend_USA_H, legend_USA_B],
            layout=layout,
        )
        return asset_figure

    asset_figure = make_figure(country, measure, measuretitle)
    return asset_figure


def make_financing_figure(rate, ratetitle, ratelabel_bar, ratelabel_point):
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
            gridcolor="#BABBC0",
            tickformat=".0%",
            zerolinecolor="#BABBC0",
        ),
        paper_bgcolor="#F2F2F2",
        plot_bgcolor="#F2F2F2",
        height=600,
    )
    financing_figure = go.Figure(
        data=[fig_equity, fig_debt, fig_bar, fig_oecd], layout=layout
    )
    return financing_figure


def make_country_figure(country, measure, measurename, measuretitle, charttitle):
    """
    function to make Plotly figure
    will be called in app callback
    """
    df = output[0:39]
    data = (df.loc[(df["country"] == country)]).reset_index(drop=True)

    data_assets = data[
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
    data_finance = data[
        [
            "country",
            "name",
            measure + "_overall",
            measure + "_equity_overall",
            measure + "_debt_overall",
        ]
    ]
    data_assets = data_assets.rename(
        columns={
            measure + "_machines": "Machines",
            measure + "_buildings": "Buildings",
            measure + "_ip": "Intellectual Property",
            measure + "_land": "Land",
            measure + "_inventory": "Inventory",
        }
    )

    data_assets = pd.melt(data_assets, id_vars=["country", "name"])

    def make_fig(country, measure, measurename, measuretitle, charttitle):
        """
        creates the Plotly traces
        """
        assets_trace = go.Scatter(
            x=data_assets["value"],
            y=data_assets["variable"],
            marker=dict(
                size=20,
                color="#008CCC",
            ),
            mode="markers",
            name=measurename,
            marker_symbol="circle",
            showlegend=False,
        )

        overall_trace = go.Scatter(
            x=[
                data_finance[measure + "_overall"][0],
                data_finance[measure + "_overall"][0],
                data_finance[measure + "_overall"][0],
                data_finance[measure + "_overall"][0],
                data_finance[measure + "_overall"][0],
            ],
            y=["Land", "Inventory", "Intellectual Property", "Buildings", "Machines"],
            mode="lines",
            line=dict(
                color="#FB0023",
                dash="dash",
            ),
            name=measurename + " Overall",
            hovertemplate=str(round(data_finance[measure + "_overall"][0], 2) * 100)
            + "%",
            showlegend=True,
        )

        equity_trace = go.Scatter(
            x=[
                data_finance[measure + "_equity_overall"][0],
                data_finance[measure + "_equity_overall"][0],
                data_finance[measure + "_equity_overall"][0],
                data_finance[measure + "_equity_overall"][0],
                data_finance[measure + "_equity_overall"][0],
            ],
            y=["Land", "Inventory", "Intellectual Property", "Buildings", "Machines"],
            mode="lines",
            line=dict(
                color="#00D56F",
                dash="dash",
            ),
            name=measurename + " on Equity<br>Financed Investment",
            hovertemplate=str(
                round(data_finance[measure + "_equity_overall"][0], 2) * 100
            )
            + "%",
            showlegend=True,
        )

        debt_trace = go.Scatter(
            x=[
                data_finance[measure + "_debt_overall"][0],
                data_finance[measure + "_debt_overall"][0],
                data_finance[measure + "_debt_overall"][0],
                data_finance[measure + "_debt_overall"][0],
                data_finance[measure + "_debt_overall"][0],
            ],
            y=["Land", "Inventory", "Intellectual Property", "Buildings", "Machines"],
            mode="lines",
            line=dict(
                color="#8300EE",
                dash="dash",
            ),
            name=measurename + " on Debt<br>Financed Investment",
            hovertemplate=str(
                round(data_finance[measure + "_debt_overall"][0], 2) * 100
            )
            + "%",
            showlegend=True,
        )

        layout = go.Layout(
            title=charttitle
            + " "
            + "<i>"
            + data_finance["name"][0]
            + ",</i>"
            + " "
            + measuretitle
            + " by Asset and Form of Financing, "
            + "<br><sup><i>Hover over data to view more information. Toggle legend items to show or hide elements.</i></sup>",
            xaxis=dict(
                tickformat=".0%",
                gridcolor="#F2F2F2",
                zeroline=False,
                range=[-0.40, 0.40],
            ),
            yaxis=dict(gridcolor="#8E919A", linecolor="#F2F2F2", type="category"),
            paper_bgcolor="#F2F2F2",
            plot_bgcolor="#F2F2F2",
            height=300,
        )

        fig = go.Figure(
            data=[assets_trace, overall_trace, equity_trace, debt_trace], layout=layout
        )
        return fig

    country_figure = make_fig(country, measure, measurename, measuretitle, charttitle)

    return country_figure


# Initialize App

app = dash.Dash(__name__)

# Create App Layout
app.layout = html.Div(
    [
        # HEADER
        html.Div(
            [
                html.H6(
                    "BETA VERSION 0.1.2 –– PEASE DO NOT CITE WITHOUT PERMISSON DATA IS NOT FINAL –– RELEASE v2-2021-09-23",
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
            ## The Tax Burden on Multinational Corporations and Proposals to Reform the US Tax System
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
                    "Corporate tax systems are complex and vary significantly among developed nations. Not only are there differences in corporate income tax rates, but there is significant variation in corporate tax bases. This dashboard compares the tax burden on corporations in the United States under current law to the corporate tax burdens of 36 member nations of the Organisation for Economic Co-operation and Development (OECD). It also considers two leading proposals to reform US corporate income taxation and several alternative changes to policy.",
                    style={"text-align": "justify"},
                ),
            ],
            className="twelve columns",
        ),
        # BIDEN PROPOSALS SECTION
        html.Div(
            [
                html.H6(
                    "Current Proposals to Reform US Corporate Taxation",
                    style={"text-align": "justify", "font-weight": "bold"},
                ),
                # html.Label(
                #     "Select a proposal, below, to view more details.",
                #     style={"font-style": "italic", "font-size": "90%"},
                # ),
                # dcc.Dropdown(
                #     id="variable_selection",
                #     options=[
                #         {"label": "All Proposals", "value": "ALL"},
                #         {
                #             "label": "Raise the Corporate Income Tax from 21 to 28 Percent",
                #             "value": "CTR",
                #         },
                #         {
                #             "label": "Reform GILTI, Limit Inversions, and Disallow Deductions Attributable to Exempt Income",
                #             "value": "GILTI",
                #         },
                #         {
                #             "label": "Repeal FDII and Replace with R&D Incentive",
                #             "value": "FDII",
                #         },
                #         {"label": "Replace BEAT with SHIELD", "value": "SHIELD"},
                #         {
                #             "label": "Restrict Excess Interest Deductions",
                #             "value": "EID",
                #         },
                #         {"label": "Impose a 15 Percent Book Tax", "value": "BOOK"},
                #     ],
                #     value="ALL",
                #     clearable=False,
                #     searchable=False,
                #     className=" input_container twelve columns",
                # ),
                # html.Div(
                #     [
                #         dash_table.DataTable(
                #             id="revenue_table",
                #             columns=[{"name": i, "id": i} for i in revenue.columns],
                #             data=revenue.to_dict("records"),
                #             style_cell={"textAlign": "center"},
                #             style_header={
                #                 "backgroundColor": "white",
                #                 "fontWeight": "bold",
                #             },
                #             style_cell_conditional=[
                #                 {
                #                     "if": {
                #                         "column_id": "Revenue Impact (Billions of Dollars)"
                #                     },
                #                     "textAlign": "left",
                #                 },
                #             ],
                #         ),
                #     ],
                #     className="description_container seven columns",
                # ),
                # dcc.Markdown(
                #     id="prop_text",
                #     className="four columns",
                #     style={"text-align": "justify", "margin-bottom": "10px"},
                #     dangerously_allow_html=True,
                # ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
                            **Major Tax Parameters Modeled for the United States**
                            """,
                            className="seven columns",
                            style={"text-align": "justify", "margin-top": "-28px"},
                            dangerously_allow_html=True,
                        ),
                        dash_table.DataTable(
                            id="parameters_table",
                            columns=[{"name": i, "id": i} for i in parameters.columns],
                            data=parameters.to_dict("records"),
                            style_data={
                                "whiteSpace": "normal",
                                "height": "auto",
                            },
                            style_cell={"textAlign": "center"},
                            style_header={
                                "backgroundColor": "white",
                                "fontWeight": "bold",
                            },
                        ),
                    ],
                    className="description_container seven columns",
                ),
                dcc.Markdown(
                    """
                    **Summary of Leading Proposals Modeled**
                    
                    In this analysis, two proposals are modeled for the United States in addition to current law. The Biden Administration's proposal would raise the federal corporate income tax rate to 28 percent and eliminate the foreign-derived intangible income (FDII) deduction. The House Ways and Means proposal would raise the federal corporate income tax rate to 26.5 percent and keep FDII in place. The major tax parameters modeled, compared to current law, are shown in the adjacent table.

                    For more details on additional corporate tax reforms put forth by the Biden Administration and lawmakers in congress, see <a href="https://www.aei.org/research-products/report/bidens-reforms-to-the-tax-treatment-of-us-multinational-corporations-the-knowns-and-unknowns/" children="Biden’s Reforms to the Tax Treatment of US Multinational Corporations: The Knowns and Unknowns" style="color:#008CCC;font-style:italic" target="blank" /> (Pomerleau, 2021). 
                    """,
                    className="four columns",
                    style={"text-align": "justify", "margin-bottom": "10px"},
                    dangerously_allow_html=True,
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
                There is no single measure of the corporate tax burden that captures every aspect of a corporate income tax. This analysis focuses on three measures: the combined statutory corporate income tax rate, the marginal effective corporate tax rate (METR), and the average effective corporate tax rate (AETR). Each measure represents a different component of a corporation’s tax burden and can be used to evaluate how a corporate income tax may distort behavior.
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
                 **Statutory Corporate Tax Rates** measure the tax burden on profits, or the rate at which each dollar of corporate taxable income is taxed. The larger the statutory rate gap between two jurisdictions, the larger the returns to profit shifting are for multinational corporations.

                 **Marginal Effective Corporate Tax Rates (METRs)** measure the tax burden on marginal investment, or an investment that breaks even in present value. This rate can affect the decision to increase or decrease the level of an investment.
                 
                 **Average Effective Corporate Tax Rates (AETRs)** measure the tax burden on discrete investment, or an investment that is expected to earn above-normal returns or economic rents. This rate can affect the choice between two or more mutually exclusive investments, or in the case of multinational corporations, the decision to locate investment in different jurisdictions.  
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
                # ASSET/FINANCING BIAS SUBSECTION
                html.Div(
                    [
                        dcc.Markdown(
                            """
                    ** Effective Tax Rates by Asset Type **

                    Effective tax rates in the OECD vary significantly by type of asset. The weighted average METR on assets ranges from -3.7 percent on intellectual property products to 22.2 percent on inventories. Machinery, on average, faces a marginal effective tax rate of 16.5 percent. Buildings face a slightly lower average marginal effective tax rate of 15.8 percent. Land faces an average METR of 15.7 percent. Proposals in the United States to increase the corporate tax burden would raise the METR on all assets in the United States. Under either the House or Biden proposal, AETRs on all assets would be the highest or close to the highest in the OECD.
                    """,
                            className="twelve columns",
                            style={"text-align": "justify"},
                            dangerously_allow_html=True,
                        ),
                        html.Label(
                            "Select a different effective tax rate to display in the figure, below.",
                            style={"font-style": "italic", "font-size": "90%"},
                            className="twelve columns",
                        ),
                        dcc.Dropdown(
                            id="asset_drop_rate",
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
                                "margin-bottom": "20px",
                                "margin-bottom": "5px",
                            },
                        ),
                        html.Label(
                            "Select one or more countries to add to the figure, below.",
                            style={"font-style": "italic", "font-size": "90%"},
                            className="twelve columns",
                        ),
                        dcc.Dropdown(
                            id="asset_drop_country",
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
                            ],
                            multi=True,
                            clearable=False,
                            searchable=True,
                            value="USA",
                            placeholder="Click to Search and Select...",
                            className="twelve columns",
                            style={
                                "justify-content": "center",
                            },
                        ),
                        html.Div(
                            [dcc.Graph(id="asset_figure")],
                            className="twelve columns",
                            style={"margin-bottom": "20px"},
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
                        html.Hr(),
                        dcc.Markdown(
                            """
                    ** Effective Tax Rates by Source of Financing  **

                    Corporations can finance new projects through equity by using either retained earnings or issuing new shares, or with debt by issuing bonds. Equity payments made to shareholders (dividends) are not deductible against taxable income, while interest on debt is deductible against taxable income. Debt-financed investment is, therefore, typically tax-preferred. In the OECD, debt-financed investment, on average, faces a METR 32.1 percentage points lower than the METR on equity-financed investment. However, the extent to which debt-financed investment is tax-preferred varies across the OECD. The Biden and House proposals would increase the bias in favor of debt-financed investment in the United States. Under either proposal, the bias in favor of debt would be slightly above the OECD average. 
                    """,
                            className="twelve columns",
                            style={"text-align": "justify"},
                            dangerously_allow_html=True,
                        ),
                        html.Label(
                            "Select a different effective tax rate to display in the figure, below.",
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
                                "margin-bottom": "20px",
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
                        html.Hr(),
                        dcc.Markdown(
                            """
                    ** Country by Country Comparison  **

                    Lorem ipsum text
                    """,
                            className="twelve columns",
                            style={"text-align": "justify"},
                            dangerously_allow_html=True,
                        ),
                        html.Label(
                            "Select a different effective tax rate to display in the comparison figures, below.",
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
                            "Select a country for the first figure, below.",
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
                                {"label": "Poland", "value": "POL"},
                                {"label": "Portugal", "value": "PRT"},
                                {"label": "Slovak Republic", "value": "SVK"},
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
                            className="twelve columns",
                            style={
                                "justify-content": "center",
                            },
                        ),
                        html.Label(
                            "Select a country for the second figure, below.",
                            style={"font-style": "italic", "font-size": "90%"},
                            className="twelve columns",
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
                                {"label": "Poland", "value": "POL"},
                                {"label": "Portugal", "value": "PRT"},
                                {"label": "Slovak Republic", "value": "SVK"},
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
                            value="GBR",
                            className="twelve columns",
                            style={
                                "justify-content": "center",
                            },
                        ),
                        html.Div(
                            [dcc.Graph(id="country_figure1")],
                            className="twelve columns",
                            style={
                                "justify-content": "center",
                            },
                        ),
                        html.Div(
                            [dcc.Graph(id="country_figure2")],
                            className="twelve columns",
                            style={
                                "justify-content": "center",
                                "margin-bottom": "20px",
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
            ],
            className="description_container twelve columns",
        ),
        # ALTERNATIVE POLICIES SECTION
        html.Div(
            [
                html.H6(
                    "Impact of Alternative Policies on Effective Tax Rates in the United States",
                    style={
                        "margin-top": "-20px",
                        "font-weight": "bold",
                        "text-align": "justify",
                    },
                ),
                dcc.Markdown(
                    """
                    The effective tax rate estimates for the United States, above, reflect current law and exclude temporary policies scheduled to change over the next decade. As such, the estimates include amortization of research and development costs and tighter limitations on net interest expenses, which are scheduled to change in 2022, and exclude 100 percent bonus depreciation, which is scheduled to phase out over five years starting in 2023. Likewise, the deduction for FDII is set to 21.875 percent, which is it’s scheduled value in 2026. The interactive figure, below, allows users to consider the impact of these alternative policies on effective tax rates in the United States.
                    """,
                    className="twelve columns",
                    style={"text-align": "justify"},
                    dangerously_allow_html=True,
                ),
                html.Label(
                    "Select one or more policies to update US effective tax rates in the figure below.",
                    style={"font-style": "italic", "font-size": "90%"},
                    className="twelve columns",
                ),
                dcc.Checklist(
                    id="policy_checklist",
                    options=[
                        {"label": "Maintain 100% Bonus Depreciation", "value": "BONUS"},
                        {"label": "Maintain R&D Expensing", "value": "RND"},
                        {"label": "Maintain 30% EBITDA Limitation", "value": "EBITDA"},
                        {"label": "Maintain FDII", "value": "FDII"},
                    ],
                    value=[],
                    labelStyle={"display": "inline-block", "margin-right": "5%"},
                    className="twelve columns",
                    style={
                        "justify-content": "center",
                    },
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
                This dashboard is an extension of research presented in *The Tax Burden on Corporations: A Comparison of OECD Countries and Proposals to Reform the US Tax System* (Pomerleau, forthcoming). The code that powers this data visualization can be found
                <a href="https://github.com/grantseiter/" children="here" style="color:#008CCC" target="blank" />.
                Feedback or questions? Contact us <a href="mailto:Grant.Seiter@AEI.org" children="here" style="color:#008CCC" />.
                """,
                    dangerously_allow_html=True,
                )
            ],
            className="footer twelve columns",
        ),
        html.Div(
            [
                dcc.Markdown(
                    """
                    **Modeling Notes**: Effective tax rates on corporate investment were estimated using a framework developed by Devereux and Griffith (1999) and by generally following the method outlined in Spengel et. Al. (2019). These rates are forward-looking and measure the tax burden that a corporation expects to pay on a new domestic investment in each jurisdiction. The parameters used to estimate effective tax rates reflect current law in each country. Several countries have changes in their corporate tax systems that are scheduled to occur. In these cases, the parameters are set to where they will be in the long run. As such, this analysis ignores several temporary changes made to corporate taxes in response to the COVID-19 pandemic. The full methodology is detailed in *The Tax Burden on Corporations: A Comparison of OECD Countries and Proposals to Reform the US Tax System* (Pomerleau, forthcoming).
                    """,
                    className="twelve columns",
                    style={
                        "text-align": "justify",
                        "margin-bottom": "20px",
                        "font-size": "90%",
                    },
                    dangerously_allow_html=True,
                ),
            ],
            className="footer twelve columns",
        ),
    ]
)


# @app.callback(
#     Output("prop_text", "children"),
#     Input("variable_selection", "value"),
# )
# def update(variable_selection):
#     if variable_selection == "ALL":
#         text = """
#         **Summary of All Major Proposals**

#         Under the administration’s proposals, US-headquartered corporations would face worldwide taxation on all their profits. Profits earned in the United States would face a tax rate of 28 percent, and all foreign profits would face a minimum tax rate of 21 percent under a reformed version of GILTI (global intangible low-taxed income). In addition, the administration would introduce new anti–base erosion provisions (SHIELD: Stopping Harmful Inversions and Ending Low-Tax Developments) and a new minimum tax on book profits. It is also pursuing a multilateral agreement aimed at reforming the tax treatment of multinational corporations throughout the world.
#         """
#     if variable_selection == "CTR":
#         text = """
#         **Raise the Corporate Income Tax to 28 Percent**

#         Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi id congue enim. Morbi eget felis a leo ultricies semper. Donec et libero pellentesque, pharetra neque id, ultricies sem. Etiam pulvinar tristique viverra. Etiam at neque consequat, pharetra purus et, malesuada quam. Mauris et ex ultrices, tristique diam eu, molestie justo. Vivamus dapibus elit rhoncus nisl convallis tempus. Quisque aliquet metus quis lectus euismod, at commodo nulla volutpat. Phasellus et nisi id odio sodales condimentum. Vestibulum facilisis sagittis ultricies. Maecenas sit amet metus at mauris varius porttitor non ut ante.
#         """
#     if variable_selection == "GILTI":
#         text = """
#         **Reform GILTI, Limit Inversions, and Disallow Deductions Attributable to Exempt Income**

#         Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi id congue enim. Morbi eget felis a leo ultricies semper. Donec et libero pellentesque, pharetra neque id, ultricies sem. Etiam pulvinar tristique viverra. Etiam at neque consequat, pharetra purus et, malesuada quam. Mauris et ex ultrices, tristique diam eu, molestie justo. Vivamus dapibus elit rhoncus nisl convallis tempus. Quisque aliquet metus quis lectus euismod, at commodo nulla volutpat. Phasellus et nisi id odio sodales condimentum. Vestibulum facilisis sagittis ultricies. Maecenas sit amet metus at mauris varius porttitor non ut ante.
#         """
#     if variable_selection == "FDII":
#         text = """
#         **Repeal FDII and Replace with R&D Incentive**

#         Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi id congue enim. Morbi eget felis a leo ultricies semper. Donec et libero pellentesque, pharetra neque id, ultricies sem. Etiam pulvinar tristique viverra. Etiam at neque consequat, pharetra purus et, malesuada quam. Mauris et ex ultrices, tristique diam eu, molestie justo. Vivamus dapibus elit rhoncus nisl convallis tempus. Quisque aliquet metus quis lectus euismod, at commodo nulla volutpat. Phasellus et nisi id odio sodales condimentum. Vestibulum facilisis sagittis ultricies. Maecenas sit amet metus at mauris varius porttitor non ut ante.
#         """
#     if variable_selection == "SHIELD":
#         text = """
#         **Replace BEAT with SHIELD**

#         Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi id congue enim. Morbi eget felis a leo ultricies semper. Donec et libero pellentesque, pharetra neque id, ultricies sem. Etiam pulvinar tristique viverra. Etiam at neque consequat, pharetra purus et, malesuada quam. Mauris et ex ultrices, tristique diam eu, molestie justo. Vivamus dapibus elit rhoncus nisl convallis tempus. Quisque aliquet metus quis lectus euismod, at commodo nulla volutpat. Phasellus et nisi id odio sodales condimentum. Vestibulum facilisis sagittis ultricies. Maecenas sit amet metus at mauris varius porttitor non ut ante.
#         """
#     if variable_selection == "EID":
#         text = """
#         **Restrict Excess Interest Deductions**

#         Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi id congue enim. Morbi eget felis a leo ultricies semper. Donec et libero pellentesque, pharetra neque id, ultricies sem. Etiam pulvinar tristique viverra. Etiam at neque consequat, pharetra purus et, malesuada quam. Mauris et ex ultrices, tristique diam eu, molestie justo. Vivamus dapibus elit rhoncus nisl convallis tempus. Quisque aliquet metus quis lectus euismod, at commodo nulla volutpat. Phasellus et nisi id odio sodales condimentum. Vestibulum facilisis sagittis ultricies. Maecenas sit amet metus at mauris varius porttitor non ut ante.
#         """
#     if variable_selection == "BOOK":
#         text = """
#         **Impose a 15 Percent Book Tax**

#         Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi id congue enim. Morbi eget felis a leo ultricies semper. Donec et libero pellentesque, pharetra neque id, ultricies sem. Etiam pulvinar tristique viverra. Etiam at neque consequat, pharetra purus et, malesuada quam. Mauris et ex ultrices, tristique diam eu, molestie justo. Vivamus dapibus elit rhoncus nisl convallis tempus. Quisque aliquet metus quis lectus euismod, at commodo nulla volutpat. Phasellus et nisi id odio sodales condimentum. Vestibulum facilisis sagittis ultricies. Maecenas sit amet metus at mauris varius porttitor non ut ante.
#         """
#     return text


# @app.callback(
#     Output("revenue_table", "style_data_conditional"),
#     Input("variable_selection", "value"),
# )
# def update(variable_selection):
#     if variable_selection == "ALL":
#         rowval = None
#     if variable_selection == "CTR":
#         rowval = 0
#     if variable_selection == "GILTI":
#         rowval = 1
#     if variable_selection == "FDII":
#         rowval = 2
#     if variable_selection == "SHIELD":
#         rowval = 3
#     if variable_selection == "EID":
#         rowval = 4
#     if variable_selection == "BOOK":
#         rowval = 5
#     return get_style_data_conditional(rowval)


@app.callback(
    Output("bar_figure", "figure"),
    Input("bar_figure_tabs", "value"),
)
def update(bar_figure_tabs):
    if bar_figure_tabs == "stat_tab":
        rate = "statutory_tax_rate"
        ratetitle = "Statutory Corporate Tax Rates"
        ratelabel = "Corporate Rate"
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
        **Analysis**

        If the US federal corporate income tax rate is increased to 28 percent, as proposed in Biden’s proposal, the United States would have the highest combined statutory corporate tax rate in the OECD at 32.3 percent. The House proposal, which would raise the federal tax rate to 26.5 percent would increase the United States’ combined statutory corporate tax rate to 30.9 percent, which would be among the highest, but still below Portugal. 
        """
    if bar_figure_tabs == "metr_tab":
        text = """
        **Analysis**

        The proposals to raise the corporate tax burden in the United States would increase the tax burden on new corporate investment in the United States to one of the highest in the OECD. Under the Biden proposal, the METR would be 23.7 percent, which would be the highest in the OECD. The House proposal would increase the METR to 22.4 percent, which would only be lower than Japan (22.9 percent).
        """
    if bar_figure_tabs == "aetr_tab":
        text = """
        **Analysis**

        The Biden Administration proposal would raise the AETR to 29.5 percent. This would be the highest among all OECD nations and 6.4 percentage points above the OECD average. The House proposal would raise the US AETR to 28 percent. This would also result in the highest AETR among OECD nations.
        """
    return text


@app.callback(
    Output("asset_figure", "figure"),
    Input("asset_drop_country", "value"),
    Input("asset_drop_rate", "value"),
)
def update(asset_drop_country, asset_drop_rate):
    country = asset_drop_country
    measure = asset_drop_rate
    if asset_drop_rate == "metr":
        measuretitle = "Marginal Effective Tax Rates"
    if asset_drop_rate == "aetr":
        measuretitle = "Average Effective Tax Rates"
    asset_figure = make_asset_figure(country, measure, measuretitle)

    return asset_figure


@app.callback(
    Output("financing_figure", "figure"),
    Input("financing_drop_rate", "value"),
)
def update(financing_drop_rate):
    if financing_drop_rate == "metr":
        rate = financing_drop_rate
        ratetitle = "Marginal Effective Tax Rates (METRs)"
        ratelabel_bar = "Debt-Equity Bias"
        ratelabel_point = "METR"
    if financing_drop_rate == "aetr":
        rate = financing_drop_rate
        ratetitle = "Average Effective Tax Rates (AETRs)"
        ratelabel_bar = "Debt-Equity Bias"
        ratelabel_point = "AETR"
    financing_figure = make_financing_figure(
        rate, ratetitle, ratelabel_bar, ratelabel_point
    )

    return financing_figure


@app.callback(
    Output("country_figure1", "figure"),
    Input("country_drop_rate", "value"),
    Input("country_drop_value1", "value"),
)
def update(country_drop_rate, country_drop_value1):
    if country_drop_rate == "metr":
        country = country_drop_value1
        measure = country_drop_rate
        measurename = "METR"
        measuretitle = "Marginal Effective Tax Rates (METRs)"
        charttitle = "<i>Country One:</i>"
    if country_drop_rate == "aetr":
        country = country_drop_value1
        measure = country_drop_rate
        measurename = "AETR"
        measuretitle = "Average Effective Tax Rates (AETRs)"
        charttitle = "<i>Country One:</i>"
    country_figure1 = make_country_figure(
        country, measure, measurename, measuretitle, charttitle
    )

    return country_figure1


@app.callback(
    Output("country_figure2", "figure"),
    Input("country_drop_rate", "value"),
    Input("country_drop_value2", "value"),
)
def update(country_drop_rate, country_drop_value2):
    if country_drop_rate == "metr":
        country = country_drop_value2
        measure = country_drop_rate
        measurename = "METR"
        measuretitle = "Marginal Effective Tax Rates (METRs)"
        charttitle = "<i>Country Two:</i>"
    if country_drop_rate == "aetr":
        country = country_drop_value2
        measure = country_drop_rate
        measurename = "AETR"
        measuretitle = "Average Effective Tax Rates (METRs)"
        charttitle = "<i>Country Two:</i>"
    country_figure2 = make_country_figure(
        country, measure, measurename, measuretitle, charttitle
    )

    return country_figure2


server = app.server
# turn debug=False for production
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)
