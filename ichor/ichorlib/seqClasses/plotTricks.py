df = pd.read_csv('MNXLResultsTable.csv')

ind = np.arange(len(df['NoV-Cor']))
width = 0.2

plt.figure()

# These are the "Tableau 20" colors as RGB.
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

# You typically want your plot to be ~1.33x wider than tall. This plot is a rare
# exception because of the number of lines being plotted on it.
# Common sizes: (10, 7.5) and (12, 9)
plt.figure()
#plt.figure(figsize=(18, 6))

# Remove the plot frame lines. They are unnecessary chartjunk.
ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# Ensure that the axis ticks only show up on the bottom and left of the plot.
# Ticks on the right and top of the plot are generally unnecessary chartjunk.
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

# Limit the range of the plot to only where the data is.
# Avoid unnecessary whitespace.
plt.ylim(-0.3, 0.9)
#plt.xlim(1968, 2014)

# Make sure your axis ticks are large enough to be easily read.
# You don't want your viewers squinting to read your plot.
#plt.yticks(range(0, 91, 10), [str(x) + "%" for x in range(0, 91, 10)], fontsize=14)
#plt.xticks(fontsize=14)

# Provide tick lines across the plot to help your viewers trace along
# the axis ticks. Make sure that the lines are light and small so they
# don't obscure the primary data lines.
print(np.linspace(-0.2, 0.8, 11))
for y in np.linspace(-0.2, 0.8, 11):
    plt.plot(list(range(0, 15)), [y] * len(list(range(0, 15))),
             "--",
             lw=0.5,
             color="black",
             alpha=0.2)

# Remove the tick marks; they are unnecessary with the tick lines we just plotted.
plt.tick_params(axis="both",
                which="both",
                bottom="off",
                top="off",
                labelbottom="on",
                left="off",
                right="off",
                labelleft="on")

#rotate x-axis labels to fit on graph
ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=90)

plt.rcParams["font.family"] = "Arial"

plt.bar(ind,
        df['MMXL-Cor'],
        width,
        color=tableau20[0],
        label='MNXL',
        edgecolor="none")
plt.bar(ind + width,
        df['NoV-Cor'],
        width,
        color=tableau20[1],
        label='NoV',
        edgecolor="none")
plt.bar(ind + width + width,
        df['SoVD-Cor'],
        width,
        color=tableau20[2],
        label='SoVD',
        edgecolor="none")
plt.xticks(ind, df['PDB'], fontsize=18)
plt.yticks(fontsize=18)

plt.legend(bbox_to_anchor=(1.0, 1), loc=0, borderaxespad=0., fontsize=18)
plt.savefig('foo.png', dpi=300)
