# Online Course Platform

Welcome to the Online Course Platform! This platform is built using Django and provides a robust environment for creating and managing online courses.

## Getting Started

Follow these steps to set up the Django project and implement user app registration, login, and logout.

### 1. Set Up Django Project

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-project.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your-project
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

5. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### 2. Create Static Files

1. Inside your Django app directory, create a `static` folder.

    ```bash
    cd your_app_name
    mkdir static
    ```

2. Place your static files (CSS, JS, images, etc.) inside the `static` folder.

### 3. User App Registration, Login, and Logout

1. In your Django app, create a `registration` folder inside the `templates` directory.

    ```bash
    cd your_app_name/templates
    mkdir registration
    ```

2. Create `registration/login.html` and `registration/logout.html` templates for login and logout views.

3. Update your project's `urls.py` to include Django's built-in authentication views.

    ```python
    # your_project_name/urls.py

    from django.contrib.auth import views as auth_views

    urlpatterns = [
        # ... your other URL patterns

        path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
        path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

        # ... your other URL patterns
    ]
    ```

4. Ensure the `django.contrib.auth` app is included in your `INSTALLED_APPS` in `settings.py`.

    ```python
    # your_project_name/settings.py

    INSTALLED_APPS = [
        # ... other apps
        'django.contrib.auth',
        'django.contrib.contenttypes',
        # ... other apps
    ]
    ```

5. Run migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

7. Access the login page at [http://localhost:8000/accounts/login/](http://localhost:8000/accounts/login/) and the logout page at [http://localhost:8000/accounts/logout/](http://localhost:8000/accounts/logout/).

Congratulations! You've completed the initial setup and implemented user app registration, login, and logout functionalities. Continue building your Online Course Platform by adding more features and functionalities as needed.
