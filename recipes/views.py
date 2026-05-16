from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Recipe, Comment

def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'recipe_list.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    comments = Comment.objects.filter(recipe=recipe).order_by('-created_at')

    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'comments': comments
    })

@login_required
def add_recipe(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        ingredients = request.POST['ingredients']

        recipe = Recipe(
            title=title,
            description=description,
            ingredients=ingredients,
            author=request.user
        )

        recipe.save()
        return redirect('recipe_detail', recipe.id)

    return render(request, 'add_recipe.html')

@login_required
def edit_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)

    if recipe.author != request.user:
        return redirect('recipe_list')

    if request.method == 'POST':
        recipe.title = request.POST['title']
        recipe.description = request.POST['description']
        recipe.ingredients = request.POST['ingredients']
        recipe.save()

        return redirect('recipe_detail', recipe.id)

    return render(request, 'edit_recipe.html', {'recipe': recipe})

@login_required
def delete_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)

    if recipe.author != request.user:
        return redirect('recipe_list')

    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')

    return render(request, 'delete_recipe.html', {'recipe': recipe})

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'my_recipes.html', {'recipes': recipes})

@login_required
def add_comment(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)

    if request.method == 'POST':
        text = request.POST['text']

        comment = Comment(
            recipe=recipe,
            author=request.user,
            text=text
        )

        comment.save()

    return redirect('recipe_detail', recipe.id)

def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipe_list')

    return render(request, 'register.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('recipe_list')