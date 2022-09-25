import os
try:
    import qrcode
    import qrcode.image.svg
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, SquareModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer
    from qrcode.image.styles.colormasks import RadialGradiantColorMask, SolidFillColorMask, SquareGradiantColorMask, HorizontalGradiantColorMask, VerticalGradiantColorMask, ImageColorMask
    import cv2
    import pyzbar.pyzbar as pyzbar
    import webbrowser
    import wand.image
except ModuleNotFoundError:
    os.system("pip install -r requirements.txt")
    print("Run application again")

chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

def generate_qrcode(link, filename, version, boxsize, border):
    #img = qrcode.make(link)
    #img.save(filename)
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=boxsize,
        border=border
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    

# method
""" 
    PIL MODULE DRAWERS
    --------------------
    SquareModuleDrawer()
    GappedSquareModuleDrawer()
    CircleModuleDrawer()
    RoundedModuleDrawer()
    VerticalBarsDrawer()
    HorizontalBarsDrawer()

    COLOR MASKS
    --------------------
    SolidFillColorMask()
    RadialGradientColorMask()
    SquareGradientColorMask()
    HorizontalGradiantColorMask()
    VerticalGradientColorMask()
    ImageColorMask()

    ERROR CORRECTION MODE
    ---------------------
    ERROR_CORRECT_L - 7%
    ERROR_CORRECT_M - 15%
    ERROR_CORRECT_Q - 25%
    ERROR_CORRECT_H - 30%  
"""

def generate_advanced_qrcode(link, filename, error_corr, colormask, pildrawer):
    qr = qrcode.QRCode(error_correction=error_corr)
    qr.add_data(link)
    img = qr.make_image(image_factory=qrcode.image.svg.SvgPathFillImage, module_drawer=pildrawer, color_mask=colormask)
    img.save(filename)
    f = open(f"{filename}")
    #svg2png(bytestring=f.read().encode("utf-8"),write_to=f"{filename}.png")
    with wand.image.Image(blob=f.read().encode("utf-8"), format="svg" ) as image:
        png_image = image.make_blob("png")
    f.close()
    with open(f"{filename[:-4]}.png", "wb") as out:
        out.write(png_image)
    """image = Image.open('/example/path/to/image/file.jpg/')
    image.thumbnail((80, 80), Image.ANTIALIAS)
    image.save('/some/path/thumb.jpg', 'JPEG', quality=88)"""
    os.remove(f"{filename}")

def scan_qrcode(path):
    try:
        img = cv2.imread(path)
        detector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = detector.detectAndDecode(img)
        if bbox is not None:
            print(f"QR Code Data:\n{data}")
        webbrowser.get("chrome").open(str(data))
    except cv2.error:
        print("Not Valid QR code!")
        return False
    return True

def camera_scan_qr():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        _, img = cap.read()
        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            a=data
            break   
        cv2.imshow("Press Q to exit", img)   
        if cv2.waitKey(1) == ord("q"):
            break
    try:
        print(str(a))
        webbrowser.get("chrome").open(str(a))
    except UnboundLocalError:
        print("No QR code found!")
        cap.release()
        cv2.destroyAllWindows()
        return False
    
    cap.release()
    cv2.destroyAllWindows()
    return True