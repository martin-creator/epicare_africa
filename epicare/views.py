from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q
import csv
import uuid
import requests
from .models import Product, Category, BlogPost, Order, ContactSubmission, NewsletterSubscription
from .forms import ContactForm, NewsletterForm, SearchForm

def homepage(request):
    products = Product.objects.all()[:3]
    # featured_post = BlogPost.objects.filter(is_featured=True).first()
    latest_posts = BlogPost.objects.all().order_by('-created_at')[:3]
    # context = {
    #     'latest_posts': latest_posts,
    # }
    # return render(request, 'home.html', context)
    newsletter_form = NewsletterForm()
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, 'Subscribed successfully!')
            return redirect('homepage')
    return render(request, 'homepage.html', {
        'products': products,
        'newsletter_form': newsletter_form,
        # 'featured_post': featured_post,
        'latest_posts': latest_posts,
    })

def about(request):
    return render(request, 'about.html')

def shop(request):
    search_form = SearchForm(request.GET)
    products = Product.objects.all()
    categories = Category.objects.all()
    sort_by = request.GET.get('sort_by', 'name')
    category_id = request.GET.get('category', '')

    if search_form.is_valid() and search_form.cleaned_data['query']:
        query = search_form.cleaned_data['query']
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category_id:
        products = products.filter(category_id=category_id)

    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('name')

    return render(request, 'shop.html', {
        'products': products,
        'categories': categories,
        'search_form': search_form,
        'sort_by': sort_by,
        'selected_category': category_id,
    })

def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        email = request.POST.get('email', 'customer@example.com')
        phone = request.POST.get('phone', '254101108886')
        if quantity <= product.stock:
            # Create order
            order = Order.objects.create(
                product=product,
                quantity=quantity,
                email=email,
                phone=phone,
            )
            # Simplified Pesapal integration
            pesapal_url = "https://demo.pesapal.com/api/PostPesapalDirectOrderV4"
            params = {
                'amount': float(product.price * quantity),
                'description': f"Purchase of {product.name}",
                'type': 'MERCHANT',
                'reference': str(uuid.uuid4()),
                'email': email,
                'phone_number': phone,
                'currency': 'KES',
                'first_name': 'Customer',
                'last_name': 'Name',
            }
            try:
                response = requests.post(pesapal_url, json=params)
                if response.status_code == 200:
                    product.stock -= quantity
                    product.save()
                    # Send order confirmation email
                    send_mail(
                        subject=f'Epicare Africa Order #{order.id} Confirmation',
                        message=f'Thank you for your order!\n\nProduct: {product.name}\nQuantity: {quantity}\nTotal: KES {product.price * quantity}\nStatus: {order.status}',
                        from_email='your-gmail-address@gmail.com',
                        recipient_list=[email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Payment initiated and order confirmed!')
                    return redirect(response.json().get('redirect_url', 'shop'))
                else:
                    order.status = 'Failed'
                    order.save()
                    messages.error(request, 'Payment failed. Please try again.')
            except requests.RequestException:
                order.status = 'Failed'
                order.save()
                messages.error(request, 'Payment gateway error.')
        else:
            messages.error(request, 'Insufficient stock.')
    return render(request, 'shop.html', {'products': [product]})

def blog(request):
    search_form = SearchForm(request.GET)
    posts = BlogPost.objects.all().order_by('-created_at')
    if search_form.is_valid() and search_form.cleaned_data['query']:
        query = search_form.cleaned_data['query']
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    
    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog.html', {
        'page_obj': page_obj,
        'search_form': search_form,
    })

# def blog_detail(request, post_id):
#     post = get_object_or_404(BlogPost, id=post_id)
#     return render(request, 'blog_detail.html', {'post': post})

from django.shortcuts import render, get_object_or_404
from .models import BlogPost
import random

def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    # Fetch up to 3 other blog posts, excluding the current one
    related_posts = BlogPost.objects.exclude(id=post_id).order_by('-created_at')[:3]
    
    # List of epilepsy facts for placeholder content
    epilepsy_facts = [
        {
            'title': 'Epilepsy Affects Millions',
            'content': 'Over 50 million people worldwide live with epilepsy, with a significant portion in Africa.',
            'image': 'https://placehold.co/600x400/6A0DAD/FFFFFF?text=Epilepsy+Facts'
        },
        {
            'title': 'Seizures Are Diverse',
            'content': 'Epilepsy can cause various seizure types, from brief lapses to convulsions.',
            'image': 'https://placehold.co/600x400/8655B9/FFFFFF?text=Seizure+Info'
        },
        {
            'title': 'Treatment Accessibility',
            'content': 'Affordable anti-seizure medications can control seizures in about 70% of cases.',
            'image': 'https://placehold.co/600x400/FF6C0C/FFFFFF?text=Treatment+Access'
        },
        {
            'title': 'Stigma Reduction',
            'content': 'Education and awareness can significantly reduce epilepsy-related stigma in communities.',
            'image': 'https://placehold.co/600x400/6A0DAD/FFFFFF?text=Community+Awareness'
        },
        {
            'title': 'Triggers Vary',
            'content': 'Stress, lack of sleep, or flashing lights can trigger seizures in some individuals.',
            'image': 'https://placehold.co/600x400/8655B9/FFFFFF?text=Seizure+Triggers'
        }
    ]
    
    # If fewer than 3 related posts, fill with random epilepsy facts
    related_content = list(related_posts)
    if len(related_content) < 3:
        needed = 3 - len(related_content)
        # Exclude facts already used by title to avoid duplicates
        used_titles = [post.title for post in related_content]
        available_facts = [fact for fact in epilepsy_facts if fact['title'] not in used_titles]
        # Randomly select needed facts
        selected_facts = random.sample(available_facts, min(needed, len(available_facts)))
        related_content.extend(selected_facts)
    
    context = {
        'post': post,
        'related_content': related_content
    }
    return render(request, 'blog_detail.html', context)


# # return the latest 3 blog posts for the homepage

# def get_latest_blog_posts():
#     return BlogPost.objects.all().order_by('-created_at')[:3]





def contact(request):
    contact_form = ContactForm()
    newsletter_form = NewsletterForm()
    if request.method == 'POST':
        if 'contact_submit' in request.POST:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact_submission = contact_form.save()
                # Send email notification to admin
                send_mail(
                    subject='New Contact Form Submission',
                    message=f'Name: {contact_submission.name}\nEmail: {contact_submission.email}\nMessage: {contact_submission.message}',
                    from_email='your-gmail-address@gmail.com',
                    recipient_list=['martinlubowa@outlook.com'],
                    fail_silently=False,
                )
                messages.success(request, 'Message sent successfully!')
                return redirect('contact')
        elif 'newsletter_submit' in request.POST:
            newsletter_form = NewsletterForm(request.POST)
            if newsletter_form.is_valid():
                newsletter_form.save()
                messages.success(request, 'Subscribed successfully!')
                return redirect('contact')
    return render(request, 'contact.html', {
        'contact_form': contact_form,
        'newsletter_form': newsletter_form,
    })

def export_newsletter_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="newsletter_subscriptions.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Email', 'Subscribed At'])
    
    subscriptions = NewsletterSubscription.objects.all()
    for subscription in subscriptions:
        writer.writerow([subscription.email, subscription.subscribed_at])
    
    return response