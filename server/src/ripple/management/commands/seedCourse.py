from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import IntegrityError, transaction
from django.core.files.base import ContentFile
from questions.models import Topic, Question, Distractor, QuestionResponse, QuestionRating, Competency, QuestionImage,\
    ExplanationImage, DistractorImage, ReportReason
from users.models import Course, User, CourseUser, Engagement, ConsentForm, Role
from recommendations.models import Day, Time, Availability, StudyRole, AvailableRole
from base64 import b64decode
import imghdr
import sys

from questions.services import QuestionService
from users.services import UserService

from random import randint, randrange, sample, choice
from datetime import datetime
from faker import Factory
fake = Factory.create()

import json
from bs4 import BeautifulSoup
import base64
import imghdr
from ripple.util import util
from django.conf import settings

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


def chance(n):
    return choice(range(n)) is n - 1

def _format(x):
    if len(x) == 0: return x
    return (x + "/") if x[-1] != "/" else x

def merge_url_parts(parts, url=""):
    if len(parts) == 0:
        return url
    return merge_url_parts(parts, urljoin(url, parts.pop(0)))


def make_question_responses(user, correct, incorrect, ability):
    if chance(2):
        user_choice = choose_answer(correct, incorrect, ability)
        response = QuestionService.respond_to_question(user_choice.id,user)

        if chance(2):
            rating = QuestionRating(
                quality=randrange(0, 10),
                difficulty=randrange(0, 10),
                response=user_choice,
                user=user
            )
            rating.save()


def choose_answer(correct, incorrect, ability):
    #Will be used with chance to get 33% probability of answering correctly
    lowPercentage = 3
    #Will be used with not chance to get 75% probability of answering correctly
    mediumPercentage = 4
    #Will be used with not chance to get 90% probability of answering correctly
    highPercentage = 10
    if (ability == "low" and chance(lowPercentage)):
        user_choice = choice(correct)
    elif (ability == "medium" and not chance(mediumPercentage)):
        user_choice = choice(correct)
    elif (ability == "high" and not chance(highPercentage)):
        user_choice = choice(correct)
    else:
        user_choice = choice(incorrect)
    return user_choice


def get_topics(file):
    with open(file) as data_file:
        data = json.load(data_file)
    return data["topics"]


def parse_questions(file, course_users, all_topics, host):
    host = merge_url_parts([
        _format(host),
        _format("static")
    ])
    distractors = []

    with open(file) as data_file:
        data = json.load(data_file)

    questions = data["questions"]
    counter = 0
    for q in questions:
        try:
            with transaction.atomic():
                distractor_count = 0
                counter = counter+1
                if q["explanation"]["content"] is None:
                        q["explanation"]["content"] = " "

                question = Question(
                    content = q["question"]["content"],
                    explanation = q["explanation"]["content"],
                    difficulty = randrange(0, 5),
                    quality = randrange(0, 5),
                    difficultyCount = randrange(0, 100),
                    qualityCount = randrange(0, 100),
                    author = choice(course_users)
                )
                question.save()
                d = decode_images(question.id, question, q["question"]["payloads"], "q", host)
                if not d:
                    raise IntegrityError("Invalid Question Image")
                d = decode_images(question.id, question, q["explanation"]["payloads"], "e", host)
                if not d:
                    raise IntegrityError("Invalid Explanation Image")

                q_topics = q["topics"]
                for topic in q_topics:
                    idx = 0
                    while idx < len(all_topics):
                        if topic["name"] == all_topics[idx].name:
                            break
                        idx+=1
                    question.topics.add(all_topics[idx])
                question.save()

                _response_choices = ["A", "B", "C", "D"]
                if True not in [q["responses"][i].get("isCorrect", False) for i in _response_choices]:
                    raise IntegrityError("No correct answer for question")

                for i in _response_choices:
                    response = q["responses"][i]
                    if response["content"] is None:
                        response["content"] = " "
                    distractor = Distractor(
                        content = response["content"],
                        response = i,
                        isCorrect = response["isCorrect"],
                        question = question
                    )
                    distractor.save()
                    distractor_count+=1
                    d = decode_images(distractor.id, distractor, response["payloads"],"d", host)
                    if not d:
                        raise IntegrityError("Invalid Distractor Image")
                    distractors.append(distractor)
        except IntegrityError as e:
            distractors=distractors[:len(distractors)-distractor_count]
            print("Invalid question: " + str(counter))

    return distractors

def decode_images(image_id, obj, images, image_type, host):
    if len(images) == 0:
        return True
    # objType q=question, d=distractor
    urls = []
    database_image_types = {
        "q": QuestionImage,
        "d": DistractorImage,
        "e": ExplanationImage
    }
    ImageToSaveClass = database_image_types.get(image_type, None)

    for i, image in images.items():
        contentfile_image = save_image_course_seeder(image, image_id)
        if contentfile_image is None:
            return False
        # Question + Explanation in the same object
        if image_type == "q" or image_type == "e":
            new_image = ImageToSaveClass.objects.create(question=obj, image=contentfile_image)
        else:
            new_image = ImageToSaveClass.objects.create(distractor=obj, image=contentfile_image)
        urls.append(new_image.image.name)

    if image_type == "e":
        obj.explanation = newSource(urls, obj.explanation, host)
    else:
        obj.content = newSource(urls, obj.content, host)

    obj.save()
    return True

def newSource(urls, content, host):
    soup = BeautifulSoup(content, "html.parser")

    images = soup.find_all('img')
    for i in range(0, len(urls)):
        if urls[i] is None:
            continue
        images[i]['src'] = util.merge_url_parts([host, urls[i]])

    immediate_children = soup.findChildren(recursive=False)
    return ''.join([str(x) for x in immediate_children])

