from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import UniYear, Skills, Job, CvProject, AdditionalInfo, Post


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'mainpage/home.html')


class BlogPageTest(TestCase):
    title = 'Test title'
    text = 'Test text'
    date = timezone.now

    def setUp(self):
        User.objects.create_superuser('testuser', 'testuser@test.com', 'password')
        self.client.login(username='testuser', password='password')

    def add_post_to_database(self):
        response = self.client.post('/post/new/', data={'author': self.client, 'title': self.title, 'text': self.text,
                                                        'created_date': self.date, 'published_date': self.date})
        self.assertEqual(response.status_code, 302)

    def edit_post_in_database(self, title, text, pk):
        response = self.client.post('/post/' + str(pk) + '/edit/',
                                    data={'author': self.client, 'title': title, 'text': text,
                                          'created_date': self.date, 'published_date': self.date})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/post/' + str(pk) + '/')

    def check_post_saved_correctly(self, title, text):
        response = self.client.get('/blog').content.decode()
        self.assertIn(title, response)
        self.assertIn(text, response)

    def test_add_post_page_returns_correct_html(self):
        response = self.client.get('/post/new/')
        self.assertTemplateUsed(response, 'blog/post_edit.html')

    def test_can_add_post(self):
        self.add_post_to_database()
        self.check_post_saved_correctly(self.title, self.text)

    def test_post_page_returns_correct_html(self):
        self.add_post_to_database()
        response = self.client.get('/post/1/')
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_edit_post_page_returns_correct_html(self):
        self.add_post_to_database()
        response = self.client.get('/post/1/edit/')
        self.assertTemplateUsed(response, 'blog/post_edit.html')

    def test_edit_post_saves_changes(self):
        extra_text = 'blarg'
        self.add_post_to_database()
        self.edit_post_in_database(self.title, self.text + extra_text, 1)
        self.check_post_saved_correctly(self.title, self.text + extra_text)

    def test_can_delete_post(self):
        self.add_post_to_database()
        self.client.post('/post/1/delete/')
        response = self.client.get('/blog').content.decode()
        self.assertNotIn(self.title, response)
        self.assertNotIn(self.text, response)

    def test_edu_num_database_entries_correct(self):
        extra_text = ' yes'
        self.assertEqual(Post.objects.count(), 0)
        self.add_post_to_database()
        self.assertEqual(Post.objects.count(), 1)
        self.edit_post_in_database(self.title, self.text + extra_text, 1)
        self.assertEqual(Post.objects.count(), 1)
        self.client.post('/post/1/delete/')
        self.assertEqual(Post.objects.count(), 0)


class CvEduSectionTest(TestCase):
    year = 'First Year'
    grades = 'Many good grades yes yes'
    overall_grade = 'Best grade yes yes'

    def setUp(self):
        User.objects.create_superuser('testuser', 'testuser@test.com', 'password')
        self.client.login(username='testuser', password='password')

    def add_year_to_database(self, year, grades, overall_grade):
        response = self.client.post('/cv/edu/new/',
                                    data={'year': year, 'grades': grades, 'overall_grade': overall_grade})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/cv')

    def edit_year_in_database(self, year, grades, overall_grade, pk):
        response = self.client.post('/cv/edu/' + str(pk) + '/',
                                    data={'year': year, 'grades': grades, 'overall_grade': overall_grade})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/cv')

    def check_year_saved_correctly(self, year, grades, overall_grade):
        response = self.client.get('/cv').content.decode()
        self.assertIn(year, response)
        self.assertIn(grades, response)
        self.assertIn(overall_grade, response)

    def test_cv_page_returns_correct_html(self):
        response = self.client.get('/cv')
        self.assertTemplateUsed(response, 'cv/cv_home.html')

    def test_add_year_page_returns_correct_html(self):
        response = self.client.get('/cv/edu/new/')
        self.assertTemplateUsed(response, 'cv/edu_edit.html')

    def test_add_year_page_can_save_POST_request(self):
        self.add_year_to_database(self.year, self.grades, self.overall_grade)
        self.check_year_saved_correctly(self.year, self.grades, self.overall_grade)

    def test_edit_year_page_returns_correct_html(self):
        self.add_year_to_database(self.year, self.grades, self.overall_grade)
        response = self.client.get('/cv/edu/1/')
        self.assertTemplateUsed(response, 'cv/edu_edit.html')

    def test_edit_year_page_makes_changes(self):
        extra_text = ' yes'
        self.add_year_to_database(self.year, self.grades, self.overall_grade)
        self.edit_year_in_database(self.year, self.grades + extra_text, self.overall_grade, 1)
        self.check_year_saved_correctly(self.year, self.grades + extra_text, self.overall_grade)

    def test_edu_num_database_entries_correct(self):
        extra_text = ' yes'
        self.assertEqual(UniYear.objects.count(), 0)
        self.add_year_to_database(self.year, self.grades, self.overall_grade)
        self.assertEqual(UniYear.objects.count(), 1)
        self.edit_year_in_database(self.year, self.grades + extra_text, self.overall_grade, 1)
        self.assertEqual(UniYear.objects.count(), 1)


