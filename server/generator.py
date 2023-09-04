
import os
import openai
import smtplib
from flask import Flask, request, jsonify
from flask_cors import CORS
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("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")

openai.api_key = "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"


def generate_sop(user_responses):
    prompt = f" Generate a Statement of Purpose (SOP) letter to apply for {user_responses['canadaInstitute']}. Following are my details. you may take them to create a SOP for me. \n\n"
    prompt += f"My name is {user_responses['fullName']} and I am {user_responses['age']} years old. "
    prompt += f"I completed my {user_responses['educationLevel']} in {user_responses['institute']} with a major in {user_responses['studyField']}. "
    
    if user_responses['hasWorkExperience'] == 'Yes':
        prompt += f"I have {user_responses['jobTitle']} experience at {user_responses['companyName']} where I worked as a {user_responses['jobDuties']}. "
    
    prompt += f"I have been admitted to {user_responses['canadaInstitute']} for a {user_responses['programOfStudy']} program. "
    prompt += f"I am applying from {user_responses['applyingFrom']} and my future goals are {user_responses['futureGoals']}. "
    
    if user_responses['hasCompletedIELTS'] == 'Yes':
        prompt += f"I cleared the IELTS exam with a score of Listening: {user_responses['ieltsListening']}, Reading: {user_responses['ieltsReading']}, Speaking: {user_responses['ieltsSpeaking']}, and Writing: {user_responses['ieltsWriting']}. "
    
    if user_responses['paidFirstYearTuition'] == 'Yes':
        prompt += f"I have paid the first-year tuition fee of {user_responses['tuitionFee']} INR. "
    
    if user_responses['hasGIC'] == 'Yes':
        prompt += f"I also completed the Guaranteed Investment Certificate (GIC) by paying {user_responses['gicAmount']} INR. "

    prompt += f"\nStatement of Purpose:\n"
    prompt += f"{'-' * 40}\n\n"

    response = openai.Completion.create(
        engine="text-davinci-002", 
        prompt=prompt,
        max_tokens=2000,  
        temperature=0.7, 
        n=1,
        stop=None,
    )

    generated_sop = response.choices[0].text.strip()
    return generated_sop

def send_email(email, sop_text):
    my_mail = "mofusa.softwaretesting@gmail.com"
    passcode = "sncmgmcgvnajxcmf"

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    connection = smtplib.SMTP(smtp_server, smtp_port)
    connection.starttls()
    connection.login(user=my_mail, password=passcode)
    
    
    msg = MIMEMultipart()
    msg["From"] = my_mail
    msg["To"] = email 
    msg["Subject"] = "Your Statement of Purpose (SOP)"


    msg.attach(MIMEText(sop_text, "plain"))

    try:
        connection.sendmail(from_addr=my_mail, to_addrs=email, msg=msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print("Something went wrong:", e)

    connection.quit()

@app.route("/generate-sop", methods=['POST', 'GET'])
def generate_and_send_sop():
    if request.method == 'POST':
        try:
            content_type = request.headers.get("Content-Type")
            if content_type != "application/json":
                return jsonify({"error": "Invalid Content-Type"}), 400

            user_data = request.json
            print("Received JSON Data:", user_data)

            sop_text = generate_sop(user_data)

            send_email(user_data["email"], sop_text)

            print("message : SOP generated and sent successfully!")
            return jsonify({"message": "SOP generated and sent successfully!"})

        except Exception as e:
            return jsonify({"error": str(e)})
    elif request.method == 'GET':
        return jsonify({"message": "This is a GET request"})

if __name__ == "__main__":
    app.run(debug=True)
