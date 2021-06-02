# -*- coding: utf-8 -*-
#
# a simple Python script that,
#
#   * reformats the raw TAB-separated value file from Google Forms into a final
#     data input (removes sensitive columns, adds new summary columns, fixes
#     typos in country names, etc.)
#   * generates an output format that covers free-form text from a manually
#     curated list of responses.

import os
import sys
import anvio.utils as u

if not os.path.exists('mentorship-RAW.tsv'):
    if os.path.exists('mentorship.tsv'):
        print("You don't seem to have the raw input file available in this directory. But you do have "
              "the formatted output. Well. GOOD. All OK, but there will be no data for wisdom.")
        sys.exit()
    else:
        print("You don't seem to have either `mentorship-raw.tsv`, nor the `mentorship.tsv` (which is "
              "generated from the `mentorship-raw.tsv` by this program) in this directory. Something "
              "is wrong here but you can always reach out to meren at uchicago.edu.")

        sys.exit(-1)


# read the raw data.
m = u.get_TAB_delimited_file_as_dictionary('mentorship-RAW.tsv')

# we will use this dictionary to turn crappy Google Forms keys into single-word
# keys for our sanity:
keys = {'You are currently':
            "mentee_current",
        'You worked (or are still working) with the mentor you have in mind as:':
            "mentee_then",
        'Your mentor was (or is):':
            "mentor_then",
        'If you had to chose one, which one of the following categories would best describe your relationship with science as an ECR or when you were an ECR?':
            "discipline",
        'How would you describe your ECR expertise? (e.g., Microbial Ecologist, Biochemist, Computer Scientist, Civil Engineer, etc.)':
            "expertise",
        'Please chose your gender (if you are no longer a trainee, respond with your gender at the time you were a trainee). The purpose of this question is to generate enough data, if possible, to not completely miss issues related or specific to gender.':
            "mentee_gender",
        "Please chose, to the best of your knowledge, your mentor's gender (similar to the previous one, this question is here in an attempt to generate enough data to not completely miss mentorship patterns related or specific to gender).":
            "mentor_gender",
        'Where were you (or still are) working as an ECR? Please enter a country name (please avoid using acronyms and spell out the full country name in English (i.g., United States, United Kingdom, Mexico, etc)).':
            "country",
        'If you are/were in the United States, which state? (please avoid using acronyms (i.e., Illinois, Massachusetts, etc)). Leave this blank if you were/are not working in the United Sates OR if you think this information, combined with your other responses, can identify you.':
            "state",
        'Except your gender, were you / are you a member of a minority group in your workplace based on your ethnic background and/or religion?':
            "mentee_minority",
        'Except their gender, and to the best of your knowledge, was/is your mentor a member of a minority group in the workplace based on their ethnic background and/or religion?':
            "mentor_minority",
        'Considering its entirety and its influence on your wellbeing and career, how would you characterize your experience with your mentor?':
            "experience_with_mentor",
        'Do you think your mentor was (or is) considered a good scientist by their colleagues?':
            "mentor_seen_by_colleagues",
        'How many trainees your mentor was (or is) responsible for during the time you worked with them as an ECR (or currently, if you are still advised by this mentor)?':
            "mentor_num_trainees",
        'On average, how much time your mentor was (or is) able to dedicate to you for 1-on-1 interactions outside of group meetings?':
            "mentor_mentee_meeting_time",
        'Was/is your experience with your mentor comparable to the experience of the other trainees who worked/are working with them?':
            "mentee_experience_was_common",
        'To what extent did/does your mentor encourage you to define your project or influence its trajectory?':
            "mentee_influence_on_project",
        'Do you think your mentor is/was aware of their shortcomings in mentoring trainees?':
            "mentor_awareness_on_shortcomings",
        'Do you think your mentor is/was aware of their strengths in mentoring trainees?':
            "mentor_awareness_on_strengths",
        'How frequently did/does your mentor ask for feedback from their trainees on their mentorship style?':
            "mentor_asking_feedback",
        "Do you think your mentor made/makes it easy for their trainees to raise their concerns about the mentorship they're receiving?":
            "mentor_makes_easy_mentees_to_raise_concerns",
        'Was/is there a public document defining the code of conduct, expectations, or the group culture provided by your mentor?':
            "code_of_conduct",
        'What is/was the BIGGEST SHORTCOMING of their mentorship style? Please consider describing how did (or does) this shortcoming influence your work, your wellbeing, or your career (you can list multiple, but please list each shortcoming and its influence as a separate paragraph).':
            "mentor_biggest_shortcomings",
        'What is/was the MOST ADMIRABLE trait of their mentorship style? Please consider describing how this trait positively influenced (or influences) your daily work, your wellbeing, or your career (you can list multiple, but please list each shortcoming and its influence as a separate paragraph).':
            "mentor_biggest_strengths",
        'Based on your experience, what advice would you give to your mentor so they could do better?':
            "mentee_advice_to_mentor",
        'Based on your experience, what advice would you give to those who are getting ready to pursue a career in science and are looking for mentors?':
            "mentee_advice_to_mentees"}

