# import google.generativeai as genai
# import threading # NEW
# import time # NEW
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import Contact

# def send_ai_reply(instance_id): # NEW: moved logic to separate function
#     try:
#         instance = Contact.objects.get(id=instance_id)
#         if instance.is_auto_replied:
#             return # don't send twice

#         # 1. Generate AI Reply
#         genai.configure(api_key=settings.GEMINI_API_KEY)
#         model = genai.GenerativeModel('gemini-1.5-flash')
        
#         prompt = f"""
#         You are the customer support lead for a professional company. 
#         Your job is to make the client feel heard, valued, and confident in us.

#         Client Details:
#         Name: {instance.name}
#         Subject: {instance.subject}
#         Message: {instance.message}

#         Rules for your reply:
#         1. Start with: "Hi {instance.name},"
#         2. Thank them sincerely for reaching out
#         3. Acknowledge their message: "We understand..."
#         4. Reassure them: "Our team is ready to work with you and we value your trust"
#         5. Tell them a real person has been notified and will follow up soon with details
#         6. Keep tone: Warm, Professional, No jargon, No bad words
#         7. Keep it 4-5 sentences max
#         8. Sign off: "Best regards, The Support Team"
        
#         Only output the email body.
#         """
        
#         response = model.generate_content(prompt)
#         ai_reply = response.text

#         # 2. Send Email
#         send_mail(
#             subject = 'Re: ' + instance.subject,
#             message = ai_reply,
#             from_email = settings.DEFAULT_FROM_EMAIL,
#             recipient_list = [instance.email],
#             fail_silently = False,
#         )
        
#         # 3. Save what we sent
#         instance.is_auto_replied = True
#         instance.ai_reply_text = ai_reply
#         instance.save(update_fields=['is_auto_replied', 'ai_reply_text'])
        
#     except Contact.DoesNotExist:
#         pass
#     except Exception as e:
#         print(f"AI Auto-reply failed: {e}")


# @receiver(post_save, sender=Contact)
# def auto_reply_with_ai(sender, instance, created, **kwargs):
#     if created and not instance.is_auto_replied:
#         # Wait 120 seconds = 2 minutes before running send_ai_reply
#         delay_seconds = 120
#         timer = threading.Timer(delay_seconds, send_ai_reply, args=[instance.id])
#         timer.daemon = True
#         timer.start()
#         print(f"Scheduled AI reply for {instance.email} in 2 minutes")