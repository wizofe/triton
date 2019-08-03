import base64
import pathlib
import json
import cProfile
import logging

from ichorlib.msClasses.MassSpectrum import MassSpectrum
from ichorlib.genClasses.PeakPicking import PeakPicking
from ichorlib.msClasses.MsCSD import MsCSD
from ichorlib.genClasses.colorPalette import tableau20

# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplotN
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go


# From SO: https://stackoverflow.com/a/29172195/8088718
# Avoid the tk gui bug
# import matplotlib
# matplotlib.use("Agg")
import matplotlib.pyplot as plt, mpld3

# Set logging level
logging.basicConfig(filename="tritonDebug.log", level=logging.DEBUG)
mpl_log = logging.getLogger("matplotlib")
mpl_log.setLevel(logging.WARNING)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

# grain_param = 10
# poly_order_param = 5
# smoothes_param = 2
# window_len_param = 1000
# simul_peak_fwhh = 75

# Set the relative data path
MYPATH = pathlib.Path(__file__).parent
DATA_PATH = MYPATH.joinpath("data").resolve()


def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.dump_stats("stupidlySlow.prof")

    return profiled_func


def plot_atd(my_data_file, my_grain, my_poly_order, my_smoothes, my_window_len):
    """ Plot the Arrival Time Distribution (ATD)

    Args:
    my_data_file (path): The experimental data file named my_data_file (tab delim. CSV)

    Returns:
    It shows a plot. TODO: Return a matplotlib/plotly/JSON object
    """
    # Plot the ATD
    ms = MassSpectrum()
    ms.read_text_file(my_data_file, 0, my_grain, normalisationtype="bpi")
    ms.smoothingSG(my_window_len, my_smoothes, my_poly_order)
    ms.normalisation_bpi()
    # ms.select_ms_range(4200,9000)

    # fig = plt.figure(figsize=(12, 8)
    # ax = plt.subplot(311)
    fig, ax = plt.subplots()
    ms.plot_simulated_spectrum_simple(ax, color=tableau20[2])
    logging.debug(ms.__dict__)
    return fig, ms


@do_cprofile
def plot_pp_csd(my_simul_peak, msobj):
    pp = PeakPicking()
    pp.calculate_gradient(msobj.xvals, msobj.yvals)
    found_peaks = pp.find_peaks(1)

    # fig = plt.figure(figsize=(12, 8))
    # ax2 = plt.subplot(312)
    fig, ax2 = plt.subplots()
    msobj.plot_simulated_spectrum_simple(ax2, color=tableau20[6])
    for peak in found_peaks:
        peak.plotSimulatedPeak(ax2, msobj.xvals, fwhm=my_simul_peak, color=tableau20[5])

    # plt.show()
    return fig

    # fig = plt.figure() # figsize=(12, 8))
    # ax4 = plt.subplot(312)
    # ax3 = plt.subplot(313)
    # ms.plot_simulated_spectrum_simple(ax4, color=tableau20[0])
    # for peak in found_peaks:
    #     peak.plotSimulatedPeak(ax4, ms.xvals, fwhm=simul_peak_fwhh, color=tableau20[2])

    # peaks_for_csds = [[32, 36, 42, 48, 54], [38, 45, 50], [28, 33, 41]]
    # #    peaks_for_csds = [[12, 36, 42, 48, 54], [38, 45, 50], [28, 33, 41]]

    # ms.csds = []
    # for count, peak_set in enumerate(peaks_for_csds):
    #     CSD1 = MsCSD()
    #     CSD1.name = "CSD" + str(count)
    #     CSD1.p_fwhh = simul_peak_fwhh
    #     CSD1_peak_indexes = peak_set
    #     indexed_peaks = pp.get_peaks_using_indexes(CSD1_peak_indexes)
    #     CSD1.mspeaks = indexed_peaks
    #     CSD1.calculateMassAndCharges(CSD1.mspeaks)
    #     CSD1.optimiseParameters()
    #     CSD1.estimateCharges(5)
    #     CSD1.plot_residuals_per_peak(
    #         ax3, CSD1.mspeaks, marker="x", color=tableau20[count]
    #     )
    #     ms.csds.append(CSD1)

    # plt.plot()
    # # rplt.show()


