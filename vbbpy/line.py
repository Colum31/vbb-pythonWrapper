class Line:
    """
    Contains information about a line.
    """

    lineId = ""
    name = ""
    product = ""

    def __init__(self, lineId: str, name: str, product: str):
        self.lineId = lineId
        self.name = name
        self.product = product

    def __str__(self):
        return "{}: {} is a {}".format(self.lineId, self.name, self.product)
