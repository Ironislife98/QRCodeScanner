import QrUtil
import PySimpleGUI as sg

#QrUtil.generate_qrcode("https://www.google.com", "google.png")

#QrUtil.generate_advanced_qrcode("google.com", "advanced.png", QrUtil.qrcode.constants.ERROR_CORRECT_L, True, [QrUtil.VerticalBarsDrawer(), QrUtil.HorizontalGradiantColorMask()])

#QrUtil.scan_qrcode("advanced.png")




sg.theme('Blue Mono')

scan_layout = [
    [sg.Text("Please select an image file")],
    [sg.InputText(key='-file1-'), sg.FileBrowse()],
    [sg.Button("Scan")],
    [sg.Text("OR")],
    [sg.Button("Take QR code from your camera")],
    [sg.T(s=(100,25))]
]

create_layout = [
    [sg.Text("Hello")]

]


layout = [[sg.Text('Scan or create a QR code')],
          [sg.TabGroup([[sg.Tab('Scan', scan_layout), sg.Tab('Create', create_layout)]])],
          [sg.Button('Cancel')]]



window = sg.Window("QR Code Scanner", layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Cancel"):
        break
    elif event == "Scan":
        filename = values['-file1-']
    elif event == "Take QR code from your camera":
        print("opening camera")
        
window.close()