# Navigation bar and logo
logo = "assets/ThalassinosLogo.png"
encoded_logo = base64.b64encode(open(logo, "rb").read())

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            src="data:image/png;base64,{}".format(
                                encoded_logo.decode()
                            ),
                            height="20px",
                        )
                    ),
                    dbc.Col(
                        dbc.NavbarBrand(
                            "Triton: A web dashboard for native IMMS data",
                            className="navbar-brand",
                        )
                    ),
                ],
                align="center",
                justify="between",
                no_gutters=True,
            ),
            href="/",
        )
    ],
    color="light",
    dark=False,
)

# Content definitions
card_content_settings = [
    dbc.CardHeader("Choose your settings"),
    dbc.CardBody(
        [
            dcc.Upload(
                id="upload-data",
                children=dbc.Button("Upload Data", color="primary", className="mr-1"),
            ),
            html.Label("Select grain:"),
            dcc.Slider(
                id="grain-slider", min=0, max=20, value=10, marks={0: "0", 20: "20"}
            ),
            html.Label("Select the order of the poly:"),
            dcc.Slider(
                id="poly-order-slider",
                min=0,
                max=10,
                value=5,
                marks={0: "0", 5: "5", 10: "10"},
            ),
            html.Label("Select the smooth parameter:"),
            dcc.Slider(
                id="smoothes-slider", min=0, max=10, value=2, marks={0: "0", 10: "10"}
            ),
            html.Label("Select the window length:"),
            dcc.Slider(
                id="windowlen-slider",
                min=0,
                max=100,
                value=10,
                marks={0: "0", 50: "50", 100: "100"},
            ),
            html.Label("Simulated peak:"),
            dcc.Slider(
                id="simulpeak-slider",
                min=0,
                max=120,
                value=75,
                marks={0: "0", 50: "50", 100: "100"},
            ),
        ]
    ),
]

adt_content_settings = [
    dbc.CardHeader("ADT Plot"),
    dbc.CardBody([dcc.Graph(id="adt-graph")]),
]

csd_content_settings = [
    dbc.CardHeader("CSD Plot"),
    dbc.CardBody([dcc.Graph(id="csd-graph")]),
]

input_data_raw = dbc.Row(
    [
        dbc.Col(dbc.Card(card_content_settings, outline=True), md=2),
        dbc.Col(dbc.Card(adt_content_settings, outline=True), md=5),
        dbc.Col(dbc.Card(csd_content_settings, outline=True), md=5),
    ]
    # className="mb-4"
)

body = html.Div(
    [input_data_raw],
    style={"marginBottom": 50, "marginTop": 25, "text-align": "center"},
)

app.config["suppress_callback_exceptions"] = False
app.layout = html.Div([navbar, body])


@app.callback(
    [
        dash.dependencies.Output("adt-graph", "figure"),
        dash.dependencies.Output("csd-graph", "figure"),
    ],
    [
        dash.dependencies.Input("upload-data", "filename"),
        dash.dependencies.Input("grain-slider", "value"),
        dash.dependencies.Input("poly-order-slider", "value"),
        dash.dependencies.Input("smoothes-slider", "value"),
        dash.dependencies.Input("windowlen-slider", "value"),
        dash.dependencies.Input("simulpeak-slider", "value"),
    ],
)
def update_adt_graph(
    data_file,
    grain_value,
    poly_order_value,
    smoothes_value,
    windowlen_value,
    simulpeak_value,
):
    if data_file is not None:
        atd, msobj = plot_atd(
            DATA_PATH.joinpath(data_file),
            grain_value,
            poly_order_value,
            smoothes_value,
            windowlen_value,
        )
    return (
        go.Figure(tls.mpl_to_plotly(atd)),
        go.Figure(tls.mpl_to_plotly(plot_pp_csd(simulpeak_value, msobj))),
    )


# @app.callback(
#     dash.dependencies.Output("csd-graph", "figure"),
#     [

