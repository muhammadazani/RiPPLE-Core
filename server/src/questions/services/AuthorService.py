from ..models import Question, Topic, Distractor, QuestionRating, QuestionResponse, Competency, CompetencyMap, QuestionImage, ExplanationImage, DistractorImage
from django.db import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.conf import settings
from ripple.util import util
from bs4 import BeautifulSoup
import base64
import imghdr


def add_question(question_request, host, user):
    explanation = question_request.get("explanation", None)
    question = question_request.get("question", None)
    responses = question_request.get("responses", None)
    topics = question_request.get("topics", None)

    if explanation is None or question is None or responses is None or topics is None:
        return {"state": "Error", "error": "Invalid Question"}
    for i in ["A", "B", "C", "D"]:
        if responses.get(i, None) is None:
            return {"state": "Error", "error": "Missing response " + i}

    # Question
    questionObj = Question(
        content=question.get("content", None),
        explanation=explanation.get("content", None),
        difficulty=0,
        quality=0,
        difficultyCount=0,
        qualityCount=0,
        author=user
    )
    if (verifyContent(questionObj.content) and verifyContent(questionObj.explanation)):
        questionObj.save()
    else:
        # INVALID CONTENT
        return {"state": "Error", "error": "Invalid Question"}
    try:
        with transaction.atomic():
            # Question Images
            images = question.get("payloads", None)
            if images:
                if not decodeImages(str(questionObj.id), images, "q", host):
                    raise IntegrityError("Invalid Question Image")

            # Explanation Images
            images = explanation.get("payloads", None)
            if images:
                if not decodeImages(str(questionObj.id), images, "e", host):
                    raise IntegrityError("Invalid Explanation Image")

            # Topics
            topicList = []
            for i in topics:
                topicList.append(i.get("id", None))
            questionObj.topics = topicList

            # Distractors
            for i in ["A", "B", "C", "D"]:
                distractor = Distractor(
                    content=responses[i].get("content", None),
                    isCorrect=responses[i].get("isCorrect", None),
                    response=i,
                    question=questionObj
                )

                if verifyContent(distractor.content):
                    distractor.save()
                else:
                    raise IntegrityError("Invalid Distractor")

                # Distractor Images
                images = responses[i].get("payloads", None)
                if images:
                    if not decodeImages(str(distractor.id), images, "d", host):
                        raise IntegrityError("Invalid Distractor Image")
    except IntegrityError as e:
        return {"state": "Error", "error": str(e)}
    except Exception as e:
        return {"state": "Error", "error": str(e)}

    return {"state": "Question Added", "question": Question.objects.get(pk=questionObj.id).toJSON()}


def decodeImages(image_id, images, image_type, host):
    # type q=question, d=distractor, e=explanation
    urls = []
    database_image_types = {
        "q": QuestionImage,
        "d": DistractorImage,
        "e": ExplanationImage
    }
    ImageToSaveClass = database_image_types.get(image_type, None)

    if image_type == "q" or image_type == "e":
        reference = Question.objects.get(pk=image_id)
    else:
        reference = Distractor.objects.get(pk=image_id)

    for i, image in images.items():
        contentfile_image = util.save_image(image, image_id)
        if contentfile_image is None:
            raise IntegrityError("Image is not of valid type")

        # Question + Explanation in the same object
        if image_type == "q" or image_type == "e":
            new_image = ImageToSaveClass.objects.create(question=reference, image=contentfile_image)
        else:
            new_image = ImageToSaveClass.objects.create(distractor=reference, image=contentfile_image)
        urls.append(new_image.image.name)

    if image_type == "e":
        reference.explanation = newSource(urls, reference.explanation, host)
    else:
        reference.content = newSource(urls, reference.content, host)

    reference.save()
    return True


def newSource(urls, content, host):
    soup = BeautifulSoup(content, "html.parser")

    images = soup.find_all('img')
    for i in range(0, len(urls)):
        images[i]['src'] = "//" + host + urls[i]
        images[i]['src'] = util.merge_url_parts([host, urls[i]])

    immediate_children = soup.findChildren(recursive=False)
    return ''.join([str(x) for x in immediate_children])


def verifyContent(content):
    if len(content) == 0:
        return False

    soup = BeautifulSoup(content, "html.parser")

    scripts = soup.find_all('script')
    if len(scripts) > 0:
        return False
    return True
