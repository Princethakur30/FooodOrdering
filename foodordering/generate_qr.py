import qrcode

data = "Foodie Demo Payment - Dummy QR"

qr = qrcode.make(data)

qr.save("dummy_payment_qr.png")

print("Dummy QR created!")