class CvSkillsSectionTest(TestCase):
    skills_col_1 = 'Many many skills to be had here'
    skills_col_2 = 'Even more over this side'

    def setUp(self):
        User.objects.create_superuser('testuser', 'testuser@test.com', 'password')
        self.client.login(username='testuser', password='password')

    def add_skills_to_database(self, skills_col_1, skills_col_2):
        response = self.client.post('/cv/skills/',
                                    data={'first_col': skills_col_1, 'second_col': skills_col_2})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/cv')

    def edit_skills_in_database(self, skills_col_1, skills_col_2):
        response = self.client.post('/cv/skills/',
                                    data={'first_col': skills_col_1, 'second_col': skills_col_2})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/cv')

    def check_skills_saved_correctly(self, skills_col_1, skills_col_2):
        response = self.client.get('/cv').content.decode()
        self.assertIn(skills_col_1, response)
        self.assertIn(skills_col_2, response)

    def test_skills_page_returns_correct_html(self):
        response = self.client.get('/cv/skills/')
        self.assertTemplateUsed(response, 'cv/skills_edit.html')

    def test_skills_page_can_save_POST_request(self):
        self.add_skills_to_database(self.skills_col_1, self.skills_col_2)
        self.check_skills_saved_correctly(self.skills_col_1, self.skills_col_2)

    def test_skills_page_can_edit_previous_entry(self):
        extra_text = ' yes'
        self.add_skills_to_database(self.skills_col_1, self.skills_col_2)
        self.edit_skills_in_database(self.skills_col_1 + extra_text, self.skills_col_2)
        self.check_skills_saved_correctly(self.skills_col_1 + extra_text, self.skills_col_2)

    def test_skills_num_database_entries_correct(self):
        extra_text = ' yes'
        self.assertEqual(Skills.objects.count(), 0)
        self.add_skills_to_database(self.skills_col_1, self.skills_col_2)
        self.assertEqual(Skills.objects.count(), 1)
        self.edit_skills_in_database(self.skills_col_1 + extra_text, self.skills_col_2)
        self.assertEqual(Skills.objects.count(), 1)


class CvJobSectionTest(TestCase):
    job_title = 'Tea taster'
    job_location = 'Trusty Teapot, Teatown'
    job_date = 'August 2019 - Now'
    job_description = 'Tasted lots of tea, gained a new appreciation for teas other than yorkshire tea gold!'

    def setUp(self):
        User.objects.create_superuser('testuser', 'testuser@test.com', 'password')
        self.client.login(username='testuser', password='password')

    def add_job_to_database(self, title, location, date, description):
        response = self.client.post('/cv/job/new/',
                                    data={'title': title, 'location': location, 'date': date,
                                          'description': description})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/cv')

    def edit_job_in_database(self, title, location, date, description, pk):
        response = self.client.post('/cv/job/' + str(pk) + '/',
                                    data={'title': title, 'location': location, 'date': date,
                                          'description': description})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/cv')

    def check_job_saved_correctly(self, title, location, date, description):
        response = self.client.get('/cv').content.decode()
        self.assertIn(title, response)
        self.assertIn(location, response)
        self.assertIn(date, response)
        self.assertIn(description, response)

    def test_job_page_returns_correct_html(self):
        response = self.client.get('/cv/job/new/')
        self.assertTemplateUsed(response, 'cv/job_edit.html')

    def test_edit_job_page_returns_correct_html(self):
        self.add_job_to_database(self.job_title, self.job_location, self.job_date, self.job_description)
        response = self.client.get('/cv/job/1/')
        self.assertTemplateUsed(response, 'cv/job_edit.html')

    def test_job_page_can_save_POST_request(self):
        self.add_job_to_database(self.job_title, self.job_location, self.job_date, self.job_description)
        self.check_job_saved_correctly(self.job_title, self.job_location, self.job_date, self.job_description)

    def test_job_page_can_edit_previous_entry(self):
        extra_text = ' best job yes yes'
        self.add_job_to_database(self.job_title, self.job_location, self.job_date, self.job_description)
        self.edit_job_in_database(self.job_title, self.job_location, self.job_date, self.job_description + extra_text,
                                  1)
        self.check_job_saved_correctly(self.job_title, self.job_location, self.job_date,
                                       self.job_description + extra_text)

    def test_job_num_database_entries_correct(self):
        extra_text = ' best job yes yes'
        self.assertEqual(Job.objects.count(), 0)
        self.add_job_to_database(self.job_title, self.job_location, self.job_date, self.job_description + extra_text)
        self.assertEqual(Job.objects.count(), 1)
        self.edit_job_in_database(self.job_title, self.job_location, self.job_date, self.job_description + extra_text,
                                  1)
        self.assertEqual(Job.objects.count(), 1)


