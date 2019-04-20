import numpy as np
import matplotlib.pyplot as plt
import ichorlib.genClasses.colorPalette as cp


seq = 'AITGTKIIERHKLILEWKAITGTKIIERHKLILEWKAITGTKIIERHAITGTKIIERHKLILEWKAI' \
      'TGTKIIERHKLILEWKAITGTKIIERHKLKKKILEWKAITGTKIIERHKLILEWKAITGTKIIERHKL' \
      'ILEWKAITGTKIIERHKLKILEWKAITGTKIIERHKLILEWKAITGTKIIERHKLILEWKAITGTKIK' \
      'IERHKLILEWKAITGTKIIERHKLILEWK'

seq2 = 'AITGTKIIERHKLILEWKAITGTKIIERHKLILEWKAITGTKIIERHAITGTKIIERHKLILEWKAI' \
      'TGTKIIERHKLILEWKAITGTKIIERHKLKKKILEWKAITGTKIIERHKLILEWKAITGTKIIERHKL' \
      'ILEWKAITGTKIIERHKLKILEWKAITGTKIIERHKLILEITGTKIIERHKLKILEWKAITGTKIIERHKLILEITGTKIIERHKLKILEWKAITGTKIIERHKLILEWKAITGTKIIERHKLILEWKAITGTKIK' \
      'IERHKLILEWKAITGTKIIERHKLILEWK'


def plotHighlightedSeq(ax,
                       seq,
                       aatohoghlight='K',
                       blockfrom=0,
                       blockto=0,
                       **kwargs):

    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    width = 1  #width of the bar
    height = 0.25  #height of the bar found that 0.15 works best
    for i, aa in enumerate(seq):
        if aa == aatohoghlight:
            # print i
            ln = ax.bar(i,
                        height,
                        width,
                        color=cp.tableau20[6],
                        edgecolor="none")
        else:
            ln = ax.bar(i,
                        height,
                        width,
                        color=cp.tableau20[11],
                        edgecolor="none")

    # color membrane topology
    if blockfrom > 0 and blockto > 0:
        for i, aa in enumerate(seq):
            if i >= blockfrom and i <= blockto:
                ln = ax.bar(i,
                            height,
                            width,
                            color=cp.tableau20[2],
                            alpha=0.5,
                            edgecolor="none")

    return ln


fig, (ax1, ax2) = plt.subplots(nrows=2,
                               ncols=1,
                               figsize=(16, 4),
                               sharex=True,
                               sharey=True)
plotHighlightedSeq(ax1, seq, aatohoghlight='E', blockfrom=10, blockto=50)
plotHighlightedSeq(ax2, seq2)

plt.rcParams["font.family"] = "Arial"
plt.xticks(fontsize=16)
#plt.ylim(0,0.25)
plt.show()
#plt.savefig('highlightK.png', dpi=300)
