'''
Created on 01.12.2016

@author: Moustafa Shama
'''
import win32com.client

def send_email(to, subject,  message):
    olMailItem = 0x0
    obj = win32com.client.Dispatch("Outlook.Application")
    newMail = obj.CreateItem(olMailItem)
    newMail.Subject = subject
    newMail.Body = message
    newMail.To = to
    
    #newMail.Attachments.Add(attachment)
    newMail.Send()