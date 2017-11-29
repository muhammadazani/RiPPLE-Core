# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

<<<<<<< HEAD


# Create your tests here.
=======
from questions.models import Topic, Distractor, Question, QuestionResponse, QuestionScore, Competency
from questions.services import CompetencyService, QuestionService, SearchService
from users.models import CourseUser
>>>>>>> origin/master

from .common import BootstrapTestCase

<<<<<<< HEAD
class QuestionTestCase(TestCase):
    def _bootstrap_courses(self):
        return Course.objects.create(course_code="test_course_1", course_name="course_name")

    def _bootstrap_topics(self, course):
        [Topic(id=i, name=x, course=course).save()
         for i, x in enumerate(["t1", "t2", "t3", "t4", "t5", "t6"])]

    def _bootstrap_questions(self, author):
        topic_map = [
            Topic.objects.filter(id__in=[1]),
            Topic.objects.filter(id__in=[1, 2]),
            Topic.objects.filter(id__in=[2, 3, 4]),
            Topic.objects.filter(id__in=[4]),
            Topic.objects.filter(id__in=[2, 4])
        ]

        for i in range(0, 5):
            q = Question(
                id=i + 1,
                author=author,
                content="",
                explanation="",
                difficulty=i+1,
                quality=1,
                difficultyCount=1,
                qualityCount=1
            )
            q.save()
            q.topics.set(topic_map[i])

    def _bootstrap_question_choices(self, correct_id):
        question_count = Question.objects.all().count()
        for i in range(0, (4 * question_count)):
            id = i + 1
            Distractor(
                id=id,
                content="question " + str(i),
                response=chr(ord('A') + id % 4),
                isCorrect=id == correct_id,
                question_id=math.ceil(id / 4.0)
            ).save()

    def _bootstrap_user(self, id):
        user = User(id=id, first_name="u_firstname", last_name="u_lastname")
        user.save()
        return user

=======
class QuestionTestCase(BootstrapTestCase):
>>>>>>> origin/master
    def test_answering_new_question_single_topic(self):
        """ New question with single topic """
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)
<<<<<<< HEAD
        # print("FIRST TEST\n")
        # for i in range(0, 20):
        #     QuestionService.respond_to_question(2, author)
        #     print(Competency.objects.all().first().confidence)
        #     print(Competency.objects.all().first().competency)
        #     QuestionService.respond_to_question(3, author)
        #     print(Competency.objects.all().first().competency)

        # for i in range(0, 20):
        #     QuestionService.respond_to_question(2, author)
        #     print(Competency.objects.all().first().competency)

    def test_answering_new_question_multiple_topics(self):
        """ New question with multiple topics """
        course = self._bootstrap_courses()
=======

        QuestionService.respond_to_question(1, author)

        self.assertEqual(QuestionResponse.objects.all().count(), 1)
        user_response = QuestionResponse.objects.first()

        self.assertEqual(user_response.user_id, 1)
        self.assertEqual(user_response.response_id, 1)

        self.assertEqual(QuestionScore.objects.all().count(), 1)
        question_score = QuestionScore.objects.all().first()

        self.assertEqual(question_score.user_id, 1)
        self.assertEqual(question_score.question_id, 1)
        self.assertEqual(question_score.score, -1)

        self.assertEqual(Competency.objects.all().count(), 1)

    def test_answering_new_question_multiple_topics(self):
        """ New question with multiple topics """
        question_number = 3
        # The plus two selects option b by default
        distractor_id = ((question_number - 1) * 4) + 2

        course = self._bootstrap_courses(1)
>>>>>>> origin/master
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
<<<<<<< HEAD
        self._bootstrap_question_choices(correct_id=6)

        print("SECOND TEST\n")

        for i in range(0, 20):
            QuestionService.respond_to_question(5, author)
            print(Competency.objects.all().first().competency)
      
