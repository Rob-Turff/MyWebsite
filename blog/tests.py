from django.test import TestCase
from .models import UniYear


class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'mainpage/home.html')


class CvEduSectionTest(TestCase):
    year = 'First Year'
    grades = 'Many good grades yes yes'
    overall_grade = 'Best grade yes yes'

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
    def add_skills_to_database(self,  skills_col_1,  skills_col_2):
        response = self.client.post('/cv/skills/',
                                    data={'first_col': skills_col_1, 'second_col': skills_col_2})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/cv')

    def edit_skills_in_database(self,  skills_col_1,  skills_col_2):
        response = self.client.post('/cv/skills/',
                                    data={'first_col': skills_col_1, 'second_col': skills_col_2})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/cv')

    def check_skills_saved_correctly(self,  skills_col_1,  skills_col_2):
        response = self.client.get('/cv').content.decode()
        self.assertIn(skills_col_1, response)
        self.assertIn(skills_col_2, response)

    def test_skills_page_returns_correct_html(self):
        response = self.client.get('/cv/skills/')
        self.assertTemplateUsed(response, 'cv/skills.html')

    def test_skills_page_can_save_POST_request(self):
        self.add_year_to_database(self.skills_col_1, self.skills_col_2)
        self.check_year_saved_correctly(self.skills_col_1, self.skills_col_2)

    def test_skills_page_can_edit_previous_entry(self):
        extra_text = ' yes'
        self.add_year_to_database(self.skills_col_1, self.skills_col_2)
        self.edit_year_in_database(self.skills_col_1 + extra_text, self.skills_col_2)
        self.check_year_saved_correctly(self.skills_col_1 + extra_text, self.skills_col_2)

    def test_skills_num_database_entries_correct(self):
        extra_text = ' yes'
        self.assertEqual(Skills.objects.count(), 0)
        self.add_year_to_database(self.skills_col_1, self.skills_col_2)
        self.assertEqual(Skills.objects.count(), 1)
        self.edit_year_in_database(self.skills_col_1 + extra_text, self.skills_col_2)
        self.assertEqual(Skills.objects.count(), 1)

