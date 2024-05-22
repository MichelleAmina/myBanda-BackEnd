import smtplib


email = "youremail@example.com"
reciver_email = "receivers email@exaple.com"


subject = "Hello"
message = "this is a test email"

text = f"subject: {subject}\n\n{message}"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()


server.login(email, "your password")

server.sendmail(email, reciver_email, text)

print("Emal Has Been sent to", reciver_email)