# the headers we wish to report in the output file we will generate from the raw input:
headers = ["timestamp", "mentee_current",  "mentee_current_summary", "mentee_then", "mentor_then",
           "discipline", "mentee_gender", "mentor_gender", "country", "mentee_minority",
           "mentor_minority", "experience_with_mentor", "mentor_seen_by_colleagues",
           "mentor_num_trainees", "mentor_mentee_meeting_time", "mentee_experience_was_common",
           'mentee_experience_was_common_summary', "mentee_influence_on_project",
           "mentor_awareness_on_shortcomings", "mentor_awareness_on_shortcomings_summary",
           "mentor_awareness_on_strengths", "mentor_awareness_on_strengths_summary",
           "mentor_asking_feedback", 'mentor_has_ever_asked_feedback',
           "mentor_makes_easy_mentees_to_raise_concerns",
           "mentor_makes_easy_mentees_to_raise_concerns_summary", "code_of_conduct"]

# the poor man's loop to summarize complex answers into simpler ones, and to
# fix typos (i.e, those in country names)
d = {}
for k in m:
    d[k] = {}
    for key in m[k]:
        d[k][keys[key]] = m[k][key]

        if keys[key] == 'mentor_seen_by_colleagues':
            if m[k][key] == "I don't know / Prefer not to comment":
                d[k][keys[key]] = "No comment"
            elif m[k][key].startswith('No'):
                d[k][keys[key]] = "Not considered good"
            elif m[k][key].startswith('Yes'):
                d[k][keys[key]] = "Considered good"


        if keys[key] in ['mentee_experience_was_common']:
            if m[k][key] in ["1", "2"]:
                d[k]['mentee_experience_was_common_summary'] = "Specific to few"
            elif m[k][key] in ["4", "5"]:
                d[k]['mentee_experience_was_common_summary'] = "Common to most"
            else:
                d[k]['mentee_experience_was_common_summary'] = None


        if keys[key] in ['mentor_awareness_on_shortcomings']:
            if m[k][key] in ["1", "2"]:
                d[k]['mentor_awareness_on_shortcomings_summary'] = "Aware"
            elif m[k][key] in ["4", "5"]:
                d[k]['mentor_awareness_on_shortcomings_summary'] = "Not Aware"
            else:
                d[k]['mentor_awareness_on_shortcomings_summary'] = "Neutral"


        if keys[key] in ['mentor_awareness_on_strengths']:
            if m[k][key] in ["1", "2"]:
                d[k]['mentor_awareness_on_strengths_summary'] = "Aware"
            elif m[k][key] in ["4", "5"]:
                d[k]['mentor_awareness_on_strengths_summary'] = "Not Aware"
            else:
                d[k]['mentor_awareness_on_strengths_summary'] = "Neutral"


        if keys[key] in ['mentor_makes_easy_mentees_to_raise_concerns']:
            if m[k][key] in ["1", "2"]:
                d[k]['mentor_makes_easy_mentees_to_raise_concerns_summary'] = "Made it difficult"
            elif m[k][key] in ["4", "5"]:
                d[k]['mentor_makes_easy_mentees_to_raise_concerns_summary'] = "Made it easy"
            else:
                d[k]['mentor_makes_easy_mentees_to_raise_concerns_summary'] = "Neutral"


        if keys[key] == 'discipline':
            d[k][keys[key]] = m[k][key][:m[k][key].find('(') - 1].title()


        if keys[key] in ['mentor_asking_feedback']:
            if m[k][key] == "Never":
                d[k]['mentor_has_ever_asked_feedback'] = "No"
            else:
                d[k]['mentor_has_ever_asked_feedback'] = "Yes"

        if keys[key] in ['mentee_current']:
            if m[k][key] == "an Associate Professor (or equivalent)":
                d[k]['mentee_current_summary'] = "Academic (Non-ECR)"
            elif m[k][key] == "a Graduate Student":
                d[k]['mentee_current_summary'] = "Academic (ECR)"
            elif m[k][key] == "a Postdoctoral Researcher":
                d[k]['mentee_current_summary'] = "Academic (ECR)"
            elif m[k][key] == "an Assistant Professor (or equivalent)":
                d[k]['mentee_current_summary'] = "Academic (Non-ECR)"
            elif m[k][key] == "an Assistant Professor  (or equivalent)":
                d[k]['mentee_current_summary'] = "Academic (Non-ECR)"
            elif m[k][key] == "a Professor (or equivalent)":
                d[k]['mentee_current_summary'] = "Academic (Non-ECR)"
            elif m[k][key] == "working in academia as a non-ECR":
                d[k]['mentee_current_summary'] = "Academic (Non-ECR)"
            elif m[k][key] == "other / prefer not to say":
                d[k]['mentee_current_summary'] = "Non-Academic"
            elif m[k][key] == "working in industry":
                d[k]['mentee_current_summary'] = "Non-Academic"
            else:
                d[k]['mentee_current_summary'] = m[k][key]


        if keys[key] in ['mentor_then', 'mentee_current', 'mentee_then']:
            if m[k][key] == "an Associate Professor (or equivalent)":
                d[k][keys[key]] = "Associate Prof"
            elif m[k][key] == "a Graduate Student":
                d[k][keys[key]] = "Grad student"
            elif m[k][key] == "a Postdoctoral Researcher":
                d[k][keys[key]] = "Postdoc"
            elif m[k][key] == "an Assistant Professor (or equivalent)":
                d[k][keys[key]] = "Assistant Prof"
            elif m[k][key] == "an Assistant Professor  (or equivalent)":
                d[k][keys[key]] = "Assistant Prof"
            elif m[k][key] == "a Professor (or equivalent)":
                d[k][keys[key]] = "Full Prof"
            elif m[k][key] == "working in academia as a non-ECR":
                d[k][keys[key]] = "Non-ECR academic"
            elif m[k][key] == "other / prefer not to say":
                d[k][keys[key]] = "Other"
            else:
                d[k][keys[key]] = m[k][key]


        if keys[key] == 'mentor_num_trainees':
            if m[k][key] == "Less than 5":
                d[k][keys[key]] = "<5"
            elif m[k][key] == "More than 20":
                d[k][keys[key]] = ">15"
            elif m[k][key] == "15-20":
                d[k][keys[key]] = ">15"
            else:
                d[k][keys[key]] = m[k][key]

        if keys[key] == 'mentor_asking_feedback' and m[k][key] == "More frequently":
            d[k][keys[key]] = "Frequently"

        if keys[key] == 'country':
            if m[k][key].lower().find('states') > 0 or m[k][key].lower().find('oregon') >= 0 or m[k][key].lower().strip() == 'us':
                d[k][keys[key]] = "United States"
            elif m[k][key].lower().find('kingdom') > 0 or m[k][key].lower().strip() == "uk":
                d[k][keys[key]] = "United Kingdom"
            elif m[k][key].lower().find('india') >= 0:
                d[k][keys[key]] = "India"
            elif m[k][key].lower().find('netherl') >= 0:
                d[k][keys[key]] = "The Netherlands"
            elif m[k][key].lower().find('canada') >= 0:
                d[k][keys[key]] = "Canada"
            elif m[k][key].lower().find('germ') >= 0 or m[k][key].lower() == 'gernany':
                d[k][keys[key]] = "Germany"
            elif m[k][key].lower().find('china') >= 0:
                d[k][keys[key]] = "China"
            elif m[k][key].lower().find('korea') >= 0:
                d[k][keys[key]] = "South Korea"
            elif m[k][key].lower().find('asia') >= 0 or m[k][key].lower().find('europe') >= 0:
                d[k][keys[key]] = "[none entered]"
            else:
                d[k][keys[key]] = m[k][key].strip().title()

        if keys[key] == "mentee_gender" or keys[key] == "mentor_gender":
            if m[k][key].lower().find('queer') > 0:
                d[k][keys[key]] = "Queer / Non-conforming"

