"""
make_dataset.py
----------------
Generates student_queries.csv : the knowledge base used by the chatbot.
Each row = one (category, question, answer) triple.
Run once to (re)create the CSV used by the notebook.
"""

import csv

data = [
# ---------------- ADMISSIONS ----------------
("Admissions", "How can I apply for admission to the college?", "You can apply online through the official college admission portal by filling the application form and uploading the required documents."),
("Admissions", "What is the last date for admission?", "The last date for admission is usually announced on the college website; generally applications close by the second week of July."),
("Admissions", "What documents are required for admission?", "You need your 10th and 12th mark sheets, transfer certificate, migration certificate, category certificate (if applicable), and passport size photographs."),
("Admissions", "Is there an entrance exam for admission?", "Yes, admission to most B.Tech programs is based on JEE Main or the respective state-level engineering entrance exam score."),
("Admissions", "What is the eligibility criteria for B.Tech admission?", "Candidates must have passed 10+2 with Physics, Chemistry and Mathematics, securing at least 45% to 50% aggregate marks depending on category."),
("Admissions", "Can I get admission through lateral entry?", "Yes, diploma holders and B.Sc graduates can apply for lateral entry directly into the second year of the B.Tech program."),
("Admissions", "How do I check my admission status?", "You can check your admission status by logging into the student portal using your application number and date of birth."),
("Admissions", "Is management quota admission available?", "Yes, a limited number of seats are available under the management quota; please contact the admissions office for details."),
("Admissions", "What branches are offered in B.Tech?", "The college offers B.Tech in Computer Science, Information Technology, Electronics, Mechanical, Civil, and Electrical Engineering."),
("Admissions", "How can I contact the admissions office?", "You can contact the admissions office via the phone number and email listed on the college website's 'Contact Us' page."),

# ---------------- FEES ----------------
("Fees", "What is the total fee for the B.Tech course?", "The total fee varies by branch and category; please refer to the official fee structure document on the college website for exact figures."),
("Fees", "How can I pay my college fees?", "Fees can be paid online through the student portal using net banking, debit card, credit card, or UPI."),
("Fees", "Is there an option to pay fees in installments?", "Yes, the college allows fee payment in two or four installments per academic year; check with the accounts office for the schedule."),
("Fees", "What happens if I miss the fee payment deadline?", "A late fee penalty will be charged, and continued non-payment may lead to suspension of library and exam privileges."),
("Fees", "Are there any fee concessions for economically weaker students?", "Yes, fee concessions and scholarships are available for economically weaker section students who meet the eligibility criteria."),
("Fees", "How do I get a fee receipt after payment?", "A digital fee receipt is automatically generated and available for download from the student portal after successful payment."),
("Fees", "Is hostel fee included in the tuition fee?", "No, hostel fee is charged separately from the tuition fee and must be paid before the start of each semester."),
("Fees", "Can I get a refund if I withdraw admission?", "Refunds are processed as per UGC/AICTE refund rules; the amount refunded depends on the date of withdrawal."),
("Fees", "Is there a fine for late semester registration?", "Yes, a late registration fine is applicable if you register after the specified deadline for the semester."),
("Fees", "Where can I see the detailed fee structure?", "The detailed fee structure for every branch and year is published under the 'Admissions' section of the college website."),

# ---------------- HOSTEL ----------------
("Hostel", "How can I apply for hostel accommodation?", "You can apply for hostel accommodation by filling the hostel application form available on the student portal after admission confirmation."),
("Hostel", "What facilities are available in the hostel?", "Hostels provide furnished rooms, Wi-Fi, mess facilities, laundry, 24/7 security, and common recreation rooms."),
("Hostel", "Is there separate hostel for boys and girls?", "Yes, the college has separate hostel blocks for boys and girls with independent wardens and security staff."),
("Hostel", "What is the hostel curfew time?", "The general hostel curfew time is 9:30 PM on weekdays and 10:30 PM on weekends, subject to warden discretion."),
("Hostel", "Can I change my hostel room?", "Room changes are allowed only at the start of a semester and require warden approval based on availability."),
("Hostel", "Is mess food included in hostel fees?", "Yes, mess charges are usually included in the hostel fee package, though some colleges bill mess separately."),
("Hostel", "What should I do if I face a hostel-related problem?", "You should report the issue to your hostel warden or the Dean of Student Welfare office for prompt resolution."),
("Hostel", "Are guests allowed to stay in the hostel?", "Guests are generally not allowed to stay overnight; day visitors must register at the hostel reception."),
("Hostel", "Is medical assistance available in the hostel?", "Yes, hostels have a tie-up with the college medical center and nearby hospitals for emergency assistance."),
("Hostel", "How do I apply for hostel leave?", "You can apply for hostel leave through the hostel management app or by submitting a leave form to the warden."),

# ---------------- LIBRARY ----------------
("Library", "What are the library timings?", "The library is open from 8:00 AM to 8:00 PM on all working days and 9:00 AM to 5:00 PM on Saturdays."),
("Library", "How many books can I borrow at a time?", "Undergraduate students can borrow up to 3 books at a time for a period of 14 days."),
("Library", "How do I renew a borrowed book?", "You can renew a borrowed book online through the library management portal, provided no one else has reserved it."),
("Library", "What is the fine for late return of books?", "A fine of a few rupees per day is charged for each day the book is returned after the due date."),
("Library", "Does the library provide access to e-books and journals?", "Yes, the library provides access to a wide range of e-books, e-journals, and research databases through its digital library."),
("Library", "Can I reserve a book that is already issued?", "Yes, you can place a reservation on an issued book, and you will be notified once it becomes available."),
("Library", "Is there a separate reading room in the library?", "Yes, the library has a dedicated silent reading room for focused study and exam preparation."),
("Library", "How do I get a library card?", "A library card is issued automatically at the time of admission along with your student ID card."),
("Library", "What happens if I lose a library book?", "You will need to pay the cost of the book along with a processing fee to replace the lost item."),
("Library", "Can alumni access the library?", "Alumni can access the library for reference purposes by registering as an external member with the librarian."),

# ---------------- EXAMINATION ----------------
("Examination", "When will the semester exams be conducted?", "Semester exams are usually conducted at the end of each semester as per the academic calendar published by the college."),
("Examination", "How can I download my admit card?", "You can download your admit card from the examination portal a few days before the exams begin, after clearing dues."),
("Examination", "What is the passing criteria for a subject?", "Students generally need to score at least 40% marks in both internal and external examinations to pass a subject."),
("Examination", "How can I apply for revaluation of answer sheets?", "You can apply for revaluation online through the examination portal within the specified window after result declaration."),
("Examination", "What happens if I fail in a subject?", "If you fail in a subject, you will need to appear for the supplementary or backlog examination in the next cycle."),
("Examination", "How can I check my exam results?", "Results are published on the college examination portal; you can check them using your roll number and date of birth."),
("Examination", "Is there a minimum attendance requirement to sit for exams?", "Yes, students generally need a minimum of 75% attendance to be eligible to appear for semester examinations."),
("Examination", "How do I apply for a duplicate mark sheet?", "You can apply for a duplicate mark sheet by submitting a written request along with the prescribed fee to the examination cell."),
("Examination", "What is the syllabus for the upcoming exams?", "The detailed syllabus for each subject is available on the college website under the academics or examination section."),
("Examination", "Can I get exam form correction done?", "Yes, exam form correction can be requested within the correction window announced along with the exam schedule."),

# ---------------- PLACEMENTS ----------------
("Placements", "When do campus placements begin?", "Campus placements typically begin in the pre-final year around August and continue through the final year."),
("Placements", "Which companies visit the campus for placements?", "Companies from IT, core engineering, and consulting sectors regularly visit the campus; the list is updated on the placement cell website."),
("Placements", "What is the eligibility criteria for placements?", "Students generally need a minimum CGPA of 6.0 and no active academic backlogs to be eligible for placement drives."),
("Placements", "How can I register for placement drives?", "You can register for placement drives through the Training and Placement Cell portal using your student credentials."),
("Placements", "Does the college provide placement training?", "Yes, the college conducts aptitude tests, mock interviews, group discussions, and resume-building workshops before placement season."),
("Placements", "What is the average placement package offered?", "The average package varies by branch and year; exact statistics are published in the annual placement report by the T&P cell."),
("Placements", "Can I sit for multiple companies in the same season?", "Placement policies vary; generally once a student accepts an offer from one company, further participation may be restricted."),
("Placements", "Does the college help with internships?", "Yes, the Training and Placement Cell also facilitates summer and winter internships with partner companies."),
("Placements", "Who should I contact for placement-related queries?", "You should contact the Training and Placement Officer (TPO) or visit the placement cell office for any placement-related queries."),
("Placements", "Are there separate placement drives for higher studies aspirants?", "Students planning higher studies can seek guidance from the placement cell for GRE, GATE, and university application support."),

# ---------------- SCHOLARSHIPS ----------------
("Scholarships", "What scholarships are available for students?", "Scholarships are available based on merit, government schemes, and financial need; details are listed on the college scholarship page."),
("Scholarships", "How can I apply for a merit scholarship?", "You can apply for a merit scholarship by submitting your previous semester marksheet and application form to the scholarship cell."),
("Scholarships", "Is there a scholarship for SC/ST/OBC students?", "Yes, government scholarships for SC, ST, and OBC students are available and can be applied through the National Scholarship Portal."),
("Scholarships", "What is the eligibility for a sports scholarship?", "Students who have represented at state or national level in sports are eligible to apply for a sports scholarship."),
("Scholarships", "How do I check my scholarship application status?", "You can check your scholarship application status by logging into the National Scholarship Portal or the college scholarship cell portal."),
("Scholarships", "Are scholarships renewed every year?", "Yes, most scholarships are renewed annually provided the student maintains the required academic performance."),
("Scholarships", "Can international students apply for scholarships?", "International students may be eligible for specific scholarships; please check with the international student cell for details."),
("Scholarships", "What documents are needed for scholarship application?", "You typically need income certificate, caste certificate (if applicable), previous marksheets, and bank account details."),
("Scholarships", "Is there a scholarship for economically weaker sections?", "Yes, the college and government both offer scholarships specifically for economically weaker section students."),
("Scholarships", "Whom should I contact for scholarship queries?", "You can contact the Scholarship Cell or the Dean of Student Welfare office for any scholarship-related queries."),

# ---------------- FACULTY INFORMATION ----------------
("Faculty", "How can I find my faculty advisor's contact details?", "Faculty advisor details along with contact information are shared during orientation and are also listed on the department notice board."),
("Faculty", "How do I contact a professor for doubts?", "You can contact a professor during their office hours or via the official email address listed on the department website."),
("Faculty", "Who is the Head of Department for Computer Science?", "The Head of Department details are listed on the respective department page of the official college website."),
("Faculty", "How can I schedule a meeting with a faculty member?", "You can schedule a meeting by emailing the faculty member directly or visiting during their published office hours."),
("Faculty", "Where can I find faculty qualifications and research areas?", "Faculty qualifications and research interests are published on the department's faculty profile page on the college website."),
("Faculty", "Who can I approach for a certificate signed by a faculty member?", "You can approach your class coordinator, mentor, or Head of Department to get certificates signed and attested."),
("Faculty", "Is there a faculty mentorship program for students?", "Yes, every student is assigned a faculty mentor for academic and personal guidance throughout their course."),
("Faculty", "How do I raise a complaint against a faculty member?", "Complaints can be raised confidentially through the Dean of Academics office or the Grievance Redressal Cell."),
("Faculty", "Can faculty members guide me for research projects?", "Yes, faculty members regularly guide students for mini projects, major projects, and research publications."),
("Faculty", "Where can I find the visiting faculty schedule?", "The visiting faculty schedule is displayed on the department notice board and shared through official class groups."),

# ---------------- ACADEMIC CALENDAR ----------------
("Academic Calendar", "Where can I find the academic calendar?", "The academic calendar is published on the college website under the Academics section at the start of every academic year."),
("Academic Calendar", "When do the semester classes begin?", "Semester classes usually begin in the first week of August for odd semesters and January for even semesters."),
("Academic Calendar", "When is the winter break scheduled?", "The winter break is generally scheduled between mid-December and early January, as per the academic calendar."),
("Academic Calendar", "When is the summer vacation?", "Summer vacation typically falls between May and June after the completion of even semester examinations."),
("Academic Calendar", "How can I know about upcoming college holidays?", "Upcoming holidays are listed in the academic calendar and also announced through official notices and the student portal."),
("Academic Calendar", "When do mid-semester exams take place?", "Mid-semester exams are usually conducted around the eighth or ninth week of each semester as per the calendar."),
("Academic Calendar", "Is there a fixed schedule for orientation week?", "Yes, orientation week for new students is scheduled in the first week of the academic session, as noted in the calendar."),
("Academic Calendar", "When are the practical/lab exams scheduled?", "Practical and lab examinations are usually scheduled a week before the theory examinations begin."),
("Academic Calendar", "How can I know the last working day of the semester?", "The last working day of the semester is clearly mentioned in the official academic calendar document."),
("Academic Calendar", "Where can I check dates for club and cultural events?", "Dates for club and cultural events are published separately by the Student Activity Council and shared via notices."),

# ---------------- COLLEGE TIMINGS ----------------
("College Timings", "What are the general college working hours?", "The college generally operates from 9:00 AM to 4:30 PM on all working days, Monday through Friday."),
("College Timings", "Is the college open on Saturdays?", "Some departments and the library remain open with limited hours on Saturdays; classes are usually not held."),
("College Timings", "What time do classes start in the morning?", "Regular classes typically start at 9:00 AM with the first period, followed by short breaks between periods."),
("College Timings", "How long is the lunch break?", "The lunch break is usually 45 minutes to 1 hour long, generally scheduled around 12:30 PM to 1:30 PM."),
("College Timings", "Are the college office timings different from class timings?", "Yes, the administrative office generally operates from 9:30 AM to 5:00 PM, slightly different from class timings."),
("College Timings", "What are the lab timings?", "Lab sessions are usually scheduled for 2 to 3 hour blocks within the regular class schedule, as per the timetable."),
("College Timings", "Is the campus open during weekends for project work?", "Certain labs and the library may remain open on weekends for project work with prior permission from faculty."),
("College Timings", "What time does the college close in the evening?", "The college campus generally closes by 6:00 PM, though hostel residents can access common areas until curfew time."),
("College Timings", "Are there any changes in timing during exams?", "Yes, during examination periods, class timings are usually reduced or rescheduled to accommodate exam sessions."),
("College Timings", "Where can I find my personalized class timetable?", "Your personalized class timetable is available on the student portal under the 'Timetable' section."),

# ---------------- STUDENT SUPPORT SERVICES ----------------
("Student Support", "Whom should I contact for general student support?", "You can contact the Student Support Office located in the administrative block, or email the support desk listed on the website."),
("Student Support", "Is counseling support available for students?", "Yes, the college provides free counseling services through the Student Wellness Center for academic and personal concerns."),
("Student Support", "How do I report ragging or harassment?", "Ragging or harassment can be reported immediately to the Anti-Ragging Committee or through the anonymous complaint box on campus."),
("Student Support", "Is there a helpline for student emergencies?", "Yes, the college has a 24/7 emergency helpline number displayed on the notice boards and the college website."),
("Student Support", "How can I get a bonafide certificate?", "You can request a bonafide certificate by submitting an online application through the student portal or the registrar's office."),
("Student Support", "Where can I submit a complaint or grievance?", "Complaints and grievances can be submitted through the Grievance Redressal Cell portal or in person at the Dean's office."),
("Student Support", "Does the college have a student union or council?", "Yes, the college has an elected Student Council that represents student interests and organizes various activities."),
("Student Support", "How can I get technical support for the student portal?", "Technical issues with the student portal can be reported to the IT Help Desk via email or the support ticket system."),
("Student Support", "Are there support services for differently-abled students?", "Yes, the college provides accessibility support, including ramps, assistive technology, and dedicated staff for differently-abled students."),
("Student Support", "How can I get a transcript or transfer certificate?", "Transcripts and transfer certificates can be requested through the registrar's office by submitting the prescribed application form."),

# ---------------- GREETINGS / SMALL TALK (helps chatbot feel natural) ----------------
("Greeting", "hi", "Hello! I am your Student Support Assistant. How can I help you today?"),
("Greeting", "hello", "Hi there! Feel free to ask me anything about admissions, fees, hostel, exams, or other student services."),
("Greeting", "good morning", "Good morning! How can I assist you with your student queries today?"),
("Greeting", "good afternoon", "Good afternoon! What would you like to know about our college services?"),
("Greeting", "good evening", "Good evening! I'm here to help with any student support questions you have."),
("Greeting", "how are you", "I'm doing great and ready to help! What question can I answer for you?"),
("Greeting", "thank you", "You're welcome! Let me know if you have any other questions."),
("Greeting", "thanks", "You're welcome! Happy to help anytime."),
("Greeting", "bye", "Goodbye! Feel free to come back if you have more questions. Have a great day!"),
("Greeting", "exit", "Thank you for using the Student Support Chatbot. Goodbye!"),
]

with open("student_queries.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["category", "question", "answer"])
    writer.writerows(data)

print(f"Dataset created with {len(data)} question-answer pairs.")
