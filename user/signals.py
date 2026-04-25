from django.db.models.signals import pre_save , post_save
from django.dispatch import receiver
from user.models import UserInfo
from django.core.mail import EmailMessage
from django.conf import settings

@receiver(post_save,sender=UserInfo)
def welcome_email(sender, instance, created, **kwargs):
    if created:
      subject='Registration Successful 🎓'
      html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            
            <body style="margin:0; padding:0; background:#141414; font-family:Arial, sans-serif;">
            
            <div style="max-width:500px; margin:auto; background:#1b1b1b; border-radius:10px; overflow:hidden;">
            
                <!-- HEADER -->
                <div style="background:#e65100; color:white; text-align:center; padding:15px; font-size:20px; font-weight:bold;">
                    JOSHI'S FIRST STEP
                </div>
            
                <!-- CONTENT -->
                <div style="padding:20px; color:#ffffff; font-size:15px; line-height:1.6;">
            
                    <p>Hi {instance.Name},</p>
            
                    <p>Welcome to <b>Joshi's First Step</b>.</p>
            
                    <p>Your account has been successfully created.</p>
            
                    <p><b>You can now:</b></p>
            
                    <ul style="padding-left:18px;">
                        <li>Explore admission process</li>
                        <li>Get instant answers via our chatbot</li>
                        <li>Contact us for assistance</li>
                    </ul>
            
                    <!-- BUTTON -->
                    <a href="https://www.joshifirststep.page/"
                       style="display:block; text-align:center; background:#e65100; color:white;
                              padding:10px; text-decoration:none; border-radius:5px; margin-top:15px;">
                        Visit Website
                    </a>
            
                    <p style="margin-top:20px;">
                        If you need help, simply reply to this email or use our chatbot.
                    </p>
            
                    <p>
                        <b>Best regards,</b><br>
                        School Team<br>
                        📞 +91-9988820977
                    </p>
            
                </div>
            
                <!-- FOOTER -->
                <div style="background:#111; text-align:center; color:#aaa; padding:10px; font-size:12px;">
                    © Joshi's First Step School
                </div>
            
            </div>
            
            </body>
            </html>
          """
      email=EmailMessage(
         subject,
         html_content,
         settings.EMAIL_HOST_USER,
         [instance.email],
        )
      email.content_subtype = "html"
      email.send()
      


      