# report the kraken!
u.store_dict_as_TAB_delimited_file(d, 'mentorship.tsv', headers=headers)

# the rest of this code is to report statements in a reproducible fashion.
wisdom_keys = ["mentor_biggest_shortcomings", "mentor_biggest_strengths", "mentee_advice_to_mentor", "mentee_advice_to_mentees"]
wisdom_questions = {"mentor_biggest_shortcomings": """In this section you will find the words of ECRs to describe '<b>the BIGGEST SHORTCOMING of the mentorship they have received</b>' from a mentor of theirs, considering how did this shortcoming influenced their work, wellbeing, and/or career. You will see that even mentees who overall had a positive experience with their mentors suffered from some aspects of the mentorship they have received.""",
                    "mentor_biggest_strengths"   : """In this section you will find the words of ECRs to describe '<b>the MOST ADMIRABLE aspect of the mentorship they have received</b>' from a mentor of theirs, considering how did this shortcoming influenced their work, wellbeing, and/or career. You will see that even mentees who had a negative experience with their mentor had benefited from some aspects of the mentorship style they have received.""",
                    "mentee_advice_to_mentor"    : 'In this section you will find the words of ECRs to describe the advice they would have given to their mentor so they could do better.',
                    "mentee_advice_to_mentees"   : 'In this section you will find the words of ECRs to describe what advice they would have given to those who are getting ready to pursue a career in science and are looking for mentors.'}

