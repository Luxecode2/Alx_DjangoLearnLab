# Permissions and Groups Implementation

This section details the setup of custom permissions and user groups within the Django application to manage access control for book-related functionalities.

## 1. Custom Permissions Defined (`bookshelf/models.py`)

Custom permissions have been defined on the `Book` model within its `Meta` class:

- `can_view`: Allows users to see the list of books.
- `can_create`: Allows users to add new books.
- `can_edit`: Allows users to modify existing book details.
- `can_delete`: Allows users to remove books.

These permissions are created in the database when `python manage.py migrate` is run after defining them in `models.py`.

## 2. Groups Configuration (Django Admin Interface)

The following groups have been created and configured through the Django administration panel (`/admin/`):

- **`Viewers` Group**:

  - **Permissions**: `bookshelf | book | Can view book`
  - **Role**: Users in this group can only view the list of books.

- **`Editors` Group**:

  - **Permissions**: `bookshelf | book | Can view book`, `bookshelf | book | Can create book`, `bookshelf | book | Can edit book`
  - **Role**: Users in this group can view, create, and edit books.

- **`Admins` Group**: (Specific to book management, not a superuser group)
  - **Permissions**: `bookshelf | book | Can view book`, `bookshelf | book | Can create book`, `bookshelf | book | Can edit book`, `bookshelf | book | Can delete book`
  - **Role**: Users in this group have full CRUD access to books.

**To set up groups and assign permissions:**

1. Log in to the Django admin as a superuser.
2. Navigate to `Authentication and Authorization` -> `Groups` -> `Add group`.
3. Create each group and assign the specified permissions from the `Available permissions` list to `Chosen permissions`.
4. Navigate to `Authentication and Authorization` -> `Users`.
5. Create new test users (e.g., `viewer_user`, `editor_user`, `admin_user`) or modify existing ones.
6. For each user, select them, then in the `Groups` section, move the appropriate group(s) to `Chosen groups`.

## 3. Enforcing Permissions in Views (`bookshelf/views.py`)

The `@permission_required` decorator from `django.contrib.auth.decorators` is used in `views.py` to enforce these permissions. This decorator checks if the logged-in user possesses the required permission. If not, it raises a `403 Forbidden` error (due to `raise_exception=True`).

**Examples:**

- `book_list` view requires `bookshelf.can_view`.
- `book_create` view requires `bookshelf.can_create`.
- `book_update` view requires `bookshelf.can_edit`.
- `book_delete` view requires `bookshelf.can_delete`.

## 4. Testing Permissions

Manual testing involves:

- Creating users and assigning them to the `Viewers`, `Editors`, and `Admins` groups.
- Logging in as each user and attempting to perform actions (view, create, edit, delete books) to verify that only authorized actions are permitted and unauthorized actions result in a 403 error page.
