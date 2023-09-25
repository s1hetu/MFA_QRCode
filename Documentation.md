### Create Secret and URL for setting authentication using authentictor app
<br>

- Generate a 32-character base32 secret that is compatible with any OTP application.

  ```python 
    otp_base32 = pyotp.random_base32()
    ```

[//]: # (e.g O5SVKFBA7G5JYY2ALSVWSYP2PDXL5SMH&#41;)

- Generate the provisioning URI for use with a QR Code generator by calling provisioning_url of TOTP class.
    ```python 
    otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(name=email.lower(), issuer_name="codevoweb.com")
    ```


[//]: # (e.g otpauth://totp/codevoweb.com:abc?secret=O5SVKFBA7G5JYY2ALSVWSYP2PDXL5SMH&issuer=codevoweb.com
otpauth://totp/issuer_name:name?secret=O5SVKFBA7G5JYY2ALSVWSYP2PDXL5SMH&issuer=issuer_name)

- Create TOTP instance
    ```python 
    totp = pyotp.TOTP(user.otp_base32)
  ```

- Verify OTP
    ```python
    totp.verify(otp_token)
    ```
    Returns True if otp matches the one provided in authenticator app else False


[//]: # (```python)

[//]: # (totp.verify&#40;otp_token, valid_window=1&#41;)

[//]: # (```)

[//]: # ()
[//]: # (valid_window parameter will extend the token’s validity to the counter ticks before and after the current one.)

<br>

### Generate QR Code from the url generated

```python
import qrcode
qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
qr.add_data(otp_auth_url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save('name.png')
```

#### version

- The version parameter is an integer from 1 to 40 that controls the size of the QR Code (the smallest, version 1, is a
  21x21 matrix).
- Set to None and use the fit parameter when making the code to determine this automatically.

#### fill_color and back_color

- fill_color and back_color can change the background and the painting color of the QR, when using the default image
  factory.

#### error_correction

- The error_correction parameter controls the error correction used for the QR Code. The following four constants are
  made available on the qrcode package:


1. ERROR_CORRECT_L
    - About 7% or less errors can be corrected.

2. ERROR_CORRECT_M (default)
    - About 15% or less errors can be corrected.

3. ERROR_CORRECT_Q
    - About 25% or less errors can be corrected.

4. ERROR_CORRECT_H.
    - About 30% or less errors can be corrected.

#### box_size

- The box_size parameter controls how many pixels each “box” of the QR code is.

#### border

- The border parameter controls how many boxes thick the border should be (the default is 4, which is the minimum
  according to the specs).