wisdom_subtitles = {"mentor_biggest_shortcomings": 'Mentees report on biggest shortcomings of their mentors',
                    "mentor_biggest_strengths"   : 'Mentees report on biggest strengths of their mentors',
                    "mentee_advice_to_mentor"    : 'Mentees advise their mentors to do better',
                    "mentee_advice_to_mentees"   : 'Mentees advise future mentees'}

# this information is read from an output file we generate AFTER going through
# the CURATED `mentorship_wisdom_all.txt` that will be generated in the next loop.
# if you are confused, read the next set of comments.
if os.path.exists('mentorship_wisdom_keys_to_keep.txt'):
    mentorship_wisdom_keys_to_keep = set([l.strip() for l in open('mentorship_wisdom_keys_to_keep.txt').readlines()])
else:
    mentorship_wisdom_keys_to_keep = set([])

# report all remarks, which is to survey and choose the ones that should be
# reported (essentially we opened the file in EXCEL, and removed the letter
# `R` from the second column of those we wished to keep and updated the
# variable `mentorship_wisdom_keys_to_keep` with those keys)
with open('mentorship_wisdom_all.txt', 'w') as f:
    for key in wisdom_keys:
        for timestamp in d:
            v = d[timestamp]
            if v[key]:
                wisdom = v[key].strip().strip('-')

                identifier = f"{key}!{timestamp}"

                if identifier in mentorship_wisdom_keys_to_keep:
                    status = ''
                else:
                    status = 'R'

                f.write(f"{identifier}\t{status}\t{wisdom}\n")


# keep the ones set to be kept, and report a markdown formatted output that
# is included from the blog post.
with open('mentorship_wisdom.md', 'w') as f:
    f.write("## The words of early career researchers\n\n")
    for key in wisdom_keys:
        f.write(f'### {wisdom_subtitles[key]}\n\n')
        f.write(f'{wisdom_questions[key]}\n\n')
        for timestamp in d:
            identifier = f"{key}!{timestamp}"

            if identifier not in mentorship_wisdom_keys_to_keep:
                continue

            v = d[timestamp]

            if v[key]:
                if v['mentee_gender'] not in ['Man', 'Woman']:
                    continue

                wisdom = v[key].strip()
                wisdom = wisdom.replace('   ', '  ').replace('   ', '  ').replace('   ', '  ').replace('  ', '<br /><br />')

                G = f"{'♂' if v['mentee_gender'] == 'Man' else '♀'}"
                g = f"{'♂' if v['mentor_gender'] == 'Man' else '♀'}"

                if v['experience_with_mentor'] == "1":
                    E = """a <span style="color:red;">very negative experience</span>"""
                elif v['experience_with_mentor'] == "2":
                    E = """a <span style="color:red;">very negative experience</span>"""
                elif v['experience_with_mentor'] == "4":
                    E = """a <span style="color:green;">positive experience</span>"""
                elif v['experience_with_mentor'] == "5":
                    E = """a <span style="color:green;">very positive experience</span>"""
                else:
                    E = """a <span style="color:orange;">neutral experience</span>"""

                if key == 'mentor_biggest_shortcomings':
                    R = f"reporting on the <b>biggest shortcomings</b> of their mentor ({g})"
                elif key == 'mentor_biggest_strengths':
                    R = f"reporting on the <b>most admirable qualities</b> of their mentor ({g})"
                elif key == 'mentee_advice_to_mentor':
                    R = f"shares <b>their advice</b> for their mentor ({g})"
                elif key == 'mentee_advice_to_mentees':
                    R = "shares <b>their advice</b> for future mentees"

                f.write("<blockquote>\n")
                f.write(f"{wisdom}\n")
                f.write(f'<div class="blockquote-author"><b>{v["mentee_then"]}</b> ({G}) had {E} in <b>{v["country"]}</b><br />{R}</div>\n')
                f.write("</blockquote>\n\n")
