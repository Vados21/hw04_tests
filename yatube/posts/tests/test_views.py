
from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth_user')
        cls.group = Group.objects.create(
            title='Текст поста',
            slug='test_slug',
            description='Описание поста'
        )
        cls.group2 = Group.objects.create(
            title='Текст поста',
            slug='test_slug2',
            description='Описание поста'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.user)

    def test_index_uses_correct_template(self):
        response = self.guest_client.get(reverse('posts:index'))
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_pages_uses_correct_template(self):
        post_id = PostPagesTests.post.id
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': (
                reverse('posts:group_list', kwargs={'slug': 'test_slug'})
            ),
            'posts/profile.html': (
                reverse('posts:profile', kwargs={'username': 'auth_user'})
            ),
            'posts/post_detail.html': (
                reverse('posts:post_detail', kwargs={'post_id': post_id})
            ),
            'posts/create_post.html': reverse('posts:create_post'),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_edit_page(self):
        post_id = PostPagesTests.post.id
        templates_pages_names = {
            'posts/create_post.html': (
                reverse('posts:post_edit', kwargs={'post_id': post_id}))
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:create_post'))
        form_fields = {
            'text': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth_user_2')
        cls.group = Group.objects.create(
            title='Текст поста',
            slug='test_slug_2',
            description='Описание поста'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
            group=cls.group,
        )
        cls.post2 = Post.objects.create(
            author=cls.user,
            text='Тестовый текст2',
            group=cls.group,
        )
        cls.post3 = Post.objects.create(
            author=cls.user,
            text='Тестовый текст3',
            group=cls.group,
        )
        cls.post4 = Post.objects.create(
            author=cls.user,
            text='Тестовый текст4',
            group=cls.group,
        )
        cls.post5 = Post.objects.create(
            author=cls.user,
            text='Тестовый текст5',
            group=cls.group,
        )
        cls.post6 = Post.objects.create(
            author=cls.user,
            text='Тестовый текст6',
            group=cls.group,
        )
        cls.post6 = Post.objects.create(
            author=cls.user,
            text='Тестовый текст6',
            group=cls.group,
        )
        cls.post7 = Post.objects.create(
            author=cls.user,
            text='Тестовый текст7',
            group=cls.group,
        )
        cls.post8 = Post.objects.create(
            author=cls.user,
            text='Тестовый текст8',
            group=cls.group,
        )
        cls.post9 = Post.objects.create(
            author=cls.user,
            text='Тестовый текст9',
            group=cls.group,
        )
        cls.post10 = Post.objects.create(
            author=cls.user,
            text='Тестовый текст10',
            group=cls.group,
        )
        cls.post11 = Post.objects.create(
            author=cls.user,
            text='Тестовый текст11',
            group=cls.group,
        )
        cls.post12 = Post.objects.create(
            author=cls.user,
            text='Тестовый текст12',
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        response = self.guest_client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)
