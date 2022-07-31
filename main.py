import QrUtil
import PySimpleGUI as sg

#QrUtil.generate_qrcode("https://www.google.com", "google.png")

#QrUtil.generate_advanced_qrcode("google.com", "advanced.png", QrUtil.qrcode.constants.ERROR_CORRECT_L, True, [QrUtil.VerticalBarsDrawer(), QrUtil.HorizontalGradiantColorMask()])

#QrUtil.scan_qrcode("advanced.png")

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
    for key in window.key_dict:    # Remove dash box of all Buttons
        element = window[key]
        if isinstance(element, sg.Button):
            element.block_focus()

# ALL VARIABLES:    LINK,FILENAME,VERSION(1-40),BOXSIZE,BORDER
def popup_basic_menu():
    col_layout = [[sg.Button("Create", bind_return_key=True), sg.Button('Cancel')]]
    layout = [
        [[sg.Text("QR code link:")], [sg.InputText(key="link")]],
        [[sg.Text("Filename:")], [sg.InputText(key="filename")]],
        [[sg.Text("Version:")], [sg.InputText(key="version")]],
        #[[sg.Text("Box size:")], [sg.InputText(key="boxsize")]],
        #[[sg.Text("Border")], [sg.InputText(key="border")]],
        [sg.Column(col_layout, expand_x=True, element_justification='right')]
        #[sg.T(s=(width, height))]
    ]
    window = sg.Window("Basic QR code maker", layout, use_default_focus=False, finalize=True, modal=True)
    block_focus(window)
    event, values = window.read()
    window.close()
    print(values) 
    if values["filename"][-4:] != ".png":
        values["filename"] = values["filename"] + ".png"    
    QrUtil.generate_qrcode(values["link"], values["filename"], values["version"],10, 4)
    sg.popup_auto_close(f"{values['filename']} created!", auto_close_duration=2)

def popup_advanced_menu():
    pass

layout = [[sg.Text('Scan or create a QR code')],
          [sg.TabGroup([[sg.Tab('Scan', scan_layout), sg.Tab('Create', [[sg.Column(create_column_layout)]])]])],
          [sg.Button('Cancel')]]



window = sg.Window("QR Code Scanner", layout)

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