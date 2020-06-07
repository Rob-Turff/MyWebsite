import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.test import Client
from selenium import webdriver

from selenium.webdriver.common.keys import Keys


class AdminUserTests(StaticLiveServerTestCase):
    def setUp(self):
        self.adminAccount = User.objects.create_superuser('testuser', 'testuser@test.com', 'password')
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def login_to_admin_page(self):
        self.browser.get(self.live_server_url + '/admin/login/?next=/admin/')
        # Dave types in the admin credentials
        usernameField = self.browser.find_element_by_id('id_username')
        usernameField.send_keys(self.adminAccount.username)
        passwordField = self.browser.find_element_by_id('id_password')
        passwordField.send_keys('password')
        passwordField.send_keys(Keys.ENTER)
        time.sleep(0.25)

    def test_can_add_edit_and_view_blog_posts(self):
        # Dave decides he wants to be the most powerful being in the universe
        # and so opens and logs into the admin login page
        self.login_to_admin_page()
        # Dave checks that he is now all powerful
        self.assertIn('Site administration | Django site admin', self.browser.title)
        # Dave navigates back to the home page of the website
        self.browser.get(self.live_server_url)
        # Dave, being an absolutely spiffing individual decides that he wants to make a post about yorkshire tea gold
        # and so presses the blog button in the top navigation bar
        self.browser.find_element_by_id('topnav-blog-button').click()
        # He then checks the title of the page to make sure he is the right place because Dave hasn't had his
        # standard 15 cups of tea today and so is being extra careful
        self.assertIn('Blog | Robert Turff', self.browser.title)
        # Now Dave is sure he is on the right page he presses the button to add a new blog post
        self.browser.find_element_by_id('new-post-button').click()
        # Dave immediately checks the heading on the page ensuring that his tea deprived mind hasn't made any mistakes
        headerText = self.browser.find_element_by_tag_name('h2')
        self.assertIn('New post', headerText.text)
        # Dave enters the title "One tea to rule them all"
        titleInput = self.browser.find_element_by_id('id_title')
        title = 'One tea to rule them all'
        titleInput.send_keys(title)
        # Dave enters the text "One tea to rule them all, One man to find them, One mug to
        # bring them all and in the darkness bind them" and then clicks the save button
        textInput = self.browser.find_element_by_id('id_text')
        text = 'One tea to rule them all, One man to find them, One mug to bring them all and in the darkness bind them'
        textInput.send_keys(text)
        self.browser.find_element_by_class_name('save').click()
        time.sleep(0.25)
        # Happy that he put his thoughts down on a page Dave reviewed what he had written
        postTitle = self.browser.find_element_by_tag_name('h2')
        self.assertIn(title, postTitle.text)
        pText = self.browser.find_elements_by_tag_name('p')
        self.assertIn(text, pText[1].text)
        # Dave decided he wanted to add ... to the end of the post text
        self.browser.find_element_by_id('edit-post-button').click()
        titleInput = self.browser.find_element_by_id('id_title')
        self.assertIn(titleInput.text, title)
        textInput = self.browser.find_element_by_id('id_text')
        self.assertIn(textInput.text, text)
        textInput.send_keys('...')
        self.browser.find_element_by_class_name('save').click()
        time.sleep(0.25)
        # He then goes back to the main blog page to admire his masterwork
        self.browser.find_element_by_id("topnav-blog-button").click()
        titlesOnPage = self.browser.find_elements_by_tag_name('h2')
        self.assertTrue(any(title in t.text for t in titlesOnPage))
        pTextOnPage = self.browser.find_elements_by_tag_name('p')
        self.assertTrue(any(text in t.text for t in pTextOnPage))

    def test_can_navigate_to_cv_page_and_edit_it(self):
        # Dave decides he wants to be the most powerful being in the universe
        # and so opens and logs into the admin login page
        self.login_to_admin_page()
        # Dave navigates back to the home page of the website
        self.browser.get(self.live_server_url)
        # During one of Daves many tea induced fever dreams he has learned some new skills he wishes to add to his cv
        # thus he clicks on the cv button in the navigation bar
        self.browser.find_element_by_id('topnav-cv-button').click()
        self.assertIn('CV | Robert Turff', self.browser.title)
        # Dave looks through the sections on the page before deciding which one to edit first
        headings = self.browser.find_elements_by_tag_name('h1')
        self.assertTrue(any('Eduction' in h.text for h in headings))
        self.assertTrue(any('Tech Skills' in h.text for h in headings))
        self.assertTrue(any('Work Experience' in h.text for h in headings))
        self.assertTrue(any('Projects' in h.text for h in headings))
        self.assertTrue(any('Additional Information' in h.text for h in headings))
        # Dave decides to add to the eduction section first
        self.browser.find_element_by_id('add-uni-year-button').click()
        # Dave adds his first years grades to the page
        textInput = self.browser.find_element_by_id('id_year')
        text = 'First Year Results'
        textInput.send_keys(text)
        textInput = self.browser.find_element_by_id('id_grades')
        gradesText = 'Introduction to tea drinking: 999%'
        textInput.send_keys(gradesText)
        textInput = self.browser.find_element_by_id('id_overall_grade')
        overallGradesText = 'Overall Grade: 105% (Underflow Error Class)'
        textInput.send_keys(overallGradesText)
        self.browser.find_element_by_class_name('save').click()
        time.sleep(0.25)
        # Dave admires his handy work back on the main cv page
        pOnPage = self.browser.find_elements_by_tag_name('p')
        self.assertTrue(any(text in p.text for p in pOnPage))
        self.assertTrue(any(gradesText in p.text for p in pOnPage))
        self.assertTrue(any(overallGradesText in p.text for p in pOnPage))
        # He realises he missed one of the grades and goes to add it
        self.browser.find_element_by_id('edit-uni-year-button-1')
        textInput = self.browser.find_element_by_id('id_grades')
        newGradesText = '\nTea making workshop: 42%'
        textInput.send_keys(newGradesText)
        self.browser.find_element_by_class_name('save').click()
        time.sleep(0.25)
        self.assertTrue(any(gradesText + newGradesText in p.text for p in pOnPage))
