"""
AptCare — Master Presentation Database Seeder (TIME WARP FIXED)
=============================================
Run with:  python manage.py seed_data
"""

import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from core.models import (
    CustomUser, Department, ComplaintCategory,
    Staff, Complaint, Attachment,
    Escalation, Notification, StaffPerformanceLog,
    Review, OTPVerification
)

# ─────────────────────────────────────────────────────
# DATA POOLS
# ─────────────────────────────────────────────────────
FIRST_NAMES = ["Aarav","Aditya","Akash","Anand","Arjun","Aryan","Ashwin","Bharath","Deepak","Dinesh","Ganesh","Gopal","Hari","Jagadesh","Karthik","Kavin","Kumar","Lokesh","Mahesh","Manoj","Mohan","Muthu","Naveen","Nikhil","Pavan","Praveen","Priya","Rahul","Rajesh","Rakesh","Ram","Ramesh","Ravi","Rohit","Sachin","Sanjay","Senthil","Shankar","Shiva","Siva","Suresh","Surya","Tamil","Udhay","Venkat","Vikram","Vinod","Vishnu","Priyanka","Kavya","Ananya","Divya","Geetha","Hema","Janani","Kamala","Keerthana","Lakshmi","Lavanya","Meena","Mythili","Nithya","Padma","Pavithra","Pooja","Revathi","Saraswathi","Saranya","Sindhu","Sujatha","Sunitha","Swetha","Uma","Usha","Vani","Vasantha","Vijaya","Yamuna"]
LAST_NAMES = ["Kumar","Sharma","Patel","Rajan","Nair","Pillai","Rao","Reddy","Singh","Iyer","Menon","Krishnan","Murugan","Selvam","Pandian","Anand","Arumugam","Balan","Chandra","Durai","Ganesh","Govindan","Jayaram","Kannan","Mani","Natarajan","Palani","Prakash","Raman","Sankaran","Subramaniam","Velu","Venkatesh","Vijayan","Periyasamy","Ramasamy","Thangavel","Chinnaswamy","Palanisamy","Duraisamy"]
DOMAINS = ["gmail.com","yahoo.com","outlook.com","hotmail.com"]

DEPARTMENTS = ["Electrical", "Plumbing", "Lift Maintenance", "Security", "Housekeeping", "IT Support", "General Maintenance"]

STAFF_LIST = [
    ("Rajesh", "Kumar", "Electrical"), ("Suresh", "Nair", "Electrical"),
    ("Mohan", "Das", "Plumbing"), ("Priya", "Sharma", "Plumbing"),
    ("Arun", "Mehta", "Lift Maintenance"), ("Vikram", "Singh", "Security"),
    ("Deepa", "Thomas", "Security"), ("Anita", "Verma", "Housekeeping"),
    ("Ravi", "Pillai", "IT Support"), ("Sanjay", "Patel", "General Maintenance"),
    ("Kavitha", "Menon", "General Maintenance"), ("Dinesh", "Reddy", "Housekeeping")
]

CATEGORIES = [
    ("Lift / Elevator", 30, "Lift Maintenance"), ("Electrical / Power", 25, "Electrical"),
    ("Gas / Fire Safety", 30, "General Maintenance"), ("Water Leakage", 20, "Plumbing"),
    ("Security Issue", 25, "Security"), ("Garbage / Waste", 15, "Housekeeping"),
    ("Cleaning / Housekeeping", 10, "Housekeeping"), ("Noise / Nuisance", 8, "Security"),
    ("Internet / Network", 15, "IT Support"), ("Plumbing / Pipe", 20, "Plumbing")
]