=======
        self._bootstrap_question_choices(correct_id=3)

        topic_count = Distractor.objects.get(id=distractor_id).question.topics.count()

        QuestionService.respond_to_question(distractor_id, author)

        self.assertEqual(QuestionResponse.objects.all().count(), 1)
        user_response = QuestionResponse.objects.first()

        self.assertEqual(user_response.user_id, 1)
        self.assertEqual(user_response.response_id, distractor_id)

        self.assertEqual(QuestionScore.objects.all().count(), 1)
        question_score = QuestionScore.objects.all().first()

        self.assertEqual(question_score.user_id, 1)
        self.assertEqual(question_score.question_id, question_number)
        self.assertEqual(question_score.score, -1)
        #TODO: Ensure competency is updated

    def test_answering_question_correctly(self):
        """ New question with a correct answer """
        question_number = 1
        # The plus two selects option b by default
        distractor_id = ((question_number - 1) * 4) + 2
        correct_id = 2
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id)

        QuestionService.respond_to_question(distractor_id, author)
        question_score = QuestionScore.objects.all().first()

        self.assertEqual(question_score.score, 1)

    def test_answering_question_incorrectly(self):
        """ New question with an incorrect answer """
        question_number = 1
        # The plus two selects option b by default
        distractor_id = ((question_number - 1) * 4) + 2
        correct_id = 3
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id)

        QuestionService.respond_to_question(distractor_id, author)
        question_score = QuestionScore.objects.all().first()

        self.assertEqual(question_score.score, -1)

    def test_answering_multiple_existing_questions(self):
        """ Single user answers multiple questions created by other authors """
        course = self._bootstrap_courses(1)
        self._bootstrap_topics(course)
        number_authors = 3
        #User used for responding
        user = self._bootstrap_user(number_authors + 1)
        responder = CourseUser.objects.create(user = user, course = course)

        #authors
        for i in range(0, number_authors):
            user = self._bootstrap_user(i + 1)
            author = CourseUser.objects.create(user = user, course = course)
            self._bootstrap_questions(author)
            self._bootstrap_question_choices(correct_id = 2)

        questions_answered = 3
        distractors = []
        for i in range(0, questions_answered):
            random_distractor = random.randint(1, Distractor.objects.count())
            QuestionService.respond_to_question(random_distractor, responder)
            distractors.append(random_distractor)

        self.assertEqual(QuestionResponse.objects.all().count(), questions_answered)
        index = 0
        for user_response in QuestionResponse.objects.all():
            self.assertEqual(user_response.user.user_id, responder.user_id)
            self.assertEqual(user_response.response_id, distractors[index])
            index += 1

    def test_answering_multiple_new_questions(self):
        """ Answer multiple questions in a row, 2 incorrect and 1 correctly """
        number_of_questions = 3
        correct_id = 2
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id)

        #set used to store unique topics to ascertain correct number of competencies
        unique_topics = set()

        #Range from 1 as both questions and distractors are id starting at 1
        for question_number in range(1, number_of_questions + 1):
            #picks different distractor for each question based on the question id. Ex Q1 == A
            distractor_id = ((question_number -1) * 4 + question_number)

            QuestionService.respond_to_question(distractor_id, author)
            distractor_object = Distractor.objects.get(pk=distractor_id)

            user_response = QuestionResponse.objects.get(response=distractor_object)
            self.assertEqual(user_response.user_id, 1)
            self.assertEqual(user_response.response_id, distractor_id)

            question_score = QuestionScore.objects.get(pk=distractor_object.question.id)
            self.assertEqual(question_score.user_id, 1)
            self.assertEqual(question_score.question_id, question_number)

            if question_number == correct_id:
                self.assertEqual(question_score.score, 1)
            else:
                self.assertEqual(question_score.score, -1)

            for question_topic in Distractor.objects.get(id=distractor_id).question.topics.all():
                unique_topics.add(question_topic)

        self.assertEqual(QuestionResponse.objects.all().count(), number_of_questions)
        self.assertEqual(QuestionScore.objects.all().count(), number_of_questions)
        #TODO: Ensure competency is updated


    def test_answering_existing_question_many_users(self):
        """ Single question one topic answered by many users """
        course = self._bootstrap_courses(1)
        number_of_responders = 4
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)
        for i in range(1, number_of_responders + 1):
            user = self._bootstrap_user(i+1)
            responder = CourseUser.objects.create(user=user, course=course)
            QuestionService.respond_to_question(i, responder)
        self.assertEqual(QuestionResponse.objects.all().count(), number_of_responders)
        self.assertEqual(QuestionScore.objects.all().count(), number_of_responders)
        response_index = 2
        for user_response in QuestionResponse.objects.all():
            self.assertEqual(user_response.user.user_id, response_index)
            self.assertEqual(user_response.response_id, response_index - 1)
            response_index += 1
        score_index = 2
        for question_score in QuestionScore.objects.all():
            self.assertEqual(question_score.user_id, score_index)
            self.assertEqual(question_score.question_id, 1)
            score_index += 1

    def test_answer_existing_questions_one_user_multiple_times(self):
        """ User different from the author answers same question many times """
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=3)
        responder_user = self._bootstrap_user(2)
        responder = CourseUser.objects.create(user=responder_user, course=course)

        responses_count = 3
        for i in range(0, responses_count):
            QuestionService.respond_to_question(i + 1, responder)

        self.assertEqual(QuestionResponse.objects.all().count(), responses_count)
        self.assertEqual(QuestionScore.objects.all().count(), 1)

        response_index = 1
        for user_response in QuestionResponse.objects.all():
            self.assertEqual(user_response.user_id, 2)
            self.assertEqual(user_response.response_id, response_index)
            response_index+=1

        question_score = QuestionScore.objects.all().first()
        self.assertEqual(question_score.user_id, 2)
        self.assertEqual(question_score.question_id, 1)
        self.assertEqual(question_score.number_answers, responses_count)

    def test_answering_question_different_course(self):
        """ User answers question from course they do not belong to """
        author_course = self._bootstrap_courses(1)
        responder_course = self._bootstrap_courses(2)
        author_user = self._bootstrap_user(1)
        responder_user = self._bootstrap_user(2)
        author = CourseUser.objects.create(user=author_user, course=author_course)
        responder = CourseUser.objects.create(user = responder_user, course = responder_course)
        self._bootstrap_topics(author_course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)

        self.assertRaises(ValueError, QuestionService.respond_to_question, 1, responder)

        self.assertEqual(QuestionResponse.objects.all().count(), 0)
        self.assertEqual(QuestionScore.objects.all().count(), 0)
        self.assertEqual(Competency.objects.all().count(), 0)

    def test_answering_question_with_invalid_response(self):
        """ User answers question with an option that does not exists"""
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)

        self.assertEqual(False, QuestionService.respond_to_question(-1, author))

    def test_getting_question_with_invalid_id(self):
        """ User requests question with an id that does not exist"""
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)

        self.assertEqual(None, QuestionService.get_question(-1))

    def test_questions_available(self):
        """ Only same course questions available to responder """
        author_course = self._bootstrap_courses(1)
        author_user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=author_user, course=author_course)
        self._bootstrap_topics(author_course)
        self._bootstrap_questions(author)

        responder_course = self._bootstrap_courses(2)
        responder_user = self._bootstrap_user(2)
        responder = CourseUser.objects.create(user = responder_user, course = responder_course)
        self._bootstrap_topics(responder_course)
        self._bootstrap_questions(responder, 6)

        self._bootstrap_question_choices(correct_id=2)

        search_query = SearchService.SearchService(responder.course)
        search_result = search_query.execute()

        self.assertEqual(search_result.count(), 5)
>>>>>>> origin/master

    def test_answering_multiple_questions(self):
        # New question with existing items with single topic
        # New question with existing items with multiple topics
        #TODO
        pass

    def test_competency_association(self):
        course = self._bootstrap_courses(1)
        user = self._bootstrap_user(1)
        author = CourseUser.objects.create(user=user, course=course)
        self._bootstrap_topics(course)
        self._bootstrap_questions(author)
        self._bootstrap_question_choices(correct_id=2)

        u = CourseUser.objects.all().first()

        topic_map = [
            Topic.objects.filter(id__in=[1]),
            Topic.objects.filter(id__in=[1, 2]),
            Topic.objects.filter(id__in=[2, 3, 4]),
            Topic.objects.filter(id__in=[4]),
            Topic.objects.filter(id__in=[2, 4])
        ]
        for i in range(0,5):
            c = Competency(
                competency=i,
                confidence=i*10,
                user=u
            )
            c.save()
            c.topics.set(topic_map[i])
            c.save()

        for i in range(0,5):
            c = Competency.objects.get(pk=i+1)
            t = Question.objects.get(pk=i+1).topics.all()

            results = CompetencyService.get_user_competency_for_topics(u, t)

            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].pk, i+1)
