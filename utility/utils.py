import os
from django.conf import settings
from keras.models import load_model
import numpy as np
import cv2
from road_damage_notifyapi.models import PotholeDetails
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from threading import Thread


pathToModel=os.path.join(settings.BASE_DIR, 'utility','model')
tf_model=load_model(pathToModel)
CATEGORIES = ['NORMAL', PotholeDetails.Road.POTHOLED, PotholeDetails.Road.UNPAVED]


def process_img(pil_img):
    IMG_SIZE = 128
    img = np.array(pil_img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
    img = np.array(img)
    img = img.reshape(-1,128,128,3)
    return img


def make_frames_from_video(video_path):
  IMG_SIZE = 128
  vidcap = cv2.VideoCapture(video_path)
  video_frames = []

  while True:
    success, frame = vidcap.read()
    if not success:
      break
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = cv2.resize(frame, (IMG_SIZE,IMG_SIZE))
    video_frames.append(frame)
    return video_frames

  cv2.destroyAllWindows()
  vidcap.release()


class EmailThread(Thread):
  def __init__(self, email):
      self.email = email
      Thread.__init__(self)

  def run(self):
      self.email.send()
      print("mail successfully send.")


def send_email(to, **temp_kwargs):
  print("mail is being sending....")

  if temp_kwargs.get("authority"):
    subject = f"Request for Pothole Repair : [{temp_kwargs.get('latitude'), temp_kwargs.get('longitude')}]"
    body_template = render_to_string("pothole_report.html", temp_kwargs)
  else:
    subject = "Request for Pothole Repair Reported"
    body_template = render_to_string("user_response.html", temp_kwargs)

  email = EmailMultiAlternatives(
      subject,
      None,
      settings.EMAIL_HOST_USER,
      [to]
  )
  email.attach_alternative(body_template, 'text/html')
  EmailThread(email).start()
