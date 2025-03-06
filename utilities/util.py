"""
    Función para convertir ObjectId a str
"""


def str_object_id(document):
    if "_id" in document:
        document["_id"] = str(document["_id"])
    return document