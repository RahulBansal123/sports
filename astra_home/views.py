from django.shortcuts import render
from django.http.response import (
    Http404,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
    JsonResponse,
)

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .models import SiteUserModel, SportsModel, CartModel, UserCartModel, OrderModel
import bcrypt
from django.conf import settings
import pyotp
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from datetime import datetime
import base64
from django.shortcuts import get_object_or_404


def isLogin(request):
    if request.session["userid"]:
        return True
    else:
        return False


def getLogOut(request):
    if request.session["userid"]:
        request.session["userid"] = ""
    return redirect("/home")


def send_otp(email, otp, username):
    sub = "Verify your Astra Account"
    emailFrom = settings.EMAIL_HOST_USER
    msg = f"Hello {username}, Please user this OTP to verify your ASTRA account { otp }"
    emailSend = EmailMessage(
        sub,
        msg,
        emailFrom,
        to=[
            email,
        ],
    )
    emailSend.send()
    print("gg4")


def generateKey(phone):
    return str(phone) + str(datetime.date(datetime.now())) + settings.OTP_SECRET_KEY


def homeView(request):
    anon = "False"
    if isLogin(request):
        return render(request, "home.html")
    return render(request, "home.html", {"anon": anon})


def registerView(request):
    print("gg")
    sports = SportsModel.objects.all()

    return render(request, "register.html", {"sports": sports})


