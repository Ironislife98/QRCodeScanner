import qrcode
import qrcode.image.svg
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, SquareModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SolidFillColorMask, SquareGradiantColorMask, HorizontalGradiantColorMask, VerticalGradiantColorMask, ImageColorMask
import cv2
import pyzbar.pyzbar as pyzbar
import webbrowser

chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

def generate_qrcode(link, filename, version, boxsize, border):
    #img = qrcode.make(link)
    #img.save(filename)
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=boxsize,
        border=border
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    

# method
""" 12 types of styles

    PIL MODULE DRAWERS
    --------------------
    SquareModuleDrawer()
    GappedSquareModuleDrawer()
    CircleModuleDrawer()
    RoundedModuleDrawer()
    VerticalBarsDrawer()
    Horizontal Bars Drawer

    COLOR MASKS
    --------------------
    SolidFillColorMask()
    RadialGradientColorMask()
    SquareGradientColorMask()
    HorizontalGradiantColorMask()
    VerticalGradientColorMask()
    ImageColorMask()
"""
def generate_advanced_qrcode(link, filename, error_corr, styled, typeofstyle):
    qr = qrcode.QRCode(error_correction=error_corr)
    qr.add_data(link)
    if not styled:
        img = qr.make_image(image_factory=StyledPilImage)
        img.save(filename)
    else:
        img = qr.make_image(image_factory=StyledPilImage, module_drawer=typeofstyle[0], color_mask=typeofstyle[1])
        img.save(filename)

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


"""cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        _, img = cap.read()
        data, bbox, _ = detector.detectAndDecode(img)
        if bbox is not None:
            for i in range(len(bbox)):
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
            if data:
                print("[+] QR Code detected, data:", data)
        cv2.imshow("img", img)
        if cv2.waitKey(1) == ord("q"):
            break"""
    