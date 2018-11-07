from django.db import models

# Create your models here.
class Jobseeker(models.Model):
	Full_Name = models.CharField(max_length=200, null=False)
	Gender = models.CharField(max_length=20, null=False)
	DOB = models.DateTimeField(help_text = 'Your Date of Birth')
	Educational_Level = models.CharField(help_text='Choose:1-None, 2-Primary(<P.7),3-UCE(S.1 - S.4 ),4-UACE(S.5-S.6 ),5-Bachelor(BA/Bsc),6-Master(MA/Msc),7-PhD/MD', max_length=200, null=False)
	work_Experience = models.FloatField(help_text='Your working experince in years, e.g 1.7 years', null=False)
	Job_Title = models = models.CharField(max_length=200, null=False)
	Job_Decription = models.TextField(max_length=5000, null=False)
	Post_Date = models.DateField(auto_now_add=True)

	class Meta:
		ordering = ['-Post_Date']

	def _unicode_(self):
		return self.Full_Name