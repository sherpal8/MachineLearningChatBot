import polls.speech_recognition as sr

recognizer = sr.Recognizer()
microphone = sr.Microphone()

def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
     recognizer.adjust_for_ambient_noise(source)
     audio = recognizer.listen(source)
     response = recognizer.recognize_google(audio)
    return response

    

##Original code that came inside the __main__.py contained inside the speech_recognition package (downloaded via pip3)

# import speech_recognition as sr

# r = sr.Recognizer()
# m = sr.Microphone()

# try:
#     print("A moment of silence, please...")
#     with m as source: r.adjust_for_ambient_noise(source)
#     print("Set minimum energy threshold to {}".format(r.energy_threshold))
#     while True:
#         print("Say something!")
#         with m as source: audio = r.listen(source)
#         print("Got it! Now to recognize it...")
#         try:
#             # recognize speech using Google Speech Recognition
#             value = r.recognize_google(audio)

#             # we need some special handling here to correctly print unicode characters to standard output
#             if str is bytes:  # this version of Python uses bytes for strings (Python 2)
#                 print(u"You said {}".format(value).encode("utf-8"))
#             else:  # this version of Python uses unicode for strings (Python 3+)
#                 print("You said {}".format(value))
#         except sr.UnknownValueError:
#             print("Oops! Didn't catch that")
#         except sr.RequestError as e:
#             print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
# except KeyboardInterrupt:
#     pass