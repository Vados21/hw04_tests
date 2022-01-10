
from django.contrib.auth import get_user_model
from django.http import response


from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth_user')
        cls.group = Group.objects.create(
            title='Текст поста',
            slug='test_slug',
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

    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'test_text',
            'group': PostCreateFormTests.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:create_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': PostCreateFormTests.user.username})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='test_text',
                group=PostCreateFormTests.group.id
            ).exists()
        )

    def test_post_edit(self):
        post = Post.objects.create(
            text='Первоначальный текст поста',
            group=self.group,
            author=self.user
        )

        form_data = {
            'text': 'Был изменен текст',
            'group': post.group.id,
        }
        response = self.authorized_client_author.post(
            reverse(
                'posts:post_edit',
                kwargs={
                    'post_id': post.id
                }
            ),
            data=form_data,
            follow=True
        )
        post.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.text, form_data['text'])