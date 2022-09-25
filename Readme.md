
# QR Code Scanner

This project has 2 parts, the back end qr handler and the front end UI. The front end is made using
PySimpleGUI and all it does is take the project out of the command line. The qr handler can be used in other projects
as it provides basic and advanced scanning and creating of QR codes.

## Run Locally

Clone the project

```bash
  git clone https://github.com/Ironislife98/QRCodeScanner.git
```

Go to the project directory

```bash
  cd QRCodeScanner
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python main.py
```


## Advanced Mode Options

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

## Acknowledgements

 - [Pure python QR Code generator](https://github.com/lincolnloop/python-qrcode)
 
## Authors

- [@Ironislife98](https://github.com/Ironislife98)

