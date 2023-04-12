import smtplib
from keys import password as PASSWORD
from checker import check_missing_and_prep_msg

my_email = "testpythondays@gmail.com"
password = PASSWORD

coming_data = {'email':'prachetpy@gmail.com', 'missing':[1,1,1], 'name': 'Prachet'}

result = check_missing_and_prep_msg(coming_data['missing'])
print(result)

try:
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        # This line makes the connection secure by encrypting the message
        try:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                            to_addrs=coming_data['email'],
                            msg=f"Subject:Regarding your Rental Application\n\n{result}")
        except Exception as e:
            print(e)
except Exception as e:
            print(e)
