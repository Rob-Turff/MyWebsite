import time

from selenium import webdriver
import unittest

from selenium.webdriver.common.keys import Keys


class AdminUserTests(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def login_to_admin_page(self):
        self.browser.get('http://127.0.0.1:8000/admin/login/?next=/admin/')
        # Dave types in the admin credentials
        credentials = open('login.txt', 'r')
        cookies = self.browser.get_cookies()
        usernameField = self.browser.find_element_by_id('id_username')
        usernameField.send_keys(credentials.readline())
        passwordField = self.browser.find_element_by_id('id_password')
        passwordField.send_keys(credentials.readline())
        credentials.close()
        passwordField.send_keys(Keys.ENTER)
        time.sleep(0.25)

    def test_can_add_edit_and_view_blog_posts(self):
        # Dave decides he wants to be the most powerful being in the universe
        # and so opens and logs into the admin login page
        self.login_to_admin_page()
        # Dave checks that he is now all powerful
        self.assertIn('Site administration | Django site admin', self.browser.title)
        # Dave navigates back to the home page of the website
        self.browser.get('http://127.0.0.1:8000/')
        time.sleep(0.25)
        # Dave, being an absolutely spiffing individual decides that he wants to make a post about yorkshire tea gold
        # and so presses the blog button in the top navigation bar
        self.browser.find_element_by_id('topnav-blog-button').click()
        time.sleep(0.25)
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
        time.sleep(0.25)
        titleInput = self.browser.find_element_by_id('id_title')
        self.assertIn(titleInput.text, title)
        textInput = self.browser.find_element_by_id('id_text')
        self.assertIn(textInput.text, text)
        textInput.send_keys('...')
        self.browser.find_element_by_class_name('save').click()
        time.sleep(0.25)
        # He then goes back to the main blog page to admire his masterwork
        self.browser.find_element_by_id("topnav-blog-button").click()
        time.sleep(0.25)
        titlesOnPage = self.browser.find_elements_by_tag_name('h2')
        self.assertTrue(any(title in t.text for t in titlesOnPage))
        pTextOnPage = self.browser.find_elements_by_tag_name('p')
        self.assertTrue(any(text in t.text for t in pTextOnPage))


    def test_can_navigate_to_blog_page_and_read_posts(self):
        # Dave has heard great tales of the blog posts contained within this website, he goes to checkout the homepage
        self.browser.get('http://localhost:8000')

        # He notices the page title and the navigation links along the top of the page
        self.assertIn('Home | Robert Turff', self.browser.title)
        navLinks = self.browser.find_elements_by_class_name('nav-link')
        self.assertTrue(any('Blog' in navLink.text for navLink in navLinks))
        self.assertTrue(any('Portfolio' in navLink.text for navLink in navLinks))
        self.assertTrue(any('CV' in navLink.text for navLink in navLinks))
        self.assertTrue(any('Contact' in navLink.text for navLink in navLinks))

        # Having seen the blog option he clicks it
        self.browser.find_element_by_id('topnav-blog-button').click()
        time.sleep(0.25)
        self.assertIn('Blog | Robert Turff', self.browser.title)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
