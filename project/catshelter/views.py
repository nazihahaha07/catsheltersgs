from django.shortcuts import render,redirect,get_object_or_404
from catshelter.models import User,Login,Cat,Image,Report,VolunteerDate,VolunteerApplication,Inventory,Fund,Admin,AdminLogin
from .forms import ImageForm,CatForm,ReportForm,VolunteerDateForm,VolunteerApplicationForm,UpdateInventoryForm,InventoryForm,FundForm,UpdateFundForm
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponse
# Create your views here.

def startpage(request):
    return render(request, "startpage.html")

def signup(request):
    if request.method == 'POST':
        userfullname = request.POST.get('userfullname')
        useremail = request.POST.get('useremail')
        userphone = request.POST.get('userphone')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User(userfullname=userfullname, useremail=useremail, userphone=userphone)
        user.save()
        
        login = Login(username=username, password=password, user=user)
        login.save()

        request.session['user_fullname'] = userfullname
        
        return redirect('login')
    
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            login_instance = Login.objects.get(username=username, password=password)
            
            # Set the session key based on the user's fullname
            request.session['user_fullname'] = login_instance.user.userfullname
            
            # Pass user's fullname to the template
            return render(request, 'homepage.html', {'user_fullname': login_instance.user.userfullname})
        except Login.DoesNotExist:
            pass

    alldata = Login.objects.all()
    context = {
        'alldata': alldata
    }
    return render(request, 'login.html', context)

def homepage(request):
    username = request.session.get('username')
    return render(request, "homepage.html", {'username': username})

def profile(request):
    if 'user_fullname' in request.session:
        user_fullname = request.session['user_fullname']
        user = User.objects.get(userfullname=user_fullname)
        login = Login.objects.get(user=user)
        return render(request, 'profile.html', {'user': user, 'login': login})
    else:
        return redirect('login')
    
def editprofile(request):
    if 'user_fullname' in request.session:
        user_fullname = request.session['user_fullname']
        user = User.objects.get(userfullname=user_fullname)
        login = Login.objects.get(user=user)

        if request.method == 'POST':
            # Handle the form data for editing the profile
            new_email = request.POST.get('email')
            new_phone = request.POST.get('phone')
            
            # Update the user's email and phone number
            user.useremail = new_email
            user.userphone = new_phone
            user.save()

            # Redirect to the profile page after editing
            return redirect('profile')

        return render(request, 'editprofile.html', {'user': user})
    else:
        return redirect('login')
    
def save_profile_changes(request):
    if request.method == 'POST':
        # Get the current user's userfullname from the session
        user_fullname = request.session.get('user_fullname')
        
        if not user_fullname:
            return redirect('login')

        # Retrieve the User object
        try:
            user = User.objects.get(userfullname=user_fullname)
        except User.DoesNotExist:
            return redirect('login')

        # Get updated profile information from the form
        new_email = request.POST.get('email')
        new_phone = request.POST.get('phone')
        
        # Update the user's profile information
        user.useremail = new_email
        user.userphone = new_phone
        user.save()
        
        # Redirect to the profile page after editing
        return redirect('profile')

    # Handle cases where the request method is not POST
    return redirect('profile')

def is_admin(user):
    return user.is_staff

def cat_list(request):
    cats = Cat.objects.all()
    return render(request, 'cat_list.html', {'cats': cats})

def cat_detail(request, pk):
    cat = get_object_or_404(Cat, pk=pk)
    return render(request, 'cat_detail.html', {'cat': cat})

def add_cat(request):
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES)  # Handle file upload
        if form.is_valid():
            form.save()
            return redirect('admin_catlist')
    else:
        form = CatForm()
    return render(request, 'add_cat.html', {'cat_form': form})

def home(request):
    cats = Cat.objects.all()
    return render(request, 'cat_detail.html', {'cats': cats})

def about_us(request):
    return render(request, 'about_us.html')

def signup_admin(request):
    if request.method == 'POST':
        adminfullname = request.POST.get('adminfullname')
        adminemail = request.POST.get('adminemail')
        adminphone = request.POST.get('adminphone')
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Signup details: {adminfullname}, {adminemail}, {adminphone}, {username}, {password}")

        admin = Admin(adminfullname=adminfullname, adminemail=adminemail, adminphone=adminphone)
        admin.save()

        hashed_password = make_password(password)
        print(f"Hashed password: {hashed_password}")
        
        admin_login = AdminLogin(username=username, password=hashed_password, admin=admin)
        admin_login.save()

        request.session['admin_fullname'] = adminfullname

        return redirect('admin_login')

    return render(request, 'admin_signup.html')

def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Received username: {username}, password: {password}")

        try:
            admin_login_instance = AdminLogin.objects.get(username=username)
            print(f"AdminLogin instance found: {admin_login_instance}")
            
            if check_password(password, admin_login_instance.password):
                print("Password matched")
                request.session['admin_fullname'] = admin_login_instance.admin.adminfullname
                return redirect('admin_dashboard')
            else:
                print("Password did not match")
                messages.error(request, 'Password did not match')
        except AdminLogin.DoesNotExist:
            print("Admin with this username does not exist")
            messages.error(request, 'Admin with this username does not exist')

    alldata = AdminLogin.objects.all()
    context = {
        'alldata': alldata
    }
    return render(request, 'admin_login.html', context)