COMPLAINT_DESCRIPTIONS = {
    "Lift / Elevator": ["The lift in Block {block} is not working.", "Lift door is not closing properly.", "The lift is stuck frequently.", "Emergency button inside the lift is not functioning."],
    "Electrical / Power": ["Power fluctuation in Flat {flat} causing damage.", "Main switchboard in corridor is sparking.", "Street light outside Block {block} has been broken.", "Short circuit occurred in kitchen area."],
    "Gas / Fire Safety": ["Gas leak smell in corridor of {block}.", "Fire alarm in common area is beeping constantly.", "Smoke detector in flat {flat} is malfunctioning.", "Strong gas odour near parking area."],
    "Water Leakage": ["Water leaking from ceiling of flat {flat}.", "Pipe burst in {block} common bathroom.", "Overhead tank overflowing.", "Bathroom tap leaking continuously."],
    "Plumbing / Pipe": ["Kitchen sink is completely clogged in {flat}.", "Toilet flush is broken and wasting water.", "Main valve in Block {block} is jammed."],
    "Security Issue": ["Unknown person spotted in Block {block} parking.", "CCTV camera near main gate is not working.", "Gate lock is broken.", "Security guard absent from duty at night shift."],
    "Garbage / Waste": ["Garbage bin near Block {block} entrance is overflowing.", "Garbage collection not happening on schedule.", "Construction waste dumped near Block {block}."],
    "Cleaning / Housekeeping": ["Common staircase in Block {block} not cleaned.", "Swimming pool area is very dirty.", "Corridor floors are slippery.", "Gym equipment has not been cleaned."],
    "Noise / Nuisance": ["Residents making loud noise after 11 PM.", "Party happening on terrace disturbing sleep.", "Construction work starting before 7 AM.", "Music playing at high volume in Block {block}."],
    "Internet / Network": ["Internet connection down in flat {flat}.", "Wi-Fi router in common area not working.", "Network cable in corridor is damaged.", "Intercom between flat and gate not working."]
}

REVIEW_COMMENTS = [
    "Excellent and quick service!", "Staff was polite and fixed it properly.",
    "Took a bit longer than expected, but issue is resolved.", "Very professional work.",
    "Satisfied with the quick response.", "The plumber did a great job.",
    "Could have been faster, but good overall.", "Perfect, no issues anymore.",
    "Terrible experience, issue is still there.", "Not happy with the delayed response."
]

