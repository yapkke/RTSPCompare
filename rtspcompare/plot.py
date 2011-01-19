def finalize_plot(plot):
    plot.xlabel("Position")
    plot.ylabel("PSNR")

    plot.xlim(0.5, 5.5)
    plot.ylim(ymin=10)
