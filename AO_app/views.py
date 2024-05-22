from django.shortcuts import render,HttpResponse, redirect,  get_object_or_404
from .forms import ContactForm, NewsletterForm
from .models import ContactRequest, TableData, Marche 
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from django.core.validators import validate_email

from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.core.mail import EmailMessage

from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from .tokens import generate_token

from AO_app import settings



from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse












def ao(request):
    data = TableData.objects.all()
    return render(request, 'ao.html', {'data': data})

def reglements(request):
    return render(request, 'reglements.html')

def false(request):
    return render(request, 'false.html')

def marches(request):
    marches = Marche.objects.all()
    return render(request, 'marches.html', {'marches': marches})

def demarches(request):
    return render(request, 'demarches.html')

def investissement(request):
    return render(request, 'investissement.html')

def doc(request):
    return render(request, 'doc.html')

def admine(request):
    return render(request, 'admin/admine.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Merci pour votre message!")
            return redirect('contact')
        else:
            messages.error(request, "Il y a eu une erreur dans votre soumission.")
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def index(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing!")
            return redirect('index')
        else:
            messages.error(request, "There was an error with your subscription.")
    else:
        form = NewsletterForm()
    return render(request, 'index.html', {'form': form})




# Create your views here.

def sing_in(request):
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        user = User.objects.filter(email=email).first()
        if user:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect('index')  # Redirige vers la page d'accueil après la connexion
            else:
                messages.error(request, "Mot de passe incorrect")  # Ajoutez un message d'erreur
        else:
            messages.error(request, "Utilisateur non trouvé")  # Ajoutez un message d'erreur

    return render(request, 'login.html', {})  # Affiche le formulaire de connexion (login.html)

def sing_up(request):
    error = False
    message = ""
    
    if request.method == "POST":
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        activite = request.POST.get('activite', None)
        adresse = request.POST.get('adresse', None)
        ville = request.POST.get('ville', None)
        telephone = request.POST.get('telephone', None)
        fax = request.POST.get('fax', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
        





        # Validation de l'email
        try:
            validate_email(email)
        except:
            error = True
            message = "Entrez un email valide s'il vous plaît !"
        
        # Validation des mots de passe
        if error == False:
            if password != repassword:
                error = True
                message = "Les deux mots de passe ne correspondent pas !"
        
        # Vérification de l'existence de l'utilisateur
        user = User.objects.filter(Q(email=email) | Q(username=name)).first()
        if user:
            error = True
            message = f"Un utilisateur avec l'email {email} ou le nom d'utilisateur {name} existe déjà !"
        if len(name)>20:
            messages.error(request, "Username must be under 20 charcters!!")
        if not name.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
        # Enregistrement de l'utilisateur
        if error == False:
            user = User(
                username = name,
                email = email,
                first_name = activite,  # Ajout de l'activité dans le champ du prénom
                last_name = adresse + ' ' + ville + ' ' + telephone + ' ' + fax,  # Concaténation des informations dans le champ du nom de famille
            )
            user.save()
            user.set_password(password)  # Définition du mot de passe
            user.is_active=False
            user.save()
            
            messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
            
            subject = "Welcome to fiftybit Django Login!!"
            message = "Hello " + user.first_name + "!! \n" + "Welcome to fiftybit!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nShovit Nepal"        
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
        
            # Email Address Confirmation Email
            current_site = get_current_site(request)
            email_subject = "Confirm your Email @ FiftyBit - Django Login!!"
            message2 = render_to_string('Email.html',{
            
            'name': user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
            })
            
            email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [user.email],
            )
            send_mail(email_subject, message2, from_email, to_list, fail_silently=True)    
            return redirect('sing_in')  # Redirection vers la page de connexion après l'inscription
            
    context = {
        'error': error,
        'message': message
    }
    
   
    return render(request, 'register.html', context)
@login_required(login_url='sing_in')
def dashboard(request):
    return render(request, 'admin.html', {})

def log_out(request):
    logout(request)
    return redirect('index')


def forgot_password(request):
    error = False
    success = False
    message = ""
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            print("processing forgot password")
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse('update_password', kwargs={'uidb64': uid, 'token': token})
            )

            html = render_to_string('password_reset_email.html', {'reset_url': reset_url})

            msg = EmailMessage(
                "Modification de mot de passe!",
                html,
                "ayaboulifa8@gmail.com",
                [email],
            )

            msg.content_subtype = 'html'
            msg.send()
            
            message = "Un email a été envoyé avec les instructions pour réinitialiser votre mot de passe."
            success = True
        else:
            print("L'utilisateur n'existe pas")
            error = True
            message = "L'utilisateur n'existe pas"
    
    context = {
        'success': success,
        'error': error,
        'message': message
    }
    return render(request, "forgot_password.html", context)
def update_password(request, uidb64=None, token=None):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password and confirm_password and new_password == confirm_password:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Votre mot de passe a été mis à jour avec succès.")
                    return redirect('sing_in')  # Assurez-vous que 'login' correspond à votre nom de route de connexion
                else:
                    messages.error(request, "Le lien de réinitialisation est invalide ou a expiré.")
            except User.DoesNotExist:
                messages.error(request, "L'utilisateur n'existe pas.")
        else:
            messages.error(request, "Les mots de passe ne correspondent pas.")

    context = {
        'uidb64': uidb64,
        'token': token
    }
    return render(request, "update_password.html", context)


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('sing_in')
    else:
        return render(request,'activation_failed.html')

from .models import Profile
from .forms import ProfileForm

@login_required
def profile_view(request):
    
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user, username=user.username, email=user.email)
    
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    
    return render(request, 'profile.html', {'form': form})