class CvProjectSectionTest(TestCase):
    project_title = 'This Website'
    project_date = 'May 2020 - Present'
    project_description = 'Built the website using the Django framework for coursework set by uni'

    def setUp(self):
        User.objects.create_superuser('testuser', 'testuser@test.com', 'password')
        self.client.login(username='testuser', password='password')

    def add_project_to_database(self, title, date, description):
        response = self.client.post('/cv/project/new/',
                                    data={'title': title, 'date': date,
                                          'description': description})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/cv')

    def edit_project_in_database(self, title, date, description, pk):
        response = self.client.post('/cv/project/' + str(pk) + '/',
                                    data={'title': title, 'date': date,
                                          'description': description})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/cv')

    def check_project_saved_correctly(self, title, date, description):
        response = self.client.get('/cv').content.decode()
        self.assertIn(title, response)
        self.assertIn(date, response)
        self.assertIn(description, response)

    def test_project_page_returns_correct_html(self):
        response = self.client.get('/cv/project/new/')
        self.assertTemplateUsed(response, 'cv/cv_project_edit.html')

    def test_edit_project_page_returns_correct_html(self):
        self.add_project_to_database(self.project_title, self.project_date, self.project_description)
        response = self.client.get('/cv/project/1/')
        self.assertTemplateUsed(response, 'cv/cv_project_edit.html')

    def test_project_page_can_save_POST_request(self):
        self.add_project_to_database(self.project_title, self.project_date, self.project_description)
        self.check_project_saved_correctly(self.project_title, self.project_date, self.project_description)

    def test_project_page_can_edit_previous_entry(self):
        extra_text = ' best project yes yes'
        self.add_project_to_database(self.project_title, self.project_date, self.project_description)
        self.edit_project_in_database(self.project_title, self.project_date,
                                      self.project_description + extra_text, 1)
        self.check_project_saved_correctly(self.project_title, self.project_date, self.project_description + extra_text)

    def test_project_num_database_entries_correct(self):
        extra_text = ' best project yes yes'
        self.assertEqual(CvProject.objects.count(), 0)
        self.add_project_to_database(self.project_title, self.project_date, self.project_description + extra_text)
        self.assertEqual(CvProject.objects.count(), 1)
        self.edit_project_in_database(self.project_title, self.project_date, self.project_description + extra_text, 1)
        self.assertEqual(CvProject.objects.count(), 1)


class CvAdditionalInfoSectionTest(TestCase):
    text = 'Lots of additional information here'

    def setUp(self):
        User.objects.create_superuser('testuser', 'testuser@test.com', 'password')
        self.client.login(username='testuser', password='password')

    def add_additional_info_to_database(self, text):
        response = self.client.post('/cv/additional_info/',
                                    data={'text': text})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/cv')

    def edit_additional_info_in_database(self, text):
        response = self.client.post('/cv/additional_info/',
                                    data={'text': text})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/cv')

    def check_additional_info_saved_correctly(self, text):
        response = self.client.get('/cv').content.decode()
        self.assertIn(text, response)
        self.assertIn(text, response)

    def test_additional_info_page_returns_correct_html(self):
        response = self.client.get('/cv/additional_info/')
        self.assertTemplateUsed(response, 'cv/additional_info_edit.html')

    def test_additional_info_page_can_save_POST_request(self):
        self.add_additional_info_to_database(self.text)
        self.check_additional_info_saved_correctly(self.text)

    def test_additional_info_page_can_edit_previous_entry(self):
        extra_text = ' yes'
        self.add_additional_info_to_database(self.text)
        self.edit_additional_info_in_database(self.text + extra_text)
        self.check_additional_info_saved_correctly(self.text + extra_text)

    def test_additional_info_num_database_entries_correct(self):
        extra_text = ' yes'
        self.assertEqual(AdditionalInfo.objects.count(), 0)
        self.add_additional_info_to_database(self.text)
        self.assertEqual(AdditionalInfo.objects.count(), 1)
        self.edit_additional_info_in_database(self.text + extra_text)
        self.assertEqual(AdditionalInfo.objects.count(), 1)