class Command(BaseCommand):
    help = 'Seeds the AptCare database with highly diverse, timeline-accurate, zero-free data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('\n🚀 Starting Master AptCare Presentation Seeder...\n'))

        self.stdout.write('🧹 Performing Nuclear Wipe (Keeping admin "rithish")...')
        
        OTPVerification.objects.all().delete()
        Notification.objects.all().delete()
        Review.objects.all().delete()
        Escalation.objects.all().delete()
        Attachment.objects.all().delete()
        StaffPerformanceLog.objects.all().delete()
        Complaint.objects.all().delete()
        Staff.objects.all().delete()
        ComplaintCategory.objects.all().delete()
        Department.objects.all().delete()

        CustomUser.objects.exclude(username__iexact='rithish').exclude(is_superuser=True).delete()

        self.stdout.write(self.style.SUCCESS('✨ Database wiped clean.'))

        self.seed_departments()
        self.seed_categories()
        staff_objs = self.seed_staff()
        residents  = self.seed_residents()
        complaints = self.seed_time_series_complaints(residents, staff_objs)
        self.seed_escalations(complaints)
        self.seed_reviews(complaints)
        self.seed_performance_logs(staff_objs)

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeding complete! TIMELINES FIXED. Dashboards are packed with rich data.\n'))

    def seed_departments(self):
        self.dept_map = {}
        for name in DEPARTMENTS:
            obj, _ = Department.objects.get_or_create(name=name)
            self.dept_map[name] = obj

    def seed_categories(self):
        self.cat_map = {}
        for name, score, dept_name in CATEGORIES:
            dept = self.dept_map.get(dept_name)
            obj, _ = ComplaintCategory.objects.get_or_create(
                name=name, defaults={'base_score': score, 'department': dept}
            )
            self.cat_map[name] = obj

    def seed_staff(self):
        staff_objs = []
        for first, last, dept_name in STAFF_LIST:
            username = f"{first.lower()}_{last.lower()}"
            user = CustomUser.objects.create(
                username=username, email=f"{username}@aptcare.com", 
                first_name=first, last_name=last, role='staff', 
                password=make_password('Staff@1234')
            )
            dept = self.dept_map[dept_name]
            staff = Staff.objects.create(user=user, department=dept, efficiency_score=round(random.uniform(75.0, 98.0), 1))
            staff_objs.append(staff)
        return staff_objs

    def seed_residents(self):
        residents = []
        self.stdout.write('🏠 Generating diverse Residents (Active, Inactive, Pending)...')
        for block in list('AB'):
            for flat in range(101, 106):
                username = f"{block}-{flat}"
                first = random.choice(FIRST_NAMES)
                
                status_roll = random.random()
                is_active = True
                must_change = False
                
                if status_roll < 0.08:
                    is_active = False
                elif status_roll < 0.20:
                    must_change = True

                user = CustomUser.objects.create(
                    username=username, email=f"{first.lower()}{flat}{block.lower()}@{random.choice(DOMAINS)}",
                    first_name=first, last_name=random.choice(LAST_NAMES), role='user',
                    flat_number=str(flat), block=block, phone=f"+91 {random.randint(6000000000, 9999999999)}",
                    password=make_password('Resident@123'),
                    is_active=is_active,
                    must_change_password=must_change
                )
                
                if is_active:
                    residents.append(user)
                    
        return residents

    def seed_time_series_complaints(self, residents, staff_objs):
        self.stdout.write('📝 Generating Time-Warped Complaints (Bypassing auto_now_add)...')
        complaints = []
        now = timezone.now()

        def make_complaint(time_offset, status, forced_priority=None, forced_cat=None):
            resident = random.choice(residents)
            cat_name = forced_cat or random.choice(list(self.cat_map.keys()))
            cat_obj = self.cat_map[cat_name]
            
            priority = forced_priority or random.choice(['low', 'medium', 'high', 'critical'])
            score_map = {'low': random.randint(10,25), 'medium': random.randint(26,50), 'high': random.randint(51,75), 'critical': random.randint(76,99)}
            
            block = resident.block or 'A'
            flat = resident.flat_number or '101'
            desc = random.choice(COMPLAINT_DESCRIPTIONS[cat_name]).format(block=block, flat=flat)

            assigned_staff = None
            if status in ['in_progress', 'resolved', 'escalated']:
                dept_staff = [s for s in staff_objs if s.department == cat_obj.department]
                assigned_staff = random.choice(dept_staff if dept_staff else staff_objs)

            created_at = now - time_offset
            
            if status == 'resolved':
                updated_at = created_at + timedelta(hours=random.randint(2, 48))
                if updated_at > now: updated_at = now
            elif status == 'in_progress':
                updated_at = created_at + timedelta(minutes=random.randint(30, 300))
                if updated_at > now: updated_at = now
            else:
                updated_at = created_at

            # 1. Create the complaint (Django will force it to 'now')
            c = Complaint.objects.create(
                user=resident, category=cat_obj, location=f"Block {block}, Flat {flat}",
                description=desc, priority_level=priority, priority_score=score_map[priority],
                status=status, assigned_staff=assigned_staff
            )
            
            # 2. THE FIX: Update the database directly to force our past dates!
            Complaint.objects.filter(id=c.id).update(created_at=created_at, updated_at=updated_at)
            
            # Fetch the updated object back
            c.refresh_from_db()
            complaints.append(c)
            return c

        make_complaint(timedelta(hours=2), 'pending', 'critical')
        make_complaint(timedelta(hours=4), 'in_progress', 'high')
        make_complaint(timedelta(hours=6), 'resolved', 'medium')
        make_complaint(timedelta(hours=1), 'pending', 'low')

        for cat in CATEGORIES:
            make_complaint(timedelta(days=random.randint(1, 5)), 'resolved', forced_cat=cat[0])

        for _ in range(2): make_complaint(timedelta(hours=random.randint(0, 3)), 'pending')
        for _ in range(3): make_complaint(timedelta(hours=random.randint(2, 8)), 'in_progress')
        for _ in range(2): make_complaint(timedelta(hours=random.randint(5, 12)), 'resolved')

        for _ in range(3): make_complaint(timedelta(days=1, hours=random.randint(0, 23)), 'resolved')
        for _ in range(1): make_complaint(timedelta(days=1, hours=random.randint(0, 23)), 'in_progress')
        
        for _ in range(2): make_complaint(timedelta(days=2, hours=random.randint(0, 10)), 'pending', 'critical') 

        for _ in range(4): make_complaint(timedelta(days=random.randint(2, 7)), 'resolved')
        for _ in range(5): make_complaint(timedelta(days=random.randint(8, 30)), 'resolved')
        for _ in range(6): make_complaint(timedelta(days=random.randint(31, 180)), 'resolved')

        return complaints

    def seed_escalations(self, complaints):
        self.stdout.write('🚨 Generating Realistic SLA Escalations & Neglect...')
        now = timezone.now()
        
        stagnant = [c for c in complaints if c.status in ['pending', 'in_progress'] and (now - c.created_at).days >= 1]
        
        for c in stagnant[:8]: 
            c.status = 'escalated'
            c.save()
            
            sla_hours = 4 if c.priority_level == 'critical' else (12 if c.priority_level == 'high' else 24)
            deadline = c.created_at + timedelta(hours=sla_hours)
            
            e = Escalation.objects.create(
                complaint=c, 
                sla_deadline=deadline,
                reason=f"SLA breached. Expected resolution within {sla_hours} hours."
            )
            # FORCE DATE BYPASS
            Escalation.objects.filter(id=e.id).update(escalated_at=deadline + timedelta(minutes=random.randint(15, 120)))

    def seed_reviews(self, complaints):
        self.stdout.write('⭐ Seeding Analytics Reviews (Guaranteeing 1 to 5 stars)...')
        resolved = [c for c in complaints if c.status == 'resolved']
        
        forced_ratings = [1, 2, 3, 4, 5]
        for idx, rating in enumerate(forced_ratings):
            if idx < len(resolved):
                c = resolved[idx]
                r = Review.objects.create(
                    complaint=c, user=c.user, staff=c.assigned_staff,
                    rating=rating, resolved_ontime=(rating > 3),
                    fixed_properly=(rating > 2), reoccurred=(rating < 3)
                )
                # FORCE DATE BYPASS
                Review.objects.filter(id=r.id).update(created_at=c.updated_at + timedelta(hours=1))

        for c in random.sample(resolved[5:], int(len(resolved[5:]) * 0.7)):
            r = Review.objects.create(
                complaint=c, user=c.user, staff=c.assigned_staff,
                rating=random.choices([5, 4, 3, 2, 1], weights=[50, 30, 10, 5, 5])[0], 
                resolved_ontime=random.choice([True, True, True, False]), 
                fixed_properly=random.choice([True, True, True, True, False]), 
                reoccurred=False
            )
            # FORCE DATE BYPASS
            Review.objects.filter(id=r.id).update(created_at=c.updated_at + timedelta(hours=random.randint(1, 24)))

    def seed_performance_logs(self, staff_objs):
        self.stdout.write('📈 Generating Weekly/Monthly Staff Performance Logs...')
        now = timezone.now()
        
        for staff in staff_objs:
            for month_offset in range(3):
                date = now - timedelta(days=30 * month_offset)
                log = StaffPerformanceLog.objects.create(
                    staff=staff, 
                    complaints_resolved=random.randint(15, 55),
                    avg_resolution_time=round(random.uniform(1.5, 6.0), 1)
                )
                # If your log model has a created_at field, force the date:
                if hasattr(log, 'created_at'):
                    StaffPerformanceLog.objects.filter(id=log.id).update(created_at=date)