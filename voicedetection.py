import random
import time
import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone,keywords=None):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("start listening")
        audio = recognizer.listen(source, phrase_time_limit=1.0)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_sphinx(audio, keyword_entries=keywords)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response




# COCO_INSTANCE_CATEGORY_NAMES = [
#     'person', 'traffic light',
#     'bench', 'cat', 'dog', 'umbrella', 'backpack',
#     'handbag', 'bottle', 'cup', 'fork', 'knife', 'spoon', 'bowl',
#     'chair', 'couch', 'potted plant', 'bed', 'dining table',
#     'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
#     'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book',
#     'clock', 'vase', 'scissors', 'hair drier', 'toothbrush'
# ]
COCO_INSTANCE_CATEGORY_NAMES = [
    'person', 'bottle', 'cup', 'potted plant', 'chair', 'potted plant', 'laptop', 'mouse', 'keyboard', 'cell phone'
]
COCO_INSTANCE_CATEGORY_NAMES = [(label, 1.0) for label in COCO_INSTANCE_CATEGORY_NAMES]
print(COCO_INSTANCE_CATEGORY_NAMES)

class Recogniser:
    def __init__(self, device_index=None):
        # create recognizer and mic instances
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=None)
    
    def get_voice_input(self):
        guess = recognize_speech_from_mic(self.recognizer, self.microphone, keywords=COCO_INSTANCE_CATEGORY_NAMES)

        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            return None, None

        # determine if guess is correct and if any attempts remain
        transcript = guess["transcription"]
        print(transcript)
        transcript = transcript.split()
        detected_label = transcript[-1]

        for label, sensitivity in COCO_INSTANCE_CATEGORY_NAMES:
            if label == detected_label:
                return 1, label

        return 0, transcript

if __name__ == "__main__":
    recogniser = Recogniser()
    input()
    print(recogniser.get_voice_input())
    
                



        

        
    

