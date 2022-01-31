import os
import cv2
import PySimpleGUI as sg
from tkinter import filedialog

sg.theme("Default")

encryptLayout = [
    [
        sg.Text("Message to be hidden"),
        sg.InputText(key="-MESSAGE-TO-BE-HIDDEN-"),
    ],
    [
        sg.Text("Path of image used for encryption"),
        sg.FileBrowse(key="-PATH-OF-IMAGE-",
                      file_types=(
                          ("Image Files", "*.png"),
                          ("All files", "*.*"),
                      )),
    ],
    [sg.Button("Encrypt")],
]
decryptLayout = [[
    sg.Text("Path of encrypted image"),
    sg.FileBrowse(key="-PATH-OF-ENCRYPTED-IMAGE-",
                  file_types=(
                      ("Image Files", "*.png"),
                      ("All files", "*.*"),
                  )),
], [sg.Button("Decrypt")], [sg.Text("", key="-DECRYPTED-TEXT-")]]
layout = [[
    sg.TabGroup([[sg.Tab("Encrypt", encryptLayout)],
                 [sg.Tab("Decrypt", decryptLayout)]])
]]
window = sg.Window('Stegnography', layout)

MESSAGE_ENDING = "@@"


def message_to_bits(message):
    bitsString = ""
    for char in message:
        bitsString += format(ord(char), "08b")
    return bitsString


[[(255, 69, 62), (255, 255, 255)], [(255, 255, 255), (255, 255, 255)]]


def encode(image, message):
    message += MESSAGE_ENDING
    bitsMessage = message_to_bits(message)

    currentIndex = 0
    for groupIndex, group in enumerate(image):
        for pixelIndex, pixel in enumerate(group):
            for colorIndex, color in enumerate(pixel):
                if currentIndex == len(bitsMessage):
                    break

                bits = format(color, "08b")
                bits = bits[:-1] + bitsMessage[currentIndex]
                image[groupIndex][pixelIndex][colorIndex] = int(bits, 2)
                currentIndex += 1
    return image


def decode(image):
    bitsMessage = ""
    for group in image:
        for pixel in group:
            for color in pixel:
                colorBits = format(color, "08b")
                bitsMessage += colorBits[-1]
    bytesMessage = [
        bitsMessage[i:i + 8] for i in range(0, len(bitsMessage), 8)
    ]

    finalMessage = ""
    for byteMsg in bytesMessage:
        char = int(byteMsg, 2)
        finalMessage += chr(char)

    finalMessage = finalMessage.split(MESSAGE_ENDING)[0]
    return finalMessage


def load_image(filePath):
    image = cv2.imread(filePath)
    return image


def write_image(filePath, image):
    cv2.imwrite(filePath, image)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == "Encrypt":
        message = values["-MESSAGE-TO-BE-HIDDEN-"]
        image_path = values["-PATH-OF-IMAGE-"]
        image_data = load_image(image_path)
        new_image = encode(image_data, message)

        new_image_path = image_path.split(".")
        new_image_path = "".join(
            new_image_path[:-1]) + "-Secret." + new_image_path[-1]
        write_image(new_image_path, new_image)
        os.startfile(new_image_path)

    elif event == "Decrypt":
        image_path = values["-PATH-OF-ENCRYPTED-IMAGE-"]
        encode_image = load_image(image_path)
        decoded_message = decode(encode_image)
        window.Element("-DECRYPTED-TEXT-").update(decoded_message)

window.close()
