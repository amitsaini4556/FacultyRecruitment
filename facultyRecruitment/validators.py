from django.core.validators import RegexValidator

def validatePhoneNumber():
    # error message when a wrong format entered
    error_message = 'Phone number must be a valid 10 digit number'

     # your desired format
    phone_regex = RegexValidator(
        regex=r'^[6-9]\d{9}$',
        message= error_message,
    )
    return phone_regex