def admin_dashboard_view(request):
    if 'admin_fullname' not in request.session:
        return redirect('admin_login')
    admin_fullname = request.session['admin_fullname']
    return render(request, 'admin_dashboard.html', {'admin_fullname': admin_fullname})

def admin_catlist(request):
    cats = Cat.objects.all()
    return render(request, 'admin_catlist.html', {'cats': cats})

def admin_catdetail(request, cat_id):
    cat = get_object_or_404(Cat, pk=cat_id)
    return render(request, 'admin_catdetail.html', {'cat': cat})

def report_cat(request, cat_id):
    cat = get_object_or_404(Cat, pk=cat_id)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.cat = cat
            report.save()
            return redirect('cat_list')  # Redirect to the admin report page
    else:
        form = ReportForm()
    return render(request, 'report_cat.html', {'cat': cat, 'form': form})

def submit_report(request, cat_id):
    cat = get_object_or_404(Cat, pk=cat_id)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.cat = cat
            report.save()
            return redirect('cat_list')  # Redirect to the admin report page
    else:
        form = ReportForm()
    return render(request, 'report_cat.html', {'cat': cat, 'form': form})

def admin_report(request):
    reports = Report.objects.all()
    return render(request, 'admin_report.html', {'reports': reports})

def admin_cat_update(request, cat_id):
    cat = get_object_or_404(Cat, pk=cat_id)
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            form.save()
            return redirect('admin_catlist')  # Correct URL pattern
    else:
        form = CatForm(instance=cat)
    return render(request, 'cat_update.html', {'form': form, 'cat': cat})

def admin_cat_delete(request, cat_id):
    cat = get_object_or_404(Cat, pk=cat_id)
    if request.method == 'POST':
        cat.delete()
        return redirect('admin_catlist')
    return render(request, 'cat_confirm_delete.html', {'cat': cat})

def admin_volunteer(request):
    if request.method == 'POST':
        form = VolunteerDateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_volunteer')
    else:
        form = VolunteerDateForm()
    return render(request, 'admin_volunteer.html', {'form': form})

def volunteer_application(request):
    if request.method == 'POST':
        form = VolunteerApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('verifyvolunteer')
    else:
        form = VolunteerApplicationForm()
    return render(request, 'volunteer.html', {'form': form})

def volunteersubmit(request):
    applications = VolunteerApplication.objects.all()
    return render(request, 'volunteersubmit.html', {'applications': applications})

def verifyvolunteer(request):
    return render(request, "verifyvolunteer.html")

def delete_submission(request, id):
    application = get_object_or_404(VolunteerApplication, id=id)
    if request.method == 'POST':
        application.delete()
        return redirect('volunteersubmit')
    return render(request, 'volunteersubmit.html')

def inventory_view(request):
    inventory_items = Inventory.objects.all()
    return render(request, 'inventory.html', {'inventory_items': inventory_items})

def admin_inventory_view(request):
    inventory_items = Inventory.objects.all()
    return render(request, 'admin_inventory.html', {'inventory_items': inventory_items})

def add_inventory_item(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_inventory')
    else:
        form = InventoryForm()
    return render(request, 'add_inventory_item.html', {'form': form})

def update_inventory_item(request, pk):
    inventory_item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        form = UpdateInventoryForm(request.POST, instance=inventory_item)
        if form.is_valid():
            form.save()
            return redirect('admin_inventory')
    else:
        form = UpdateInventoryForm(instance=inventory_item)
    return render(request, 'update_inventory_item.html', {'form': form})

def delete_inventory_item(request, pk):
    inventory_item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        inventory_item.delete()
        return redirect('admin_inventory')
    return render(request, 'delete_inventory_item.html', {'inventory_item': inventory_item})

def all_users(request):
    users = User.objects.all()
    return render(request, 'all_user.html', {'users': users})

def delete_report(request, id):
    report = get_object_or_404(Report, id=id)
    report.delete()
    return redirect('admin_report')

def admin_fund_view(request):
    funds = Fund.objects.all()
    return render(request, 'admin_fund.html', {'funds': funds})

def add_fund(request):
    if request.method == 'POST':
        form = FundForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_fund')
    else:
        form = FundForm()
    return render(request, 'add_fund.html', {'form': form})

def update_fund(request, pk):
    fund = get_object_or_404(Fund, pk=pk)
    if request.method == 'POST':
        form = UpdateFundForm(request.POST, instance=fund)
        if form.is_valid():
            form.save()
            return redirect('admin_fund')
    else:
        form = UpdateFundForm(instance=fund)
    return render(request, 'update_fund.html', {'form': form})

def delete_fund(request, pk):
    fund = get_object_or_404(Fund, pk=pk)
    if request.method == 'POST':
        fund.delete()
        return redirect('admin_fund')
    return render(request, 'delete_fund.html', {'fund': fund})