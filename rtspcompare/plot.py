def finalize_plot(plot):
    plot.xlabel("Position")
    plot.ylabel("PSNR")

    plot.xlim(0.5, 5.5)
    plot.ylim(ymin=10)

def update_ap_label(label):
    return label.\
           replace("c", "A").\
           replace("e","B").\
           replace("f","C")