def make_days():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for x in days:
        if len(Day.objects.filter(day=x)) == 0:
            day = Day.objects.create(day=x)
            day.save()

def make_times(times):
    for i in range(len(times) - 1):
        if len(Time.objects.filter(start=times[i], end=times[i + 1])) == 0:
            time_range = Time.objects.create(start=times[i], end=times[i + 1])
            time_range.save()

def make_study_roles():
    study_roles = [
    {"role": "mentor", "description": "Provide Mentorship"},
    {"role": "mentee", "description": "Seek Mentorship"},
    {"role": "partner", "description": "Find Study Partners"}]

    for x in study_roles:
        study_role = StudyRole.objects.create(role=x["role"], description=x["description"])
        study_role.save()

class Command(BaseCommand):
    args = ''
    help = 'Populates the Questions database using a question set in a JSON file'

    def add_arguments(self, parser):
        parser.add_argument("--name", nargs="+")
        parser.add_argument("--course", nargs="+")
        parser.add_argument("--file", nargs="+")
        parser.add_argument("--host")

    def handle(self, *args, **options):
        if(len(options["name"])!=len(options["course"]) or len(options["name"])!=len(options["file"])):
            print("Please ensure you have a course code, name and file for each course")
            sys.exit(1)

        course_names = options["name"]
        course_ids = options["course"]
        course_files = options["file"]
        host = options["host"]

        def populate_course(file, topics, course, users):
            #Add an admin user for each course
            (admin, created) = CourseUser.objects.get_or_create(user=users[0], course=course)
            (role, created) = Role.objects.get_or_create(role = "Instructor")
            admin.roles.add(role)

            all_topics = []
            for x in topics:
                topic = Topic.objects.create(name=x)
                topic.course.add(course)
                all_topics.append(topic)

            print("\t-Enrolling Users")
            course_users = []
            for user in users:
                if chance(2):
                    course_users.append(
                        CourseUser.objects.get_or_create(user=user, course=course)[0])

            print("\t-Making Questions")
            distractors = parse_questions(file, course_users, all_topics, host)
            correct_distractors = []
            incorrect_distractors = []
            for item in distractors:
                if (item.isCorrect):
                    correct_distractors.append(item)
                else:
                    incorrect_distractors.append(item)

            print("\t-Answering and Rating Questions")
            abilities = ["low", "medium", "high"]
            index = 1
            for user in course_users:
                studentAbility = abilities[choice(range(3))]
                print("\t-Answering Course User:" + str(index) + " Questions")
                index += 1
                for i in range(0, 100):
                    make_question_responses(user, correct_distractors, incorrect_distractors, studentAbility)

        def populate_availability(course_users, days, times):
            for i in range(len(course_users)):
                course_user = course_users[i]
                for j in range(randint(3, 10)):
                    random_day = Day.objects.get(pk=randint(1, len(days)))
                    random_time = Time.objects.get(pk=randint(1, len(times)))
                    # Add availability
                    availability = Availability.objects.create(course_user=course_user, day=random_day, time=random_time)

        def populate_available_roles(course_users, study_roles):
            for course_user in course_users:
                topics = Topic.objects.filter(course=course_user.course)
                for topic in topics:
                    role_id = randint(0, 1)
                    if role_id > 0:
                        study_role = study_roles[1]
                        availableRole = AvailableRole.objects.create(course_user=course_user, topic=topic, study_role=study_role)

                    role_id = randint(0, 1)
                    if role_id:
                        study_role = study_roles[2]
                        availableRole = AvailableRole.objects.create(course_user=course_user, topic=topic, study_role=study_role)

        courses = []
        for i in range(0,len(course_names)):
            courses.append({"courseID": course_ids[i], "courseName": course_names[i], "courseCode": course_names[i], 
                "courseSem": "Semester " + str(randint(1,2)) + " 2018", "courseFile": course_files[i]})

        users = [User.objects.create(user_id=user_id, first_name=fake.first_name(), last_name=fake.last_name(), image=util.merge_url_parts([host, "static/default_images/"+str(user_id)+".jpg"]))
                 for user_id in range(50)]

        all_courses = [UserService.insert_course_if_not_exists({
            "course_id": x["courseID"],
            "course_code": x["courseCode"],
            "course_name": x["courseName"],
            "course_sem": x["courseSem"]}, users[0]) for x in courses]

        for i in range(0,len(all_courses)):
            print("Populating Course: " + all_courses[i].course_code)
            unique_topics = get_topics(courses[i]["courseFile"])
            populate_course(courses[i]["courseFile"], unique_topics, all_courses[i], users)

        print("Populating Availabilities")
        print("\t-Making Days")
        make_days()

        print("\t-Making Times")
        time_inputs = [datetime(2017, 11, 6, hour, 0).time() for hour in range(0, 24)]
        time_inputs.append(datetime(2017, 11, 7, 0, 0).time())
        make_times(time_inputs)

        print("\t-Making Study Roles")
        make_study_roles()

        course_users = CourseUser.objects.all()
        days = Day.objects.all()
        times = Time.objects.all()
        print("\t-Populating Availabilities")
        populate_availability(course_users, days, times)
        study_roles = StudyRole.objects.all()
        print("\t-Populating Study Roles")
        populate_available_roles(course_users, study_roles)

def save_image_course_seeder(encoded_image, image_id):
    image_format, base64_payload = encoded_image.split(';base64,')
    ext = image_format.split('/')[-1]
    data = ContentFile(b64decode(base64_payload),
                       name="")
    if imghdr.what(data) is not None:
        data.name = "u"+str(image_id)+"."+imghdr.what(data)
    else:
        return None

    return data
