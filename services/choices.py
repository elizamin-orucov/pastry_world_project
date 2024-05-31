from datetime import datetime

now_date = int(datetime.now().strftime("%Y")) + 1


def year_choice():
    return ((year, year) for year in range(2011, now_date))


RATING = (
    (1, "★✩✩✩✩"),
    (2, "★★✩✩✩"),
    (3, "★★★✩✩"),
    (4, "★★★★✩"),
    (5, "★★★★★"),
)


DISCOUNT_CHOICES = (
    (5, "5% off"),
    (10, "10% off"),
    (15, "15% off"),
    (20, "20% off"),
    (25, "25% off"),
    (30, "30% off"),
    (40, "40% off"),
    (50, "50% off"),
    (60, "60% off"),
    (70, "70% off"),
)


PRODUCT_STATUS_CHOICES = (
    ("Sold", "Sold"),
    ("In stock", "In stock"),
    ("Will available", "Will available")
)