#     ],
# )
# def update_csd_graph(simulpeak_value):

#     return go.Figure(tls.mpl_to_plotly(plot_pp_csd(simulpeak_value, )))

#     #plotly_fig = tls.mpl_to_plotly( fig )
#     #iplot(plotly_fig)

#     fig = plt.figure(figsize=(12, 8))
#     ax = plt.subplot(111)
#     ms.plot_simulated_spectrum_simple(ax, color=tableau20[0])

#     for counter, csd in enumerate(ms.csds):
#         csd.plot_csd_gaussian(ax, ms.xvals, color=tableau20[counter])
#         csd.plot_simulated_species(ax, ms.xvals, color=tableau20[counter])

#     for peak in found_peaks:
#         peak.plotSimulatedPeak(ax, ms.xvals, fwhm=simul_peak_fwhh, color='grey')

#     plt.plot()

#     #plotly_fig = tls.mpl_to_plotly( fig )
#     #iplot(plotly_fig)

#     #CSD2.filter_theoretical_peaks_using_charges([56, 57, 58, 59])
#     #CSD3.filter_theoretical_peaks_using_charges([45, 46, 47, 48, 49, 50])
#     #CSD4.filter_theoretical_peaks_using_charges([53, 54, 55, 56, 57, 58, 58, 59, 60])
#     #CSD5.filter_theoretical_peaks_using_charges([64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74])

#     ms.leastSquaresOptimisation(fixed_p_fwhh=simul_peak_fwhh)
#     #ms.leastSquaresOptimisation()

#     fig = plt.figure(figsize=(16, 9))
#     #plt.figure(figsize=(12, 8))
#     #plt.rcParams["font.family"] = "Times"
#     ax = plt.subplot(111)
#     ax.spines["top"].set_visible(False)
#     #ax.spines["bottom"].set_visible(False)
#     ax.spines["right"].set_visible(False)
#     ax.spines["left"].set_visible(True)
#     ax.get_xaxis().tick_bottom()
#     ax.get_yaxis().tick_left()

#     ms.plot_simulated_spectrum(ax, showcharges='False')

#     #DONEED
#     plt.show()
#     #plotly_fig = tls.mpl_to_plotly( fig )

#     # CSD4 = MsCSD()
#     # CSD4.name = 'CSD4'
#     # CSD4.p_fwhh = 10
#     # CSD4_peak_indexes = [20, 21, 22, 23, 24, 25, 26, 27]
#     # indexed_peaks = pp.get_peaks_using_indexes(CSD4_peak_indexes)
#     # CSD4.mspeaks = indexed_peaks
#     # CSD4.calculateMassAndCharges(CSD4.mspeaks)
#     # CSD4.optimiseParameters()
#     # CSD4.estimateCharges(5)
#     # #CSD2.filter_theoretical_peaks_using_charges([56, 57, 58, 59])
#     # CSD4.plot_residuals_per_peak(
#     #     ax,
#     #     CSD4.mspeaks,
#     #     marker='x',
#     #     color='blue',
#     # )
#     # plt.plot()

#     # CSD5 = MsCSD()
#     # CSD5.name = 'CSD5'
#     # CSD5.p_fwhh = 10
#     # CSD5_peak_indexes = [29, 30, 31, 32, 33, 34, 35]
#     # indexed_peaks = pp.get_peaks_using_indexes(CSD5_peak_indexes)
#     # CSD5.mspeaks = indexed_peaks
#     # CSD5.calculateMassAndCharges(CSD5.mspeaks)
#     # CSD5.optimiseParameters()
#     # CSD5.estimateCharges(5)
#     # #CSD2.filter_theoretical_peaks_using_charges([56, 57, 58, 59])
#     # CSD5.plot_residuals_per_peak(
#     #     ax,
#     #     CSD5.mspeaks,
#     #     marker='x',
#     #     color='blue',
#     # )
#     # plt.plot()

if __name__ == "__main__":
    app.run_server(debug=False, host="127.0.0.1", port=5000, threaded=True)
