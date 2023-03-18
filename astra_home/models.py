from django.db import models

# Create your models here.


from django.contrib.auth.models import User


class SiteUserModel(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", null=True
    )
    passwordHash = models.CharField(max_length=512)
    registerOtp = models.CharField(max_length=6, null=True)
    salt = models.CharField(max_length=512)
    name = models.CharField(max_length=100, null=False)
    paymentVerified = models.BooleanField(default=False)
    phoneNumber = models.CharField(max_length=10, null=False)
    email = models.CharField(max_length=30, null=False)
    registerCounter = models.PositiveIntegerField(default=0, null=False)
    emailVerified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SportsModel(models.Model):
    # pharmacy
    TEAM_SPORTS = "T"
    INDIVIDUAL_SPORTS = "I"
    SPORTS_CHOICE = (
        (TEAM_SPORTS, "Team Sports"),
        (INDIVIDUAL_SPORTS, "Individual Sports"),
    )
    imageUrl = models.CharField(max_length=200, null=True)
    # posterImage = models.ImageField(upload_to='PosterImages',null=True)
    sportsName = models.CharField(max_length=50, null=False)
    poolPrice = models.PositiveIntegerField(null=False)
    maxPlayers = models.PositiveIntegerField(null=False)
    description = models.CharField(max_length=512, null=False)
    sportsType = models.CharField(
        max_length=1, blank=False, null=False, choices=SPORTS_CHOICE
    )
    regFee = models.PositiveIntegerField(null=False)

    def __str__(self):
        return self.sportsName


class UserCartModel(models.Model):
    userId = models.ForeignKey(SiteUserModel, on_delete=models.SET_NULL, null=True)
    cartAmount = models.PositiveBigIntegerField(default=0)


class CartModel(models.Model):
    userCartId = models.ForeignKey(UserCartModel, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveSmallIntegerField()
    teamName = models.CharField(max_length=50, null=True, unique=False)
    sport = models.ForeignKey(SportsModel, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField(default=0)

    def get_display_price(self):
        return "{0:.2f}".format(self.amount / 100)


class OrderModel(models.Model):  # deprecated
    userCartId = models.ForeignKey(UserCartModel, on_delete=models.CASCADE, null=True)
    amount = models.PositiveIntegerField(default=0)
    email = models.EmailField(max_length=254, default="")
    phone = models.CharField(max_length=10, default="")
    orderStatus = models.BooleanField(default=False)
    createdOn = models.DateTimeField(auto_now_add=True)
