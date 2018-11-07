from django.core.management.base import BaseCommand
from faker import Faker
import random
import uuid
from models import Jobseeker
from datetime import datetime, timedelta

fake = Faker('en_US')

end = datetime.now()
start = end-timedelta(days=21900) 
random_date  = start+(end-start)*random.random()

class Command(BaseCommand):
	help = 'generate 10k Jobseeker profiles'

	for i in range(10*4):
		full_name = fake.name()
		gender = random.choice(['Male','Female'])
		date_of_birth = random_date
		educational_level = random.choice(['None,Primary(<P.7),UCE(S.1 - S.4 ),UACE(S.5-S.6 ),Bachelor(BA/Bsc),Master(MA/Msc),PhD/MD'])
		work_experience = random.uniform(0.0,40.0)
		job_title = fake.job()
		job_decription = fake.sentence()
		post_date = datetime.now()

		new_jobseekers = Jobseeker.objects.create(
			Full_Name = full_name,
			Gender = gender,
			DOB = date_of_birth,
			Education_Level = education_level,
			Work_Experience = work_experience,
			Job_Description = job_description,
			Post_Date = post_date
			)

		new_jobseekers.save()
		print(new_jobseekers)