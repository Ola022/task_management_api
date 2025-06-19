# import sendgrid
# from sendgrid.helpers.mail import Mail

# sg = sendgrid.SendGridAPIClient(api_key='YOUR_SENDGRID_API_KEY')
# email = Mail(
#     from_email='your_verified_sender@example.com',
#     to_emails='recipient@example.com',
#     subject='Test Email',
#     plain_text_content='This is a test email.'
# )
# response = sg.send(email)
# print(response.status_code)