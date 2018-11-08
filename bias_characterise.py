import numpy as np
from sys import argv
from matplotlib import pyplot as plt
from phonecal import raw, plot, io
from phonecal.general import gaussMd

folder = io.path_from_input(argv)
root, images, stacks, products, results = io.folders(folder)
phone = io.read_json(root/"info.json")

isos, means = io.load_means (folder, retrieve_value=io.split_iso)
colours     = io.load_colour(stacks)

savefolder = results/"bias"

xmax = phone["software"]["bias"] + 25
xmin = max(phone["software"]["bias"] - 25, 0)

for iso, mean in zip(isos, means):
    gauss = gaussMd(mean, sigma=10)
    mean_RGBG, _ = raw.pull_apart(mean, colours)
    gauss_RGBG = gaussMd(mean_RGBG, sigma=(0,5,5))
    vmin, vmax = gauss_RGBG.min(), gauss_RGBG.max()
    
    plot.hist_bias_ron_kRGB(mean_RGBG, xlim=(xmin, xmax), xlabel="Bias (ADU)", saveto=savefolder/f"histogram_iso{iso}.pdf", nrbins=100)

    plot.show_image(gauss, colorbar_label="Bias (ADU)", saveto=savefolder/f"gauss_iso{iso}.pdf")
    for j, c in enumerate("RGBG"):
        X = "2" if j == 3 else ""
        plot.show_image(gauss_RGBG[j], colorbar_label="Bias (ADU)", saveto=savefolder/f"{c}{X}_gauss_iso{iso}.pdf", colour=c, vmin=vmin, vmax=vmax)
        
    plot.show_RGBG(gauss_RGBG, colorbar_label=25*" "+"Bias (ADU)", saveto=savefolder/f"all_gauss_iso{iso}.pdf", vmin=vmin, vmax=vmax)
        
    print(f"ISO: {iso} ; Mean: {mean_RGBG.mean():.3f} ; Median: {np.median(mean_RGBG):.3f} ; Max: {mean_RGBG.max():.3f} ; Min: {mean_RGBG.min():.3f} ; Standard deviation: {mean_RGBG.std():.3f}")