def getRegister(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        userName = request.POST.get("username")

        user_obj = User.objects.filter(username=userName)

        if user_obj.exists():
            messages.warning(request, "User Name is already taken")
            return HttpResponseRedirect(request.path_info)

        password = bytes(password, "utf-8")
        salt = bcrypt.gensalt()
        # Hashing the password
        hashed = bcrypt.hashpw(password, salt)
        user_obj = User.objects.create(username=userName, email=email)
        user_obj.set_password(password)
        user_obj.save()

        siteUser = SiteUserModel.objects.create(
            user=user_obj,
            name=name,
            email=email,
            phoneNumber=phone,
            passwordHash=str(hashed, "UTF-8"),
            salt=str(salt, "UTF-8"),
        )

        siteUser.registerCounter += 1

        key = generateKey(phone)
        key = base64.b32encode(key.encode())
        request.session["userid"] = user_obj.id
        OTP = pyotp.HOTP(key)
        otp = OTP.at(siteUser.registerCounter)
        siteUser.registerOtp = otp
        siteUser.save()
        send_otp(str(email), otp, user_obj.username)

        return redirect("/verifyOtp/")

    return render(request, "signup.html")


def getOtp(request):
    print("hello")
    if isLogin(request):
        if request.method == "POST":
            otp = str(request.POST.get("b1"))

            user_id = request.session["userid"]
            user = get_object_or_404(User, pk=user_id)
            mobile = ""

            siteUser = get_object_or_404(SiteUserModel, user=user)

            siteUser = get_object_or_404(SiteUserModel, user=user)
            mobile = siteUser.phoneNumber

            keygen = generateKey(mobile)
            key = base64.b32encode(keygen.encode())  # Generating Key
            OTP = pyotp.HOTP(key)  # HOTP Model
            if OTP.verify(otp, siteUser.registerCounter):  # Verifying the OTP
                siteUser.emailVerified = True
                siteUser.save()
                return redirect("/login")
            else:
                messages.success(request, "Invalid OTP")
                return HttpResponseRedirect(request.path_info)

        return render(request, "otp.html")
    else:
        return render("/login")


def getLogin(request):
    if request.method == "POST":
        password = request.POST.get("loginPassword")
        userName = request.POST.get("loginUsername")

        user_obj = User.objects.filter(username=userName)

        if not user_obj.exists():
            # render(request,"login.html",{"error" : "Account Not Found"})
            messages.warning(request, "Account Not Found")
            return HttpResponseRedirect(request.path_info)
        siteUser = SiteUserModel.objects.filter(user=user_obj[0])
        siteUser = siteUser[0]
        if not siteUser.emailVerified:
            messages.warning(request, "Email not Verified")
            return HttpResponseRedirect(request.path_info)
        print(user_obj[0].email)

        allUserHash = bytes(siteUser.passwordHash, "utf-8")
        allUserSalt = bytes(siteUser.salt, "utf-8")
        password = bytes(password, "utf-8")
        result = bcrypt.hashpw(password, allUserSalt)
        result = str(result, "UTF-8")

        if result == siteUser.passwordHash:
            request.session["userid"] = user_obj[0].id
            return redirect("/")

        else:
            messages.warning(request, "Invalid Credentials")
            return HttpResponseRedirect(request.path_info)

    return render(request, "login.html")


def getCartView(request):
    if isLogin(request):
        uid = request.session.get("userid")
        user = get_object_or_404(User, pk=int(uid))

        siteuser = SiteUserModel.objects.get(user=user)
        try:
            cart = UserCartModel.objects.get(userId=siteuser)
        except:
            return render(request, "empty_cart.html")
        request.session["userCart"] = cart.id
        cartModel = CartModel.objects.filter(userCartId=cart)
        if len(cartModel) == 0:
            return redirect("/emptyCart/")
        context = {"cart": cartModel, "userCart": cart}
        return render(request, "cart.html", context)
    return redirect("/login/")


def addToCart(request):
    if isLogin(request):
        sports_id = request.GET.get("sports_id")
        if sports_id:
            if request.method == "POST":
                team_name = str(request.POST.get("team-name"))
                team_size = request.POST.get("team-size")

                uid = request.session.get("userid")
                user = get_object_or_404(User, pk=int(uid))
                siteuser = SiteUserModel.objects.get(user=user)
                product = get_object_or_404(SportsModel, pk=sports_id)

                try:
                    temp = CartModel.objects.get(teamName=team_name)
                    messages.warning(request, "Team name already exists")
                    return HttpResponseRedirect(request.path_info)
                except:
                    try:
                        userCart = UserCartModel.objects.get(userId=siteuser)
                    except:
                        userCart = UserCartModel()
                        userCart.userId = siteuser
                        userCart.save()

                    try:
                        cart = CartModel.objects.get(sport=product, userCartId=userCart)
                        qty = cart.quantity
                        cart1 = cart
                        if team_name:
                            cart1.teamName = team_name
                            cart1.quantity = team_size
                        else:
                            cart1.quantity = qty + 1

                        cart1.amount = int(product.regFee * int(cart1.quantity))
                        cart1.save()
                        userCart.cartAmount = cart1.amount
                    except:
                        cart = CartModel()
                        cart.userCartId = userCart
                        if cart.quantity is None:
                            cart.quantity = team_size
                        else:
                            if team_size:
                                cart.quantity = team_size
                            else:
                                cart.quantity += 1
                        cart.sport = product
                        if cart.teamName is None:
                            if team_name:
                                cart.teamName = team_name
                            else:
                                cart.teamName = siteuser.name

                        # cart.stripePaymentIntent
                        cart.amount = int(product.regFee * int(cart.quantity))
                        cart.save()
                        userCart.cartAmount = cart.amount
                    userCart.save()
            else:
                return render(request, "info.html", {"sports_id": sports_id})
        return redirect("/cart/")
    else:
        return redirect("/login/")


def removeFromCart(request):
    if isLogin(request):
        sports_id = request.GET.get("sports_id")
        if sports_id:
            if request.method == "POST":
                uid = request.session.get("userid")
                user = get_object_or_404(User, pk=int(uid))

                siteuser = SiteUserModel.objects.get(user=user)

                product = get_object_or_404(SportsModel, pk=sports_id)
                userCart = UserCartModel.objects.get(userId=siteuser)
                cart = CartModel.objects.filter(sport=product, userCartId=userCart)
                cart1 = cart[0]
                if cart1.quantity == 1:
                    cart1.delete()
                    return redirect("/cart/")

                if cart1.quantity is not None:
                    cart1.quantity -= 1
                    cart1.save()
                else:
                    return redirect("/cart/")
                if cart1.amount is not None:
                    cart1.amount -= product.regFee
                else:
                    return redirect("/cart/")

                if cart1.quantity == 0:
                    cart1.delete()
                cart1.save()

                userCart.cartAmount = int(cart1.amount)
                userCart.save()
                return redirect("/cart/")
            else:
                return redirect("/register/")
        else:
            return redirect("/register/")

    return redirect("/login/")


def getEmptyCart(request):
    return render(request, "empty_cart.html")


def getTempView(request):
    return render(request, "temp.html")
