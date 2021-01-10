import gaugan

with open('frame000138.png', "rb") as fh:
    image = gaugan.segmentImage(fh.read())
    image = gaugan.processImage(image)

with open('output-map3.png', "wb") as fh:
    fh.write(image)
