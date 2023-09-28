import PySimpleGUI as sg

layout = [
    [sg.Button(word) for word in 'Elővettem a buszon'],
    [sg.Button('Close')]
]

window = sg.Window('Makk', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':
        break
window.close()