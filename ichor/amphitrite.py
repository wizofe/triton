import base64
import io
import pathlib

from ichorlib.msClasses.MassSpectrum import MassSpectrum
from ichorlib.genClasses.PeakPicking import PeakPicking
from ichorlib.msClasses.MsCSD import MsCSD
from ichorlib.genClasses.colorPalette import tableau20
import matplotlib.pyplot as plt, mpld3

# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplotN
import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import json

external_stylesheets = ["https://code.getmdl.io/1.3.0/material.min.js"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

grain_param = 10
poly_order_param = 5
smoothes_param = 2
window_len_param = 10
simul_peak_fwhh = 75

# Set the relative data path
MYPATH = pathlib.Path(__file__).parent
DATA_PATH = MYPATH.joinpath("data").resolve()


def parse_contents(contents):
    _, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    return io.StringIO(decoded.decode("utf-8"))


def plot_atd(
    f,
    grain=grain_param,
    poly_order=poly_order_param,
    smoothes=smoothes_param,
    window_len=window_len_param,
):
    """ Plot the Arrival Time Distribution (ATD)

    Args:
    f (path): The f with the data (tab delim. CSV)

    Returns:
    It shows a plot. TODO: Return a matplotlib/plotly/JSON object
    """
    # Plot the ATD
    ms = MassSpectrum()
    ms.read_text_file(f, grain=grain_param, normalisationtype="bpi")
    ms.smoothingSG(
        poly_order=poly_order_param,
        smoothes=smoothes_param,
        window_len=window_len_param,
    )
    ms.normalisation_bpi()
    # ms.select_ms_range(4200,9000)

    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot(311)
    ms.plot_simulated_spectrum_simple(ax, color=tableau20[2])
    plt.plot()

    return fig


def plot_pp_csd(ms, simul_peak_fwhh):
    pp = PeakPicking()
    pp.calculate_gradient(ms.xvals, ms.yvals)
    found_peaks = pp.find_peaks(1)

    # #fig = plt.figure(figsize=(12, 8))
    # ax2 = plt.subplot(312)
    # ms.plot_simulated_spectrum_simple(ax2, color=tableau20[6])
    # for peak in found_peaks:
    #     peak.plotSimulatedPeak(ax2,
    #                            ms.xvals,
    #                            fwhm=simul_peak_fwhh,
    #                            color=tableau20[5])

    # plt.show()
    # #plotly_fig = tls.mpl_to_plotly(fig)

    # fig = plt.figure(figsize=(12, 8))
    ax4 = plt.subplot(312)
    ax3 = plt.subplot(313)
    ms.plot_simulated_spectrum_simple(ax4, color=tableau20[0])
    for peak in found_peaks:
        peak.plotSimulatedPeak(ax4, ms.xvals, fwhm=simul_peak_fwhh, color=tableau20[2])

    peaks_for_csds = [[32, 36, 42, 48, 54], [38, 45, 50], [28, 33, 41]]
    #    peaks_for_csds = [[12, 36, 42, 48, 54], [38, 45, 50], [28, 33, 41]]

    ms.csds = []
    for count, peak_set in enumerate(peaks_for_csds):
        CSD1 = MsCSD()
        CSD1.name = "CSD" + str(count)
        CSD1.p_fwhh = simul_peak_fwhh
        CSD1_peak_indexes = peak_set
        indexed_peaks = pp.get_peaks_using_indexes(CSD1_peak_indexes)
        CSD1.mspeaks = indexed_peaks
        CSD1.calculateMassAndCharges(CSD1.mspeaks)
        CSD1.optimiseParameters()
        CSD1.estimateCharges(5)
        CSD1.plot_residuals_per_peak(
            ax3, CSD1.mspeaks, marker="x", color=tableau20[count]
        )
        ms.csds.append(CSD1)

    plt.plot()
    # rplt.show()


app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("icons/ThalassinosLogo.png"),
                            id="thalassinos-logo",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3("Triton", style={"margin-bottom": "0px"}),
                                html.H5(
                                    "A native IMMS dashboard",
                                    style={"margin-top": "0px"},
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [dcc.Upload(id="upload-data", children=html.Button("Upload Data"))],
                    className="one-third column",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [html.Div([dcc.Graph(id="adt-graph")], className="row flex-display")],
            className="row flex-display",
        ),
    ],
    style={"display": "flex", "flex-direction": "column"},
)


@app.callback(
    dash.dependencies.Output("adt-graph", "figure"),
    [dash.dependencies.Input("upload-data", "filename")],
)
def update_adt_graph(data_file):
    if data_file is not None:
        figure = go.Figure(tls.mpl_to_plotly(plot_atd(DATA_PATH.joinpath(data_file))))
    else:
        figure = ""
    return figure


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
    app.run_server(debug=False, host="127.0.0.1", port=5000)
