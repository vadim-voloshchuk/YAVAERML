


def processing_message(message, template=None):
    file = None
    if template != None:
        file = open("fictitious_nn/Finalnaya_versia.docx", "rb")
    return message, file.read()
