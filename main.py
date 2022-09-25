import QrUtil
import PySimpleGUI as sg

width, height = 90, 10


sg.theme('Blue Mono')

scan_layout = [
    [sg.Text("Please select an image file")],
    [sg.InputText(key='-file1-'), sg.FileBrowse()],
    [sg.Button("Scan")],
    [sg.Text("OR")],
    [sg.Button("Take QR code from your camera")],
    [sg.T(s=(width, height))]
]

create_column_layout = [
    [sg.Button("Create basic QR code")],
    [sg.Button("Create advanced QR code")],
    [sg.T(s=(width,height))]

]

def block_focus(window):
    for key in window.key_dict:   
        element = window[key]
        if isinstance(element, sg.Button):
            element.block_focus()

# ALL VARIABLES:    LINK,FILENAME,VERSION(1-40),BOXSIZE,BORDER
def popup_basic_menu():
    col_layout = [[sg.Button("Create", bind_return_key=True), sg.Button('Cancel')]]
    layout = [
        [[sg.Text("QR code link:")], [sg.InputText(key="link")]],
        [[sg.Text("Filename:")], [sg.InputText(key="filename")]],
        [[sg.Text("Version (1-40):")], [sg.InputText(key="version")]],
        #[[sg.Text("Box size:")], [sg.InputText(key="boxsize")]],
        #[[sg.Text("Border")], [sg.InputText(key="border")]],
        [sg.Column(col_layout, expand_x=True, element_justification='right')]
        #[sg.T(s=(width, height))]
    ]
    window = sg.Window("Basic QR code maker", layout, use_default_focus=False, finalize=True, modal=True)
    block_focus(window)
    event, values = window.read()
    window.close()
    
    # Will append .png to end of file if not already
    if values["filename"][-4:] != ".png":
        values["filename"] = values["filename"] + ".png" 
    try:
        # If user doesn't set version correctly, set to 1
        if int(values["version"]) not in range(1, 40):
            values["version"] = 1
    except ValueError:
        sg.popup_error("One or more fields left empty")
        popup_basic_menu()
    try:
        QrUtil.generate_qrcode(values["link"], values["filename"], values["version"],10, 4)
        sg.popup_auto_close(f"{values['filename']} created!", auto_close_duration=2)
    except NameError:
        sg.popup_error("One or more fields left empty")
        popup_basic_menu()


# ALL VARIABLES: LINK, FILENAME, ERR_CORR, COLOR MASK, PIL DRAWER
# ERR correction will be auto set to ERROR_CORRECT_M - 15%
def popup_advanced_menu():
    errorcorrlist = ["7%", "15%", "25%", "30%"]
    errorcorrtechnicallist = [QrUtil.qrcode.ERROR_CORRECT_L, QrUtil.qrcode.ERROR_CORRECT_M, QrUtil.qrcode.ERROR_CORRECT_Q, QrUtil.qrcode.ERROR_CORRECT_H]
    colormasklist = ["Solid Fill", "Radial Gradient", "Square Gradient", "Horizontal Gradient", "Vertical Gradient", "Image"]
    pildrawerlist = ["Square", "Gapped Square", "Circle", "Rounded", "Vertical Bars", "Horizontal Bars"]

    col_layout = [[sg.Button("Create", bind_return_key=True), sg.Button('Cancel')]]
    layout = [
        [sg.Text("QR code link:"), sg.InputText(key="link")],
        [sg.Text("Filename:"), sg.InputText(key="filename")],
        [sg.Text("Error Correction Percentage:"), sg.Combo(errorcorrlist, default_value=errorcorrlist[2], key="errorcorr")],
        [sg.Text("Color Masks:"), sg.Combo(colormasklist, default_value=colormasklist[0], key="colormask")],
        [sg.Text("Render Mode:"), sg.Combo(pildrawerlist, default_value=pildrawerlist[0], key="pildrawer")],
        [sg.Column(col_layout, expand_x=True, element_justification='right')]
    ]

   

    window = sg.Window("Advanced QR code maker", layout, use_default_focus=False, finalize=True, modal=True)
    block_focus(window)
    event, values = window.read()
    window.close() 
    if values["filename"][-4:] != ".svg":
        values["filename"] = values["filename"] + ".svg" 
    values["errorcorr"] = errorcorrtechnicallist[errorcorrlist.index(values["errorcorr"])]
    try:
        QrUtil.generate_advanced_qrcode(values["link"], values["filename"], values["errorcorr"], values["colormask"], values["pildrawer"])
        sg.popup_auto_close(f"{values['filename']} created!", auto_close_duration=2)
    except NameError:
        sg.popup_error("One or more fields left empty")
        popup_basic_menu()

layout = [[sg.Text('Scan or create a QR code')],
          [sg.TabGroup([[sg.Tab('Scan', scan_layout), sg.Tab('Create', [[sg.Column(create_column_layout)]])]])],
          [sg.Button('Cancel')]]



window = sg.Window("QR Code Scanner", layout, icon="Images/qr-code.ico")

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Cancel"):
        break
    elif event == "Scan":
        path = values['-file1-']
        if not QrUtil.scan_qrcode(path):
            sg.popup_error("Select a valid QR code!")
    elif event == "Take QR code from your camera":
        print("opening camera")
        if not QrUtil.camera_scan_qr():
            sg.popup_auto_close("Exited")
    elif event == "Create basic QR code":
        action = popup_basic_menu()
    elif event == "Create advanced QR code":
        action = popup_advanced_menu()

window.close()